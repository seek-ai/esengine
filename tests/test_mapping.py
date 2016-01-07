from esengine import (
    Document, Mapping,
    IntegerField, LongField, StringField, FloatField,
    DateField, BooleanField, GeoPointField
)

class Doc(Document):
    _index = 'index'
    _doctype = 'doc_type'

    integerfield = IntegerField()
    longfield = LongField()
    stringfield = StringField()
    floatfield = FloatField()
    datefield = DateField()
    booleanfield = BooleanField()
    geopointfield = GeoPointField()


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
                'stringfield': {'type': 'string'}
            }
        }
    }



def test_change_format():
    mapping = Mapping(DocDate, enable_all=False).generate()
    assert mapping['doc_type']['_all']['enabled'] is False
    assert mapping['doc_type']['properties']['datefield']['format'] == 'yyyy-MM-dd||epoch_millis'