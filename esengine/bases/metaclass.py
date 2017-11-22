from esengine.fields import StringField
from esengine.bases.field import BaseField

from six import iteritems


class ModelMetaclass(type):

    def __new__(mcls, name, bases, attrs):  # noqa
        attrs['_fields'] = {}
        for base in bases:
            if hasattr(base, '_autoid'):
                if base._autoid and 'id' not in attrs:
                    attrs['id'] = StringField(field_name='id')
                break

        for base in bases:
            for key, value in iteritems(base.__dict__):
                if isinstance(value, BaseField):
                    value._field_name = key
                    attrs['_fields'][key] = value

        for key, value in iteritems(attrs):
            if isinstance(value, BaseField):
                value._field_name = key
                attrs['_fields'][key] = value
        cls = type.__new__(mcls, name, bases, attrs)
        if any(x.__name__ == 'EmbeddedDocument' for x in bases):
            cls._type = cls
        return cls
