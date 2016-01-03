# coding: utf-8

from datetime import datetime
from esengine.bases.field import BaseField
from esengine.exceptions import ValidationError

__all__ = [
    'IntegerField', 'LongField', 'StringField', 'FloatField',
    'DateField', 'BooleanField', 'GeoPointField'
]


class IntegerField(BaseField):
    _type = int
    _default_mapping = {'type': 'integer'}


class LongField(BaseField):
    _type = long
    _default_mapping = {'type': 'long'}


class StringField(BaseField):
    _type = unicode
    _default_mapping = {'type': 'string'}


class FloatField(BaseField):
    _type = float
    _default_mapping = {'type': 'float'}


class BooleanField(BaseField):
    _type = bool
    _default_mapping = {'type': 'boolean'}


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

    _default_mapping = {'type': 'geo_point'}

    def __init__(self, *args, **kwargs):
        self.mode = kwargs.pop('mode', 'dict')
        super(GeoPointField, self).__init__(*args, **kwargs)
        if self.mode == 'string':
            self._type = unicode

            def string_validator(field_name, value):
                values = [float(item.strip()) for item in value.split(',')]
                if not len(values) == 2:
                    raise ValidationError(
                        '2 elements "lat,lon" required in %s' % field_name
                    )

            self._validators.append(string_validator)

        elif self.mode == 'array':
            self._multi = True
            self._type = float

            def array_validator(field_name, value):
                if not len(value) == 2:
                    raise ValidationError(
                        '2 elements [lon, lat] required in %s' % field_name
                    )

            self._validators.append(array_validator)

        else:
            self._type = dict

            def dict_validator(field_name, value):
                for key in 'lat', 'lon':
                    if not isinstance(value.get(key), float):
                        raise ValidationError(
                            '%s: %s requires a float' % (field_name, key)
                        )

            self._validators.append(dict_validator)


class DateField(BaseField):
    _type = datetime
    _default_mapping = {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd"
    }

    @property
    def _date_format(self):
        return getattr(self, 'date_format', "%Y-%m-%d %H:%M:%S")

    def to_dict(self, value, validate=True):
        if validate:
            self.validate(value)
        if value:
            return value.strftime(self._date_format)

    def from_dict(self, serialized):
        if serialized:
            if self._multi:
                values = []
                for elem in serialized:
                    if isinstance(elem, self._type):
                        values.append(elem)
                    elif isinstance(elem, basestring):
                        date = datetime.strptime(elem, self._date_format)
                        values.append(date)
                    else:
                        raise ValueError(
                            'Expected str or date. {} found'.format(
                                elem.__class__
                            )
                        )
                return values
            else:
                if isinstance(serialized, self._type):
                    return serialized
                elif isinstance(serialized, basestring):
                    return datetime.strptime(serialized, self._date_format)
                raise ValueError('Expected str or date. {} found'.format(
                    serialized.__class__)
                )
