import warnings
from esengine.fields import StringField


class BaseDocument(object):
    _strict = False

    def _initialize_multi_fields(self):
        for key, field_class in self.__class__._fields.items():
            if field_class._multi:
                setattr(self, key, [])
            else:
                setattr(self, key, None)

    def __init__(self, *args, **kwargs):
        klass = self.__class__.__name__
        if not hasattr(self, '_doctype'):
            raise ValueError('{} have no _doctype attribute'.format(klass))
        if not hasattr(self, '_index'):
            raise ValueError('{} have no _index attribute'.format(klass))
        id_field = self.__class__._fields.get("id")
        if id_field and not isinstance(id_field, StringField):
            warnings.warn(
                'To avoid mapping problems, '
                'it is recommended to define the id field as a StringField'
            )
        self._initialize_multi_fields()
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __setattr__(self, key, value):
        if (not key.startswith('_')) and key not in self._fields:
            raise KeyError('`{}` is an invalid field'.format(key))
        field_instance = self._fields.get(key)
        if field_instance and not self._strict:
            value = field_instance.from_dict(value)
        super(BaseDocument, self).__setattr__(key, value)

    def to_dict(self):
        result = {}
        for field_name, field_instance in self._fields.iteritems():
            value = getattr(self, field_name)
            field_instance.validate(field_name, value)
            result.update({field_name: field_instance.to_dict(value)})
        return result

    @classmethod
    def from_dict(cls, dct):
        params = {}
        for field_name, field_instance in cls._fields.iteritems():
            serialized = dct.get(field_name)
            value = field_instance.from_dict(serialized)
            params[field_name] = value
        return cls(**params)
