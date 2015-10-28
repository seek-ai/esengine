from collections import Iterable

from es_engine.exceptions import RequiredField, InvalidMultiField
from es_engine.exceptions import FieldTypeMismatch


class BaseField(object):

    def __init__(self, field_type=None, required=False, multi=False, **kwargs):
        if field_type is not None:
            self.__type__ = field_type
        self._required = required
        self._multi = multi
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
                    if not isinstance(elem, self.__type__):
                        raise FieldTypeMismatch(field_name, self.__type__,
                                                elem.__class__)
            else:
                if not isinstance(value, self.__type__):
                    raise FieldTypeMismatch(field_name, self.__type__,
                                            value.__class__)

    def to_dict(self, value):
        return value

    def from_dict(self, serialized):
        if self._multi:
            return [self.__type__(x) for x in serialized]
        return self.__type__(serialized)
