from datetime import datetime

from es_engine.bases.field import BaseField


class IntegerField(BaseField):
    __type__ = int


class StringField(BaseField):
    __type__ = unicode


class FloatField(BaseField):
    __type__ = float


class DateField(BaseField):
    __type__ = datetime

    def to_dict(self, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    def from_dict(self, serialized):
        if self._multi:
            values = []
            for elem in serialized:
                if isinstance(elem, self.__type__):
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
            if isinstance(serialized, self.__type__):
                return serialized
            elif isinstance(serialized, basestring):
                return datetime.strptime(serialized, "%Y-%m-%d %H:%M:%S")
            raise ValueError('Expected str or date. {} found'.format(
                serialized.__class__)
            )
