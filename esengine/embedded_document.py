from collections import Iterable

from esengine.bases.field import BaseField
from esengine.bases.metaclass import ModelMetaclass
from esengine.exceptions import RequiredField, InvalidMultiField
from esengine.exceptions import FieldTypeMismatch

from six import with_metaclass, iteritems


class EmbeddedDocument(with_metaclass(ModelMetaclass, BaseField)):

    def _to_dict_element(self, real_obj):
        result = {}
        for field_name, field_class in iteritems(self._fields):
            value = getattr(real_obj, field_name)
            result.update({field_name: field_class.to_dict(value)})
        return result

    def to_dict(self, value):
        if value is not None:
            if self._multi:
                return [self._to_dict_element(elem) for elem in value]
            return self._to_dict_element(value)

    def _validate_element(self, elem):
        if not isinstance(elem, EmbeddedDocument):
            raise FieldTypeMismatch(self._field_name, self.__class__._type,
                                    elem.__class__)
        for field_name, field_class in iteritems(self._fields):
            value = getattr(elem, field_name)
            field_class.validate(value)

    def validate(self, value):
        if value is None:
            if self._required:
                raise RequiredField(self._field_name)
        else:
            if self._multi:
                if not isinstance(value, Iterable):
                    raise InvalidMultiField(self._field_name)
                for elem in value:
                    self._validate_element(elem)
            else:
                self._validate_element(value)

    def _from_dict_element(self, dct):
        params = {}
        for field_name, field_class in iteritems(self._fields):
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
