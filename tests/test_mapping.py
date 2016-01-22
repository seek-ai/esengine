from esengine import (
    Document, Mapping,
    IntegerField, LongField, StringField, FloatField,
    DateField, BooleanField, GeoPointField
)


class BaseDoc(Document):
    _index = 'index'

    @classmethod
    def put_mapping(cls, *args, **kwargs):
        cls.called = True


class Doc(BaseDoc):
    _doctype = 'doc_type'

    integerfield = IntegerField()
    longfield = LongField()
    stringfield = StringField()
    floatfield = FloatField()
    datefield = DateField()
    booleanfield = BooleanField()
    geopointfield = GeoPointField()


class Doc1(BaseDoc):
    _doctype = 'doc_type1'
    integerfield = IntegerField()


class DocDate(Doc):
    datefield = DateField(mapping={'format': 'yyyy-MM-dd||epoch_millis'})


def test_mapping():

    mapping = Mapping(Doc)

    assert mapping.generate() == {
        'doc_type': {
            '_all': {'enabled': True},
            'properties': {
                'booleanfield': {'type': 'boolean'},
                'datefield': {
                    'type': 'date'
                },
                'floatfield': {'type': 'float'},
                'geopointfield': {'type': 'geo_point'},
                'integerfield': {'type': 'integer'},
                'longfield': {'type': 'long'},
                'stringfield': {
                    "index": "analyzed",
                    "store": "yes",
                    'type': 'string'
                }
            }
        }
    }


def test_change_format():
    mapping = Mapping(DocDate, enable_all=False).generate()
    pattern = 'yyyy-MM-dd||epoch_millis'
    assert mapping['doc_type']['_all']['enabled'] is False
    assert mapping['doc_type']['properties']['datefield']['format'] == pattern


def test_configure_prerequiriments():
    mapping = Mapping()
    try:
        mapping.configure(10, None)
    except AttributeError as e:
        assert str(e) == 'models_to_mapping must be iterable'


def test_configure_prerequiriments_throw_on_index_existence():
    mapping = Mapping()
    try:
        models = [Doc, Doc1]
        es = ESMock()
        es.indices.exists_ret = True
        mapping.configure(models, True, es)
    except ValueError as e:
        assert str(e) == 'Settings are supported only on index creation'


def test_configure_without_settings():
    mapping = Mapping()
    models = [Doc, Doc1]
    mapping.configure(models, None)
    for model in models:
        assert model.called


def test_configure():
    mapping = Mapping()
    models = [Doc, Doc1]
    es = ESMock()
    es.indices.exists_ret = False
    settings = {
        "asdf": 'This is a test',
        "analyzer": {
            "my_analizer": "Another test"
        }
    }
    mapping.configure(models, settings, es)
    expected_mappings = {
        'doc_type': {
            '_all': {'enabled': True},
            'properties': {
                'booleanfield': {'type': 'boolean'},
                'datefield': {
                    'type': 'date'
                },
                'floatfield': {'type': 'float'},
                'geopointfield': {'type': 'geo_point'},
                'integerfield': {'type': 'integer'},
                'longfield': {'type': 'long'},
                'stringfield': {
                    "index": "analyzed",
                    "store": "yes",
                    'type': 'string'
                }
            }
        },
        'doc_type1': {
            '_all': {'enabled': True},
            'properties': {
                'integerfield': {'type': 'integer'},
            }
        }
    }
    expected_output = {
        "mappings": expected_mappings,
        "settings": settings
    }
    assert es.indices.create_return['index'] == expected_output


class ESMock(object):

    class Indice(object):
        exists_ret = False

        def exists(self, *args, **kwargs):
            return self.exists_ret

        def create(self, index, body):
            try:
                self.create_return[index] = body
            except:
                self.create_return = {}
                self.create_return[index] = body

    indices = Indice()

    def index(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        pass
