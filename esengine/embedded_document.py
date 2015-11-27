from collections import Iterable

from esengine.bases.field import BaseField
from esengine.bases.metaclass import ModelMetaclass
from esengine.exceptions import RequiredField, InvalidMultiField
from esengine.exceptions import FieldTypeMismatch


class EmbeddedDocument(BaseField):
    __metaclass__ = ModelMetaclass

    def _to_dict_element(self, real_obj):
        result = {}
        for field_name, field_class in self._fields.iteritems():
            value = getattr(real_obj, field_name)
            result.update({field_name: field_class.to_dict(value)})
        return result

    def to_dict(self, value):
        if value is not None:
            if self._multi:
                return [self._to_dict_element(elem) for elem in value]
            return self._to_dict_element(value)

    def _validate_element(self, field_name, elem):
        if not isinstance(elem, EmbeddedDocument):
            raise FieldTypeMismatch(field_name, self.__class__._type,
                                    elem.__class__)
        for field_name, field_class in self._fields.iteritems():
            value = getattr(elem, field_name)
            field_class.validate(field_name, value)

    def validate(self, field_name, value):
        if value is None:
            if self._required:
                raise RequiredField(field_name)
        else:
            if self._multi:
                if not isinstance(value, Iterable):
                    raise InvalidMultiField(field_name)
                for elem in value:
                    self._validate_element(field_name, elem)
            else:
                self._validate_element(field_name, value)

    def _from_dict_element(self, dct):
        params = {}
        for field_name, field_class in self._fields.iteritems():
            serialized = dct.get(field_name)
            value = field_class.from_dict(serialized)
            params[field_name] = value
        return self.__class__(**params)

    def from_dict(self, serialized):
        if serialized is None:
            return None
        if self._multi:
            return [self._from_dict_element(elem) for elem in serialized]
        return self._from_dict_element(serialized)
