import pytest

from esengine.bases.field import BaseField

from esengine.exceptions import RequiredField, InvalidMultiField
from esengine.exceptions import FieldTypeMismatch


def test_raise_when_required_fild_has_empty_value():
    field = BaseField(required=True, field_name="test")
    with pytest.raises(RequiredField) as ex:
        field.validate(None)
    assert str(ex.value) == "test"
    field = BaseField(required=False, field_name="test")
    field.validate(None)


def test_raise_when_multi_fild_is_not_iterable():
    field = BaseField(field_type=int, multi=True, field_name="test")
    field.validate([10])
    with pytest.raises(InvalidMultiField) as ex:
        field.validate(10)
    assert str(ex.value) == "test"


def test_raise_when_multi_fild_type_missmatch():
    field = BaseField(field_type=int, multi=True, field_name="test")
    with pytest.raises(FieldTypeMismatch) as ex:
        field.validate([10, 'asdf'])
    assert str(ex.value) == "`test` expected `" + str(int) + "`, actual `" + str(str) + "`" # noqa


def test_raise_when_nom_iterable_is_passed_to_multi():
    field = BaseField(field_type=int, required=False, field_name="test")
    field.validate(10)
    with pytest.raises(FieldTypeMismatch) as ex:
        field.validate([10])
    assert str(ex.value) == "`test` expected `" + str(int) + "`, actual `" + str(list) + "`" # noqa


def test_to_dict_return_same_value():
    field = BaseField(field_type=int, multi=True, field_name="test")
    x = [10, 11]
    assert field.to_dict(x) is x
    field = BaseField(field_type=int, multi=False, field_name="test")
    x = 10
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
