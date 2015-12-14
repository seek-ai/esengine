import pytest
from datetime import datetime
from esengine.fields import DateField


def test_date_field_to_dict():
    date = datetime.strptime("2015-01-15 00:01:59", "%Y-%m-%d %H:%M:%S")
    field = DateField()
    assert field.to_dict(date) == "2015-01-15 00:01:59"


def test_date_field_from_dict():
    str_date = "2015-01-15 00:01:59"
    date = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    field = DateField()
    assert field.from_dict(date) == date
    assert field.from_dict(str_date) == date
    with pytest.raises(ValueError) as ex:
        field.from_dict(10)
    assert str(ex.value) == "Expected str or date. <type 'int'> found"


def test_date_multi_field_from_dict():
    str_date = "2015-01-15 00:01:59"
    date = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    dates = [str_date, date]
    field = DateField(multi=True)
    assert field.from_dict(dates) == [date, date]
    with pytest.raises(ValueError) as ex:
        field.from_dict([10])
    assert str(ex.value) == "Expected str or date. <type 'int'> found"
