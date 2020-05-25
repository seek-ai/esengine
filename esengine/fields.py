# coding: utf-8
from esengine.bases.py3 import *  # noqa
from dateutil import parser
from datetime import datetime
from six import string_types
from esengine.bases.field import BaseField
from esengine.exceptions import ValidationError, FieldTypeMismatch
from esengine.utils.validation import FieldValidator

__all__ = [
    'IntegerField', 'LongField', 'KeywordField', 'FloatField',
    'DateField', 'UuidField', 'BooleanField', 'GeoPointField', 'ArrayField', 'ObjectField'
]


class IntegerField(BaseField):
    _type = int
    _default_mapping = {'type': 'integer'}


class LongField(BaseField):
    _type = long
    _default_mapping = {'type': 'long'}


class UuidField(BaseField):
    _type = unicode
    _default_mapping = {"store": "true", 'type': 'keyword'}


class KeywordField(BaseField):
    _type = unicode
    _default_mapping = {"index": "true", "store": "true", 'type': 'keyword'}


class FloatField(BaseField):
    _type = float
    _default_mapping = {'type': 'float'}


class BooleanField(BaseField):
    _type = bool
    _default_mapping = {'type': 'boolean'}


class ObjectField(BaseField):
    """
    Represent a typed or schema-less object (a python dict {})
    A mapping can be optionally defined in mapping argument
    example:

    >>> field = ObjectField(
    ...    mapping={"dynamic": False,
    ...             "properties": {"name": {"type": "string"}}
    ... )

    The above field will not store arbitrary properties and will accepts
    only string type in name property

    If multi=True the mapping type will be changed from 'object' to 'nested'

    If you need a more complex definition with fields and validators please
    take a look at embedded_document.EmbeddedDocument
    """
    _type = dict

    def __init__(self, *args, **kwargs):
        properties = kwargs.pop('properties', None)
        dynamic = kwargs.pop('dynamic', None)
        self._default_mapping = {'type': 'object'}
        self._default = {}
        super(ObjectField, self).__init__(*args, **kwargs)
        if dynamic is not None:
            self._default_mapping['dynamic'] = dynamic
        if properties is not None:
            self._default_mapping['properties'] = properties
        if self._multi:
            self._default_mapping['type'] = 'nested'


class ArrayField(BaseField):
    """
    ArrayField is by default a string type allowing multiple items of
    any type to be stored and retrieved as string

    It can be configured to use any of other fields as its type

    # to store an array of any objects as string
    field = ArrayField()

    # To store an array of integers (Float, Long etc)
    field = ArrayField(IntegerField())

    # As ArrayField is multi by default, if an ObjectField is used, the type
    # is turned in to 'nested' type to allow better searches.

    An array of arbitrary schema-less objects
    field = ArrayField(ObjectField())

    # equivalent to

    field = Arrayfield(field_type=dict, mapping={"type": "nested"})

    Or an array of schema strict documents

    >>> field = ArrayField(
    ...    ObjectField(
    ...        dynamic=False,
    ...        properties={"name": {"type": "string"}}
    ...    )
    ... )

    # NOTE: Schema validation is done only at E.S indexing level

    """
    _multi = True

    def __init__(self, field=None, *args, **kwargs):
        self.field = field
        self._default_mapping = {'type': 'string'}
        self._type = unicode
        if field:
            if isinstance(field, ObjectField):
                self.field._default_mapping['type'] = 'nested'
            self._default_mapping.update(self.field.mapping)
            self._type = field._type

        if 'default' not in kwargs:
            kwargs['default'] = []

        super(ArrayField, self).__init__(*args, **kwargs)

    def from_dict(self, serialized):
        """
        Transform data read from E.S to Python Object
        :param serialized: Result from E.S (string)
        :return: Instance or Instances of self._type
        """
        if serialized is not None:
            return [
                self.field.from_dict(x)
                if x is not None
                else x
                for x in serialized
            ]
        return self._default


class GeoPointStringValidator(FieldValidator):
    @staticmethod
    def validate_string(field, value):
        if value:
            values = [
                float(item.strip())
                for item in value.split(',')
            ]
            if not len(values) == 2:
                raise ValidationError(
                    '2 elements "lat,lon" required in %s' %
                    field._field_name
                )

    def validate_value(self, field, value):
        if not field._multi:
            self.validate_string(field, value)

    def validate_item(self, field, item):
        self.validate_string(field, item)


class GeoPointDictValidator(FieldValidator):
    @staticmethod
    def validate_dict(field, value):
        if value:
            for key in 'lat', 'lon':
                if not isinstance(value.get(key), float):
                    raise ValidationError(
                        '%s: %s requires a float' %
                        (field._field_name, key)
                    )

    def validate_value(self, field, value):
        if not field._multi:
            self.validate_dict(field, value)

    def validate_item(self, field, item):
        self.validate_dict(field, item)


class GeoPointField(BaseField):
    """
    A field to hold GeoPoint

    mode = dict|array|string

    >>> location = GeoPointField(mode='dict')  # default
    An object representation with lat and lon explicitly named
    >>> location = {"lat": 40.722, "lon": -73.989}}

    >>> location = GeoPointField(mode='string')
    A string representation, with "lat,lon"
    >>> location = "40.715, -74.011"

    >>> location = GeoPointField(mode='array')
    An array representation with [lon,lat].
    >>> location = [-73.983, 40.719]
    """

    def __init__(self, *args, **kwargs):
        self._default_mapping = {'type': 'geo_point'}
        self.mode = kwargs.pop('mode', 'dict')
        super(GeoPointField, self).__init__(*args, **kwargs)
        if self.mode == 'string':
            self._type = unicode
            self._validators.append(GeoPointStringValidator())

        elif self.mode == 'array':
            self._multi = True
            self._type = float
            self._default = []
            self._validators.append(_array_validator)

        else:
            self._type = dict
            self._default = {}
            self._validators.append(GeoPointDictValidator())

    def validate_field_type(self, value):
        if self.mode == 'array' and isinstance(value, list):
            def validate(val):
                if not isinstance(val, self._type):
                    raise FieldTypeMismatch(self._field_name,
                                            self._type,
                                            val.__class__)

            if value is not None:
                if any([isinstance(item, list) for item in value]):
                    [validate(item) for item in value]
        else:
            super(GeoPointField, self).validate_field_type(value)


def _validate_array_item(field, value):
    if value:
        if not len(value) == 2:
            raise ValidationError(
                '2 elements [lon, lat] required in %s' %
                field._field_name
            )


def _array_validator(field, value):
    if any([isinstance(item, list) for item in value]):
        # it is a multi location geo array
        [_validate_array_item(field, item) for item in value]
    else:
        _validate_array_item(field, value)


class DateField(BaseField):
    _type = datetime
    _default_mapping = {"type": "date"}

    @property
    def _date_format(self):
        """
        Optional string format used to send date value to E.S
        specified in DateField(date_format="%Y-%m-%d %H:%M:%S")
        if not specified isoformat() will be used
        :return: string date format or None
        """
        return getattr(self, 'date_format', None)

    def to_dict(self, value, validate=True):
        if self._multi:
            if not value:
                return []
            self.validate(value)
            if self._date_format:
                return [x.strftime(self._date_format) for x in value]
            return [x.isoformat() for x in value]
        else:
            if not value:
                return None
            if validate:
                self.validate(value)
            if self._date_format:
                return value.strftime(self._date_format)
            return value.isoformat()

    def from_dict(self, serialized):
        if serialized:
            if self._multi:
                values = []
                for elem in serialized:
                    if elem is None:
                        continue
                    if isinstance(elem, self._type):
                        values.append(elem)
                    elif isinstance(elem, string_types):
                        date = parser.parse(elem)
                        values.append(date)
                    else:
                        raise ValueError(
                            'Expected str or date. {} found'.format(
                                elem.__class__
                            )
                        )
                return values
            else:
                if serialized is None:
                    return None
                if isinstance(serialized, self._type):
                    return serialized
                elif isinstance(serialized, string_types):
                    return parser.parse(serialized)
                raise ValueError('Expected str or date. {} found'.format(
                    serialized.__class__)
                )
