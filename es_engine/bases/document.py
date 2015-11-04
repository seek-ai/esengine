class BaseDocument(object):
    def _initialize_multi_fields(self):
        for key, field_class in self.__class__._fields.items():
            if field_class._multi:
                setattr(self, key, [])
            else:
                setattr(self, key, None)

    def __init__(self, *args, **kwargs):
        klass = self.__class__.__name__
        if not hasattr(self, '__doc_type__'):
            raise ValueError('{} have no __doc_type__ field'.format(klass))
        if not hasattr(self, '__index__'):
            raise ValueError('{} have no __index__ field'.format(klass))
        self._initialize_multi_fields()
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __setattr__(self, key, value):
        if (not key.startswith('_')) and key not in self._fields:
            raise KeyError('`{}` is an invalid field'.format(key))
        super(BaseDocument, self).__setattr__(key, value)

    def to_dict(self):
        result = {}
        for field_name, field_class in self._fields.iteritems():
            value = getattr(self, field_name)
            field_class.validate(field_name, value)
            result.update({field_name: field_class.to_dict(value)})
        return result

    @classmethod
    def from_dict(cls, dct):
        params = {}
        for field_name, field_class in cls._fields.iteritems():
            serialized = dct.get(field_name)
            value = field_class.from_dict(serialized)
            params[field_name] = value
        return cls(**params)
