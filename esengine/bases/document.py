import warnings
from six import iteritems
from esengine.fields import StringField
from esengine.exceptions import ValidationError


class BaseDocument(object):
    _strict = False
    _validators = None
    _query_fields = None

    def _initialize_defaults_fields(self, ignore=None):
        ignore = ignore or []
        for key, field_instance in iteritems(self.__class__._fields):
            if key not in ignore:
                default = self.get_default_value_for_field(field_instance)
                setattr(self, key, default)

    def get_default_value_for_field(self, field_instance):
        default = field_instance._default
        if callable(default):
            try:
                default = field_instance._default(self, field_instance)
            except TypeError:
                default = field_instance._default()
        return default

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
        for key, value in iteritems(kwargs):
            setattr(self, key, value)
        self._initialize_defaults_fields(ignore=kwargs.keys())

    def __setattr__(self, key, value):
        if (not key.startswith('_')) and key not in self._fields:
            raise KeyError('`{}` is an invalid field'.format(key))
        field_instance = self._fields.get(key)
        if field_instance and not self._strict:
            value = field_instance.from_dict(value)
        super(BaseDocument, self).__setattr__(key, value)

    def to_dict(self, validate=True, only=None, exclude=None):
        """
        Transform value from Python to Dict to be saved in E.S
        :param validate: If should validate before transform
        :param only: if specified only those fields will be included
        :param exclude: fields to exclude from dict
        :return: dict
        """
        if validate:
            self.validate()

        if only:
            fields = {
                k: v for k, v in iteritems(self._fields)
                if k in only
            }
        elif exclude:
            fields = {
                k: v for k, v in iteritems(self._fields)
                if k not in exclude
            }
        else:
            fields = self._fields

        return {
            field_name: field_instance.to_dict(
                getattr(self, field_name), validate=validate
            )
            for field_name, field_instance in iteritems(fields)
        }

    @classmethod
    def from_dict(cls, dct):
        """
        Transform data read from E.S to Python Document Object
        :param dct: Result from E.S (hits, source as dict)
        :return: Instance of Document
        """
        params = {}
        for field_name, field_instance in iteritems(cls._fields):
            serialized = dct.get(field_name)
            value = field_instance.from_dict(serialized)
            params[field_name] = value
        return cls(**params)

    @classmethod
    def from_es(cls, hit):
        """
        Takes E.S hit element containing
        [u'_score', u'_type', u'_id', u'_source', u'_index']

        :param hit: E.S hit
        :return: Document instance
        """
        instance = cls.from_dict(dct=hit.get('_source', {}))
        instance._id = instance.id = hit.get('_id')
        instance._score = hit.get('_score')
        instance._query_fields = hit.get('fields', None)
        return instance

    def validate(self):
        if self._validators:
            for validator in self._validators:
                """
                Functions in self._validators receives document instance
                should return None or
                raise Exception (ValidationError) or return any value
                """
                val = validator(self)
                if val:
                    raise ValidationError("Invalid: %s" % val)
