

class Mapping(object):
    """
    Used to generate mapping based in document field definitions

    >>> class Obj(Document):
    ...     name = StringField()

    And you can use a Mapping to refresh mappings
    (use in cron jobs or call periodically)

    obj_mapping = Mapping(Obj)
    obj_mapping.save()

    """
    def __init__(self, document_class, enable_all=True):
        self.document_class = document_class
        self.enable_all = enable_all

    def generate(self):
        m = {
            self.document_class._doctype: {
                "_all": {"enabled": self.enable_all},
                "properties": {
                    field_name: field_instance.mapping
                    for field_name, field_instance in
                    self.document_class._fields.items()
                    if field_name != "id"
                }
            }
        }
        return m

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
