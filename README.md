ElasticSearch ODM (Object Document Mapper) based in MongoEngine
 

# install

```bash
pip install esengine
```

# Getting started

```python
from elasticsearch import ElasticSearch
from es_engine import Document, StringField

es = ElasticSearch(host='host', port=port)
```

# Defining a document

```python
class Person(Document):
    __doc_type__ = "person"
    __index__ = "universe"
    
    name = StringField()
    
```

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

By default ES engine does not try to implicit create a connection for you, but you can do it easily:

```python

from elasticsearch import ElasticSearch
from es_engine import Document, StringField
from es_engine.utils import validate_client


class Person(Document):
    __doc_type__ = "person"
    __index__ = "universe"
    
    name = StringField()
    
    @classmethod
    def get_es(cls, es):
        es = es or ElasticSearch(host='host', port=port)
        validate_client(es)
        return es
        
        
# Now you can use the document transport methods ommiting ES instance

person = Person(id=1234, name="Gonzo")
person.save()
         
Person.get(id=1234)

Person.filter(name="Gonzo")

```

# Contribute

ESEngine is OpenSource! join us!