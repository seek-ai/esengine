from collections import Iterable

from esengine.exceptions import RequiredField, InvalidMultiField
from esengine.exceptions import FieldTypeMismatch, ValidationError


class BaseField(object):
    _type = unicode
    _default = None
    _default_mapping = {'type': 'string'}

    def __init__(self, field_type=None, required=False, multi=False,
                 field_name=None, validators=None, mapping=None,
                 default=None, **kwargs):
        self._validators = validators or []
        self._field_name = field_name
        self._mapping = mapping or {}

        if field_type is not None:
            self._type = field_type

        self._required = required or getattr(self, '_required', False)
        self._multi = multi or getattr(self, '_multi', False)

        if default:
            self._default = default
        elif self._multi:
            self._default = []

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def validate_field_type(self, value):
        if value is not None:
            if not isinstance(value, self._type):
                raise FieldTypeMismatch(self._field_name,
                                        self._type,
                                        value.__class__)

    def validate(self, value):
        if value is None:
            if self._required:
                raise RequiredField(self._field_name)
        else:
            if self._multi:
                if not isinstance(value, Iterable):
                    raise InvalidMultiField(self._field_name)
                [self.validate_field_type(elem) for elem in value]
            else:
                self.validate_field_type(value)

        for validator in self._validators:
            """
            Functions in self._validators receives field_instance, value
            should return None or
            raise Exception (ValidationError) or return any value
            """
            val = validator(self, value)
            if val:
                raise ValidationError(
                    'Invalid %s, returned: %s' % (self._field_name, val)
                )

    def to_dict(self, value, validate=True):
        """
        Transform value from Python to be saved in E.S
        :param value: raw value
        :param validate: if should validate before transform
        :return: pure value
        """
        if validate:
            self.validate(value)
        return value

    def from_dict(self, serialized):
        """
        Transform data read from E.S to Python Object
        :param serialized: Result from E.S (string)
        :return: Instance or Instances of self._type
        """
        if serialized is not None:
            if self._multi:
                return [
                    self._type(x) if x is not None else x for x in serialized
                ]
            return self._type(serialized)
        return self._default

    @property
    def mapping(self):
        m = dict(**self._default_mapping)
        m.update(self._mapping)
        return m
