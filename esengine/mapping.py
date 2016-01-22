import collections


class Mapping(object):
    """
    Used to generate mapping based in document field definitions

    >>> class Obj(Document):
    ...     name = StringField()

    And you can use a Mapping to refresh mappings
    (use in cron jobs or call periodically)

    obj_mapping = Mapping(Obj)
    obj_mapping.save()

    Adicionally this class handle index settings configuration. However this
    operation must be done at elasticsearch index creation.

    """
    def __init__(self, document_class=None, enable_all=True):
        self.document_class = document_class
        self.enable_all = enable_all

    def _generate(self, doc_class):
        m = {
            doc_class._doctype: {
                "_all": {"enabled": self.enable_all},
                "properties": {
                    field_name: field_instance.mapping
                    for field_name, field_instance in doc_class._fields.items()
                    if field_name != "id"
                }
            }
        }
        return m

    def generate(self):
        return self._generate(self.document_class)

    def save(self, es=None):
        es = self.document_class.get_es(es)
        if not es.indices.exists(index=self.document_class._index):
            return es.indices.create(
                index=self.document_class._index,
                body={"mappings": self.generate()}
            )
        else:
            return es.indices.put_mapping(
                doc_type=self.document_class._doctype,
                index=self.document_class._index,
                body=self.generate()
            )

    def create_all(self, models_to_mapping, custon_settings, es=None):
        """
        Add custon settings like filters and analizers to index.

        Add custon settings, like filters and analizers, to index. Be aware
        that elasticsearch only allow this operation on index creation.
        """
        if not isinstance(models_to_mapping, collections.Iterable):
            raise AttributeError('models_to_mapping must be iterable')

        mapped_models = [x for x in models_to_mapping]
        if custon_settings:
            indexes = set()
            for model in mapped_models:
                indexes.add(model._index)
                if es is None:
                    es = model.get_es(es)
            for index in indexes:
                if es.indices.exists(index=index):
                    msg = 'Settings are supported only on index creation'
                    raise ValueError(msg)
            mappings_by_index = collections.defaultdict(dict)
            for model in mapped_models:
                mapping = self._generate(model)
                mappings_by_index[model._index].update(mapping)
            for index, mappings in mappings_by_index.items():
                settings = {
                    "settings": custon_settings,
                    "mappings": mappings
                }
                es.indices.create(index=index, body=settings)
        else:
            for model in mapped_models:
                model.put_mapping()
