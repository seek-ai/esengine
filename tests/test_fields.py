import pytest
from esengine.bases.py3 import *  # noqa
from datetime import datetime
from esengine import Document
from esengine.fields import (
    DateField, GeoPointField, ArrayField, LongField, StringField
)
from esengine.exceptions import ValidationError, FieldTypeMismatch

import sys


def test_date_field_to_dict():
    date = datetime.strptime("2015-01-15 00:01:59", "%Y-%m-%d %H:%M:%S")
    field = DateField(date_format="%Y-%m-%d %H:%M:%S")
    assert field.to_dict(date) == "2015-01-15 00:01:59"


def test_date_field_from_dict():
    str_date = "2015-01-15 00:01:59"
    date = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    field = DateField(date_format="%Y-%m-%d %H:%M:%S")
    assert field.from_dict(date) == date
    assert field.from_dict(str_date) == date
    with pytest.raises(ValueError) as ex:
        field.from_dict(10)
    assert str(ex.value) == "Expected str or date. " + str(int) + " found"


def test_date_multi_field_from_dict():
    str_date = "2015-01-15 00:01:59"
    date = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    dates = [str_date, date]
    field = DateField(multi=True, date_format="%Y-%m-%d %H:%M:%S")
    assert field.from_dict(dates) == [date, date]
    with pytest.raises(ValueError) as ex:
        field.from_dict([10])
    assert str(ex.value) == "Expected str or date. " + str(int) + " found"


def test_geo_field_dict_type():
    field = GeoPointField(field_name='test')
    value = {
        "lat": 40.722,
        "lon": -73.989
    }
    assert field.to_dict(value) == value


def test_geo_field_dict_lon_missing():
    field = GeoPointField(field_name='test')
    value = {
        "lat": 40.722
    }
    with pytest.raises(ValidationError) as ex:
        field.to_dict(value)
    assert str(ex.value) == "test: lon requires a float"


def test_geo_field_dict_lat_missing():
    field = GeoPointField(field_name='test')
    value = {
        "lon": -40.722
    }
    with pytest.raises(ValidationError) as ex:
        field.to_dict(value)
    assert str(ex.value) == "test: lat requires a float"


def test_geo_field_dict_invalid_lat_type():
    field = GeoPointField(field_name='test')
    value = {
        "lat": '40.722',
        "lon": -73.989
    }
    with pytest.raises(ValidationError) as ex:
        field.to_dict(value)
    assert str(ex.value) == "test: lat requires a float"


def test_geo_field_dict_invalid_lon_type():
    field = GeoPointField(field_name='test')
    value = {
        "lat": 40.722,
        "lon": list
    }
    with pytest.raises(ValidationError) as ex:
        field.to_dict(value)
    assert str(ex.value) == "test: lon requires a float"


def test_geo_field_dict_invalid_type():
    field = GeoPointField(field_name='test')
    value = [-73.989, 40.722]
    with pytest.raises(FieldTypeMismatch) as ex:
        field.to_dict(value)
    assert str(ex.value) == "`test` expected `" + str(dict) + "`, actual `" + str(list) + "`"  # noqa


def test_geo_field_string_type():
    field = GeoPointField(field_name='test', mode='string')
    value = u"40.715, -74.011"
    assert field.to_dict(value) == value


def test_geo_field_string_value_missing():
    field = GeoPointField(field_name='test', mode='string')
    value = u"40.715"
    with pytest.raises(ValidationError) as ex:
        field.to_dict(value)
    assert str(ex.value) == '2 elements "lat,lon" required in test'


def test_geo_field_string_invalid_type():
    field = GeoPointField(field_name='test', mode='string')
    value = u"asdf, error"
    with pytest.raises(ValueError) as ex:
        field.to_dict(value)
    msg = 'could not convert string to float: asdf'
    if sys.version_info > (3,):
        msg = "could not convert string to float: 'asdf'"
    assert str(ex.value) == msg


def test_geo_field_array_type():
    field = GeoPointField(field_name='test', mode='array')
    value = [40.715, -74.011]
    assert field.to_dict(value) == value


def test_geo_field_array_value_missing():
    field = GeoPointField(field_name='test', mode='array')
    value = [40.715]
    with pytest.raises(ValidationError) as ex:
        field.to_dict(value)
    assert str(ex.value) == '2 elements [lon, lat] required in test'


def test_geo_field_array_invalid_type():
    field = GeoPointField(field_name='test', mode='array')
    value = [40.715, list]
    with pytest.raises(FieldTypeMismatch) as ex:
        field.to_dict(value)
    msg = "`test` expected `<type 'float'>`, actual `<type 'type'>`"
    if sys.version_info > (3,):
        msg = "`test` expected `<class 'float'>`, actual `<class 'type'>`"
    assert str(ex.value) == msg


def test_geo_field_dict_multi():
    field = GeoPointField(field_name='test', multi=True)
    value = [
        {
            "lat": 40.722,
            "lon": -73.989
        },
        {
            "lat": 40.722,
            "lon": -73.989
        },
        {
            "lat": 40.722,
            "lon": -73.989
        }
    ]
    assert field.to_dict(value) == value


def test_geo_field_string_type_multi():
    field = GeoPointField(field_name='test', mode='string', multi=True)
    value = [u"40.715, -74.011", u"40.715, -74.011", u"40.715, -74.011"]
    assert field.to_dict(value) == value


def test_geo_field_array_type_multi():
    field = GeoPointField(field_name='test', mode='array', multi=True)
    value = [[40.715, -74.011], [40.715, -74.011], [40.715, -74.011]]
    assert field.to_dict(value) == value


def test_geo_field_dict_multi_invalid():
    field = GeoPointField(field_name='test', multi=True)
    value = [
        {
            "lat": 40.722,
            "lon": -73.989
        },
        {
            "lat": 40.722,
            "lon": -73.989
        },
        {
            "lat": 40.722
        }
    ]
    with pytest.raises(ValidationError) as ex:
        field.to_dict(value)
    assert str(ex.value) == "test: lon requires a float"


def test_geo_field_string_type_multi_invalid():
    field = GeoPointField(field_name='test', mode='string', multi=True)
    value = [u"40.715, -74.011", u"40.715, -74.011", u"40.715"]
    with pytest.raises(ValidationError) as ex:
        field.to_dict(value)
    assert str(ex.value) == '2 elements "lat,lon" required in test'


def test_geo_field_array_type_multi_invalid():
    field = GeoPointField(field_name='test', mode='array', multi=True)
    value = [[40.715, -74.011], [40.715], [40.715, -74.011]]
    with pytest.raises(ValidationError) as ex:
        field.to_dict(value)
    assert str(ex.value) == '2 elements [lon, lat] required in test'


def test_geo_field_array_type_multi_invalid_type():
    field = GeoPointField(field_name='test', mode='array', multi=True)
    value = [[40.715, -74.011], [40.715], list]
    with pytest.raises(FieldTypeMismatch) as ex:
        field.to_dict(value)
    msg = "`test` expected `<type 'float'>`, actual `<type 'type'>`"
    if sys.version_info > (3,):
        msg = "`test` expected `<class 'float'>`, actual `<class 'type'>`"
    assert str(ex.value) == msg


def test_array_field():
    class DocWithArrays(Document):
        _index = 'text_indice'
        _doctype = 'DocWithArrays'
        date_array = ArrayField(DateField())
        long_array = ArrayField(LongField())
        str_array = ArrayField(StringField())
        empyt_array = ArrayField(StringField())

    example = {
        "date_array": ["2016-10-04 15:15:05", u'1967-07-28'],
        "long_array": [10, 20, '42'],
        "str_array": ['asdf'],
        "empyt_array": []
    }
    doc = DocWithArrays.from_dict(example)
    dates = [
        datetime.strptime(example["date_array"][0], "%Y-%m-%d %H:%M:%S"),
        datetime.strptime(example["date_array"][1], "%Y-%m-%d")
    ]
    assert doc.date_array == dates
    assert doc.long_array == [long(x) for x in example["long_array"]]
    assert doc.str_array == example["str_array"]
    assert doc.empyt_array == example["empyt_array"]


def test_date_field_from_dict_accept_none():
    field = DateField(multi=True)
    serialized = [None]
    assert field.from_dict(serialized) == []
