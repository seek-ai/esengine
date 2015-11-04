import pytest

from es_engine.bases.metaclass import ModelMetaclass
from es_engine.bases.field import BaseField
from es_engine.embedded_document import EmbeddedDocument

from es_engine.exceptions import RequiredField, InvalidMultiField
from es_engine.exceptions import FieldTypeMismatch

class NoFields(object):
    __metaclass__ = ModelMetaclass

class OneField(object):
    __metaclass__ = ModelMetaclass
    field = BaseField(field_type=int, required=False, multi=False)


def test_derived_class_has_fields_attr():
    assert hasattr(NoFields, '_fields')
    assert len(NoFields._fields) == 0

def test_derived_class_has_correct_field_attr():
    assert hasattr(OneField, '_fields')
    assert len(OneField._fields) == 1
    assert 'field' in OneField._fields
    assert isinstance(OneField._fields['field'], BaseField)
    # assert isinstance(OneField.field, BaseField)

def test_has_type_field_if_is_EmbeddedDocument():
    obj = ModelMetaclass.__new__(ModelMetaclass, 'name_test', (EmbeddedDocument,), {})
    assert hasattr(obj, '__type__')
    assert getattr(obj, '__type__') is obj

def test_raise_when_required_fild_has_empty_value():
    field = BaseField(required=True)
    with pytest.raises(RequiredField):
        field.validate('test', None)
    field = BaseField(required=False)
    field.validate('test', None)

def test_raise_when_multi_fild_is_not_iterable():
    field = BaseField(field_type=int, multi=True)
    field.validate('test', [10])
    with pytest.raises(InvalidMultiField):
        field.validate('test', 10)

def test_raise_when_multi_fild_type_missmatch():
    field = BaseField(field_type=int, multi=True)
    with pytest.raises(FieldTypeMismatch):
        field.validate('test', [10, 'asdf'])

def test_raise_when_nom_iterable_is_passed_to_multi():
    field = BaseField(field_type=int, required=False)
    field.validate('test', 10)
    with pytest.raises(FieldTypeMismatch):
        field.validate('test', [10])

def test_to_dict_return_same_value():
    field = BaseField(field_type=int, multi=True)
    x = 10
    assert field.to_dict(x) is x
    field = BaseField(field_type=int, multi=False)
    assert field.to_dict(x) is x

def test_from_dict_cast():
    field = BaseField(field_type=int, multi=False)
    x = '10'
    assert field.from_dict(x) == int(x)
    field = BaseField(field_type=int, multi=True)
    x = ['10', '11', '12']
    assert field.from_dict(x) == [int(a) for a in x]

def test_base_field_set_attr():
    field = BaseField(field_type=int, multi=False, asdf=10)
    assert field.asdf == 10
  