__all__ = [
    'IntegerField', 'StringField', 'FloatField',
    'DateField', 'BooleanField', 'GeoField'
]

from datetime import datetime
from esengine.bases.field import BaseField


class IntegerField(BaseField):
    _type = int


class LongField(BaseField):
    _type = long


class StringField(BaseField):
    _type = unicode


class FloatField(BaseField):
    _type = float


class BooleanField(BaseField):
    _type = bool


class GeoField(FloatField):
    _multi = True


class DateField(BaseField):
    _type = datetime

    @property
    def _date_format(self):
        return getattr(self, 'date_format', "%Y-%m-%d %H:%M:%S")

    def to_dict(self, value):
        if value:
            return value.strftime(self._date_format)

    def from_dict(self, serialized):
        if serialized:
            if self._multi:
                values = []
                for elem in serialized:
                    if isinstance(elem, self._type):
                        values.append(elem)
                    elif isinstance(elem, basestring):
                        date = datetime.strptime(elem, self._date_format)
                        values.append(date)
                    else:
                        raise ValueError(
                            'Expected str or date. {} found'.format(
                                elem.__class__
                            )
                        )
                return values
            else:
                if isinstance(serialized, self._type):
                    return serialized
                elif isinstance(serialized, basestring):
                    return datetime.strptime(serialized, self._date_format)
                raise ValueError('Expected str or date. {} found'.format(
                    serialized.__class__)
                )
