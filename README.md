[![Travis CI](http://img.shields.io/travis/catholabs/esengine.svg)](https://travis-ci.org/catholabs/esengine)
[![Coverage Status](http://img.shields.io/coveralls/catholabs/esengine.svg)](https://coveralls.io/r/catholabs/esengine)
[![Code Health](https://landscape.io/github/catholabs/esengine/development/landscape.svg?style=flat)](https://landscape.io/github/catholabs/esengine/development)
<a href="http://smallactsmanifesto.org" title="Small Acts Manifesto"><img src="http://smallactsmanifesto.org/static/images/smallacts-badge-80x15-blue.png" style="border: none;" alt="Small Acts Manifesto" /></a>

# ElasticSearch ODM (Object Document Mapper) based in MongoEngine
 

# install

ESengine depends on elasticsearch-py (Official E.S Python library) so the instalation 
depends on the version of elasticsearch you are using.


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

# filtering by IDS

```python
ids = [1234, 5678, 9101]
power_trio = Person.filter(ids=ids)
```


# filtering by fields

```python
Person.filter(name="Gonzo", es=es)
```

# Searching

ESengine does not try to create abstraction for query building, 
by default ESengine only implements search transport receiving a raw ES query 
in form of a Python dictionary.

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

By default ES engine does not try to implicit create a connection for you, 
but you can easily achieve this overwriting the **get_es** method and returning a 
default connection or using any kind of technique as RoundRobin or Mocking for tests
Also you can set the **_es** attribute pointing to a function generating the connection client
or the client instance as the following example:

```python

from elasticsearch import ElasticSearch
from esengine import Document, StringField
from esengine.utils import validate_client


class Person(Document):
    _doctype = "person"
    _index = "universe"
    _es = Elasticsearch(host='10.0.0.0')
    
    name = StringField()
    
```
        
# Now you can use the document transport methods ommiting ES instance


```python
person = Person(id=1234, name="Gonzo")
person.save()
         
Person.get(id=1234)

Person.filter(name="Gonzo")
```


# Updating

##  A single document

A single document can be updated simply using the **.save()** method

```python

person = Person.get(id=1234)
person.name = "Another Name"
person.save()

```

## Updating a Resultset

The Document methods **.get**, **.filter** and **.search** will return an instance
of **ResultSet** object. This object is an Iterator containing the **hits** reached by 
the filtering or search process and exposes some CRUD methods[ **update**, **delete** and **reload** ]
to deal with its results.


```python
people = Person.filter(field='value')
people.update(another_field='another_value')
```

> When updating documents sometimes you need the changes done in the E.S index reflected in the objects 
of the **ResultSet** iterator, so you can use **.reload** method to perform that action.


## The use of **reload** method
 
```python
people = Person.filter(field='value')
print people
... <Resultset: [{'field': 'value', 'another_field': None}, 
                 {'field': 'value', 'another_field': None}]>

# Updating another field on both instances
people.update(another_field='another_value')
print people
... <Resultset: [{'field': 'value', 'another_field': None}, {'field': 'value', 'another_field': None}]>

# Note that in E.S index the values weres changed but the current ResultSet is not updated by defaul
# you have to fire an update
people.reload()

print people
... <Resultset: [{'field': 'value', 'another_field': 'another_value'},
                 {'field': 'value', 'another_field': 'another_value'}]>


```

## Deleting documents


### A ResultSet

```python
people = Person.all()
people.delete()
```

### A single document

```python
Person.get(id=123).delete()
```

# Bulk operations

ESEngine takes advantage of elasticsearch-py helpers for bulk actions, 
the **ResultSet** object uses **bulk** melhod to **update** and **delete** documents.

But you can use it in a explicit way using Document's **update_all**, **save__all** and **delete_all** methods.

### Lets create a bunch of document instances


```python
top_5_racing_bikers = []

for name in ['Eddy Merckx', 
             'Bernard Hinault', 
             'Jacques Anquetil', 
             'Sean Kelly', 
             'Lance Armstrong']:
     top_5_racing_bikers.append(Person(name=name))
```

### Save it all 

```python
Person.save_all(top_5_racing_bikers)
```

### Using the **create** shortcur

The above could be achieved using **create** shortcut


#### A single

```python
Person.create(name='Eddy Merckx', active=False)
```

> Create will return the instance of the indexed Document

#### All using list comprehension

```python
top_5_racing_bikers = [
    Person.create(name=name, active=False)
    for name in ['Eddy Merckx', 
                 'Bernard Hinault', 
                 'Jacques Anquetil', 
                 'Sean Kelly', 
                 'Lance Armstrong']
]

```
> NOTE: **.create** method will automatically save the document to the index, and
will not raise an error if there is a document with the same ID (if specified), it will update it acting as upsert.

### Updating all

Turning the field **active** to **True** for all documents

```python
Person.update_all(top_5_racing_bikes, active=True)
```

### Deleting all

```python
Person.delete_all(top_5_racing_bikes)
```


### Chunck size

chunk_size is number of docs in one chunk sent to ES (default: 500)
you can change using **meta** argument.

```python
Person.update_all(
    top_5_racing_bikes, # the documents
    active=True,  # values to be changed
    metal={'chunk_size': 200}  # meta data passed to **bulk** operation    
)
```

# Contribute

ESEngine is OpenSource! join us!