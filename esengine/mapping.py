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
        """
        Generate the mapping acording to doc_class.

        Args:
            doc_class: esengine.Document object containing the model to be
            mapped to elasticsearch.
        """
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
        """
        Save the mapping to index.

        Args:
            es: elasticsearch client intance.
        """
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

    def configure(self, models_to_mapping, custom_settings=None, es=None):
        """
        Add custon settings like filters and analizers to index.

        Add custon settings, like filters and analizers, to index. Be aware
        that elasticsearch only allow this operation on index creation.

        Args:
            models_to_mapping: A list with the esengine.Document objects that
            we want generate mapping.

            custom_settings: a dict containing the configuration that will be
            sent to elasticsearch/_settings (www.elastic.co/guide/en/
                elasticsearch/reference/current/indices-update-settings.html)

            es: elasticsearch client intance.
        """
        if not isinstance(models_to_mapping, collections.Iterable):
            raise AttributeError('models_to_mapping must be iterable')

        mapped_models = [x for x in models_to_mapping]
        if custom_settings:
            indexes = set()
            for model in mapped_models:
                indexes.add(model._index)
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
                    "settings": custom_settings,
                    "mappings": mappings
                }
                es.indices.create(index=index, body=settings)
        else:
            for model in mapped_models:
                model.put_mapping()
