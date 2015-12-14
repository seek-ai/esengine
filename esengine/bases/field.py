from collections import Iterable

from esengine.exceptions import RequiredField, InvalidMultiField
from esengine.exceptions import FieldTypeMismatch


class BaseField(object):

    def __init__(self, field_type=None, required=False, multi=False, **kwargs):
        if field_type is not None:
            self._type = field_type
        self._required = required or getattr(self, '_required', False)
        self._multi = multi or getattr(self, '_multi', False)
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def validate(self, field_name, value):
        if value is None:
            if self._required:
                raise RequiredField(field_name)
        else:
            if self._multi:
                if not isinstance(value, Iterable):
                    raise InvalidMultiField(field_name)
                for elem in value:
                    if not isinstance(elem, self._type):
                        raise FieldTypeMismatch(field_name, self._type,
                                                elem.__class__)
            else:
                if not isinstance(value, self._type):
                    raise FieldTypeMismatch(field_name, self._type,
                                            value.__class__)

    def to_dict(self, value):
        return value

    def from_dict(self, serialized):
        if serialized is not None:
            if self._multi:
                return [self._type(x) for x in serialized]
            return self._type(serialized)
