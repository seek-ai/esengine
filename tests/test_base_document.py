import pytest
from esengine.bases.py3 import *  # noqa
from esengine.bases.document import BaseDocument
from esengine.bases.field import BaseField
from esengine.fields import StringField, IntegerField

from esengine.exceptions import FieldTypeMismatch


def test_raise_when_doc_has_no_doc_type():
    with pytest.raises(ValueError):
        BaseDocument()


def test_raise_when_doc_has_no_index():
    class WhitoutIndex(BaseDocument):
        _doctype = 'test'

    class WhitIndex(BaseDocument):
        _doctype = 'test'
        _index = 'test'
        _fields = {}

    with pytest.raises(ValueError) as ex:
        WhitoutIndex()
    assert str(ex.value) == '{} have no _index attribute'.format(
        WhitoutIndex.__name__
    )
    WhitIndex()


def test_raise_if_doc_has_no_fields():
    class WhitoutFields(BaseDocument):
        _doctype = 'test'
        _index = 'test'

    class WhitFields(BaseDocument):
        _doctype = 'test'
        _index = 'test'
        _fields = {}

    with pytest.raises(AttributeError) as ex:
        WhitoutFields()
    assert str(ex.value) == "type object '{}' has no attribute '{}'".format(
        WhitoutFields.__name__,
        '_fields'
    )
    WhitFields()


def test_doc_set_kwargs():
    class Doc(BaseDocument):
        _doctype = 'test'
        _index = 'test'
        _fields = {}

        def __setattr__(self, key, value):
            if key not in self._fields:
                if isinstance(value, basestring):
                    self._fields[key] = StringField()
                elif isinstance(value, int):
                    self._fields[key] = IntegerField()
                else:
                    self._fields[key] = StringField(_multi=True)
            super(Doc, self).__setattr__(key, value)

    x = Doc(asdf='0', x=10, value=['a', 'b'], _value='aaa')
    assert x.asdf == '0'
    assert x.x == 10
    assert x.value == ['a', 'b']
    assert x._value == 'aaa'


def test_raise_if_attr_not_in_fields():
    class Doc(BaseDocument):
        _doctype = 'test'
        _index = 'test'
        _fields = {}

    with pytest.raises(KeyError) as ex:
        Doc(asdf='0')
    assert str(ex.value) == "'`{}` is an invalid field'".format('asdf')


def test_doc_setattr_():
    def pass_func(self, ignore=None):
        pass

    class Doc(BaseDocument):
        _doctype = 'test'
        _index = 'test'
        _fields = {"asdf": 1}
    Doc._initialize_defaults_fields = pass_func

    doc = Doc()
    with pytest.raises(AttributeError) as ex:
        doc.asdf = "0"
        assert ex.message == "'int' object has no attribute 'from_dict'"

    doc.__setattr__('_test', 10)
    assert doc._test == 10


def test_doc_initialize_multi_fields():
    class Doc(BaseDocument):
        _doctype = 'test'
        _index = 'test'
        _fields = {
            'multiple': BaseField(field_type=int, multi=True),
            'simple': BaseField(field_type=int)
        }
    doc = Doc()
    assert doc.multiple == []
    assert doc.simple is None


def test_doc_to_dict():
    class Doc(BaseDocument):
        _doctype = 'test'
        _index = 'test'
        _fields = {
            'multiple': BaseField(field_type=int, multi=True),
            'simple': BaseField(field_type=int)
        }
    doc = Doc(multiple=[1, 2], simple=10)
    assert doc.to_dict() == {'multiple': [1, 2], 'simple': 10}


def test_doc_to_dict_call_validate():
    class Doc(BaseDocument):
        _doctype = 'test'
        _index = 'test'
        _strict = True
        _fields = {
            'multiple': BaseField(field_type=int, multi=True,
                                  field_name='multiple'),
            'simple': BaseField(field_type=int, field_name='simple')
        }
    doc = Doc(multiple=[1, 2], simple="10")
    with pytest.raises(FieldTypeMismatch) as ex:
        doc.to_dict()
    assert str(ex.value) == (
        "`simple` expected `" + str(int) + "`, actual `" + str(str) + "`"
    )


def test_doc_from_dict():
    class Doc(BaseDocument):
        _doctype = 'test'
        _index = 'test'
        _fields = {
            'multiple': BaseField(field_type=int, multi=True),
            'simple': BaseField(field_type=int)
        }
    dict_doc = {'multiple': [1, 2], 'simple': 10}
    doc = Doc.from_dict(dict_doc)
    assert doc.multiple == [1, 2]
    assert doc.simple == 10
