import pytest
from datetime import datetime
from esengine.fields import DateField, GeoPointField
from esengine.exceptions import ValidationError, FieldTypeMismatch


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
    assert str(ex.value) == "Expected str or date. <type 'int'> found"


def test_date_multi_field_from_dict():
    str_date = "2015-01-15 00:01:59"
    date = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    dates = [str_date, date]
    field = DateField(multi=True, date_format="%Y-%m-%d %H:%M:%S")
    assert field.from_dict(dates) == [date, date]
    with pytest.raises(ValueError) as ex:
        field.from_dict([10])
    assert str(ex.value) == "Expected str or date. <type 'int'> found"


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
    assert str(ex.value) == "`test` expected `<type 'dict'>`, actual `<type 'list'>`"  # noqa


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
    value = u"test, error"
    with pytest.raises(ValueError) as ex:
        field.to_dict(value)
    assert str(ex.value) == 'could not convert string to float: test'


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
    assert str(ex.value) == "`test` expected `<type 'float'>`, actual `<type 'type'>`"  # noqa


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
    assert str(ex.value) == "`test` expected `<type 'float'>`, actual `<type 'type'>`"  # noqa
