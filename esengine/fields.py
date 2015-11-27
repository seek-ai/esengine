from datetime import datetime

from esengine.bases.field import BaseField


class IntegerField(BaseField):
    _type = int


class StringField(BaseField):
    _type = unicode


class FloatField(BaseField):
    _type = float


class DateField(BaseField):
    _type = datetime

    def to_dict(self, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    def from_dict(self, serialized):
        if self._multi:
            values = []
            for elem in serialized:
                if isinstance(elem, self._type):
                    values.append(elem)
                elif isinstance(elem, basestring):
                    date = datetime.strptime(elem, "%Y-%m-%d %H:%M:%S")
                    values.append(date)
                else:
                    raise ValueError('Expected str or date. {} found'.format(
                        elem.__class__)
                    )
            return values
        else:
            if isinstance(serialized, self._type):
                return serialized
            elif isinstance(serialized, basestring):
                return datetime.strptime(serialized, "%Y-%m-%d %H:%M:%S")
            raise ValueError('Expected str or date. {} found'.format(
                serialized.__class__)
            )
