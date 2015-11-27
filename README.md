ElasticSearch ODM (Object Document Mapper) based in MongoEngine
 

# install

ESEngine depends on elasticsearch Python library so the instalation depends on the version of elasticsearch you are using


## Elasticsearch 2.x

```bash
pip install esengine[es2]
```

## Elasticsearch 1.x

```bash
pip install esengine[es1]
```

## Elasticsearch 0.90.x

```bash
pip install esengine[es0]
```

The above command will install esengine and the elasticsearch library specific for you ES version.


> Alternatively you can install elasticsearch library before esengine

pip install ``<version-specific-es>`` 

- for 2.0 + use "elasticsearch>=2.0.0,<3.0.0"
- for 1.0 + use "elasticsearch>=1.0.0,<2.0.0"
- under 1.0 use "elasticsearch<1.0.0"

Then install esengine

```bash
pip install esengine
```

# Getting started

```python
from elasticsearch import ElasticSearch
from esengine import Document, StringField

es = ElasticSearch(host='host', port=port)
```

# Defining a document

```python
class Person(Document):
    _doctype = "person"
    _index = "universe"
    
    name = StringField()
    
```

> If you do not specify an "id" field, ESEngine will automatically add "id" as StringField. It is recommended that when specifying you use StringField for ids.

# Indexing

```python
person = Person(id=1234, name="Gonzo")
person.save(es=es)
```

# Getting by id

```python
Person.get(id=1234, es=es)
```

# filtering by fields

```python
Person.filter(name="Gonzo", es=es)
```

# Searching

ESengine does not try to create abstratction for query building, but it is provided by a [plugin](http://plugin) 
by default ESengine only implements search transport receiving a raw ES query in form of a Python dictionary.

```python
query = {
    "query": {
        "filtered": {
            "query": {
                "match_all": {}
            },
            "filter": {
                "ids": {
                    "values": list(ids)
                }
            }
        }
    }
}
Person.search(query, size=10, es=es)
```

# Default connection

By default ES engine does not try to implicit create a connection for you, but you can easily achieve this overwriting the **get_es** method and returning a default connection or using any kind of technique as RoundRobin or Mocking for tests

```python

from elasticsearch import ElasticSearch
from esengine import Document, StringField
from esengine.utils import validate_client


class Person(Document):
    _doctype = "person"
    _index = "universe"
    
    name = StringField()
    
    @classmethod
    def get_es(cls, es):
        es = es or ElasticSearch(host='host', port=port)
        validate_client(es)
        return es
```
        
# Now you can use the document transport methods ommiting ES instance


```python
person = Person(id=1234, name="Gonzo")
person.save()
         
Person.get(id=1234)

Person.filter(name="Gonzo")
```

# Contribute

ESEngine is OpenSource! join us!