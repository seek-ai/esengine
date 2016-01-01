

class Mapping(object):
    """
    Used to generate mapping based in document field definitions

    class Obj(Document):
        name = StringField()

    And you can use a Mapping to refresh mappings
    (use in cron jobs or call periodically)

    obj_mapping = Mapping(Obj)
    obj_mapping.save()

    """

    _mapping = {}

    def __init__(self, document_class):
        self.document_class = document_class

    def generate(self):
        for field_name, field_instance in self._fields.items():
            self._mapping[field_name] = field_instance.mapping

    def save(self):
        pass
