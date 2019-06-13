import pytest

from esengine.embedded_document import EmbeddedDocument
from esengine.exceptions import RequiredField, InvalidMultiField
from esengine.exceptions import FieldTypeMismatch
from esengine.fields import IntegerField


class TowFields(EmbeddedDocument):
        x = IntegerField()
        y = IntegerField()


def test_pass_none_to_to_dict():
    field = TowFields()
    assert field.to_dict(None) is None


def test_to_dict():
    field = TowFields(x=10, y=15)
    assert field.to_dict(field) == {'x': 10, 'y': 15}


def test_multi_to_dict():
    field = TowFields(multi=True, x=10, y=15)
    assert field.to_dict([field, field]) == [
        {'x': 10, 'y': 15}, {'x': 10, 'y': 15}
    ]


def test_raise_when_validate_is_not_multi_field():
    field = TowFields(multi=True, field_name="test")
    with pytest.raises(InvalidMultiField) as ex:
        field.validate(10)
    assert str(ex.value) == "test"


def test_raise_when_validate_required_field():
    field = TowFields(required=True, field_name="test")
    with pytest.raises(RequiredField) as ex:
        field.validate(None)
    assert str(ex.value) == "test"


def test_validate():
    field = TowFields(x=10, y=15, field_name="test")
    field.validate(field)


def test_validate_multi():
    field = TowFields(multi=True, x=10, y=15, field_name="test")
    field.validate([field, field])


def test_raise_when_multi_fild_type_missmatch():
    field = TowFields(multi=True, field_name="test")
    with pytest.raises(FieldTypeMismatch) as ex:
        field.validate([10, 'asdf'])
    tmpl = "`{field._field_name}` expected `{field._type}`, actual `" + str(int) + "`"  # noqa
    assert str(ex.value) == tmpl.format(
        field=field
    )


def test_none_from_dict():
    field = TowFields()
    assert field.from_dict(None) is None


def test_from_dict():
    field = TowFields()
    value = field.from_dict({'y': 10, 'x': 15})
    assert value.x == 15
    assert value.y == 10
    value = field.from_dict({'y': '11', 'x': '1'})
    assert value.x == 1
    assert value.y == 11


def test_multi_from_dict():
    field = TowFields(multi=True)
    dct_serialized_list = [{'y': 10, 'x': 15}, {'y': 1, 'x': 2}]
    values = field.from_dict(dct_serialized_list)
    for i, value in enumerate(values):
        assert value.x == dct_serialized_list[i]['x']
        assert value.y == dct_serialized_list[i]['y']
