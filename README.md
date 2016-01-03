
<img src="https://raw.githubusercontent.com/catholabs/esengine/master/octosearch.gif" align="left" width="192px" height="132px"/>
<img align="left" width="0" height="192px" hspace="10"/>

> **esengine** - The **E**lastic**s**earch **O**bject **D**ocument **M**apper

[![PyPI](https://img.shields.io/pypi/v/esengine.svg)](https://pypi.python.org/pypi/esengine)
[![versions](https://img.shields.io/pypi/pyversions/esengine.svg)](https://pypi.python.org/pypi/esengine)
[![downloads](https://img.shields.io/pypi/dw/esengine.svg)](https://pypi.python.org/pypi/esengine)
[![Travis CI](http://img.shields.io/travis/catholabs/esengine.svg)](https://travis-ci.org/catholabs/esengine)
[![Coverage Status](http://img.shields.io/coveralls/catholabs/esengine.svg)](https://coveralls.io/r/catholabs/esengine)
[![Code Health](https://landscape.io/github/catholabs/esengine/master/landscape.svg?style=flat)](https://landscape.io/github/catholabs/esengine/master)


**esengine** is an ODM (**O**bject **D**ocument **M**apper) it maps Python classes in to **E**lastic**s**earch **index/doc_type** and **object instances()** in to Elasticsearch documents.

<br><br>

### Modeling

Out of the box ESengine takes care only of the Modeling and CRUD operations including:

- Index, DocType and Mapping specification 
- Fields and its types coercion
- basic CRUD operations (Create, Read, Update, Delete)

### Communication
ESengine does not communicate direct with ElasticSearch, it only creates the basic structure, 
to communicate it relies on an ES client providing the transport methods (index, delete, update etc). 

### ES client
ESengine does not enforce the use of the official ElasticSearch client,
but you are encouraged to use it because it is well maintained and has the support to **bulk** operations. Bu you are free to use another client or create your own.

### Querying the data
ESengine does not enforce or encourage you to use a DSL language for queries, out of the box you have to
write the elasticsearch **payload** representation as a raw Python dictionary. However ESEngine comes with a **utils.payload** helper module to help you building payloads in a less verbose way.

### Why not elasticsearch_dsl?

ElasticSearch DSL is an excellent tool, a very nice effort by the maintainers of the official ES library, it is handy in most of the cases, but its DSL objects leads to a confuse query building, sometimes it is better to write raw_queries or use a simpler payload builder having more control and visibility of what os being generated. DSL enforce you to use the official ES client and there are cases when a different client implementation perform better or you need to run tests using a Mock. Also, to make things really easy, all the synrax sugar in DSL can lead in to performance problems.

### Project Stage

It is in beta-Release, working in production, but missing a lot of features, you can help using, testing,, discussing or coding!


# Getting started

## install

ESengine needs a client to communicate with E.S, you can use one of the following:

- ElasticSearch-py (official)
- Py-Elasticsearch (unofficial)
- Create your own implementing the same api-protocol
- Use the MockES provided as py.test fixture (only for tests)

Because of bulk operations you are recommendded to use
**elasticsearch-py** (Official E.S Python library) so the instalation 
depends on the version of elasticsearch you are using.

### Elasticsearch 2.x

```bash
pip install esengine[es2]
```

### Elasticsearch 1.x

```bash
pip install esengine[es1]
```

### Elasticsearch 0.90.x

```bash
pip install esengine[es0]
```

The above command will install esengine and the elasticsearch library specific for you ES version.


> Alternatively you can only install elasticsearch library before esengine

pip install ``<version-specific-es>`` 

- for 2.0 + use "elasticsearch>=2.0.0,<3.0.0"
- for 1.0 + use "elasticsearch>=1.0.0,<2.0.0"
- under 1.0 use "elasticsearch<1.0.0"

Then install esengine

```bash
pip install esengine
```

# Usage

```python
from elasticsearch import ElasticSearch
from esengine import Document, StringField

es = ElasticSearch(host='host', port=port)
```

## Defining a document

```python
class Person(Document):
    _doctype = "person"
    _index = "universe"
    
    name = StringField()
    
```

> If you do not specify an "id" field, ESEngine will automatically add "id" as StringField. It is recommended that when specifying you use StringField for ids.


## Special Fields

### GeoPointField

A field to hold GeoPoint with modes dict|array|string and its mappings

```python
class Obj(Document):
    location = GeoPointField(mode='dict')  # default
    # An object representation with lat and lon explicitly named

Obj.location = {"lat": 40.722, "lon": -73.989}}

class Obj(Document):
    location = GeoPointField(mode='string')
    # A string representation, with "lat,lon"

Obj.location = "40.715, -74.011"

class Obj(Document):
    location = GeoPointField(mode='array')
    # An array representation with [lon,lat].

Obj.location = [-73.983, 40.719]
```

## Indexing

```python
person = Person(id=1234, name="Gonzo")
person.save(es=es)
```

## Getting by id

```python
Person.get(id=1234, es=es)
```

## filtering by IDS

```python
ids = [1234, 5678, 9101]
power_trio = Person.filter(ids=ids)
```


## filtering by fields

```python
Person.filter(name="Gonzo", es=es)
```

## Searching

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
                    "values": [1, 2]
                }
            }
        }
    }
}
Person.search(query, size=10, es=es)
```

## Getting all documents

```python
Person.all(es=es)

# with more arguments

Person.all(size=20, es=es)

```


## Counting

```python
Person.count(name='Gonzo', es=es)
```

## Using a default connection

By default ES engine does not try to implicit create a connection for you, so you have to pass in **es=es** argument.


You can easily achieve this overwriting the **get_es** method and returning a 
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
        
### Now you can use the document transport methods ommiting ES instance


```python
person = Person(id=1234, name="Gonzo")
person.save()
         
Person.get(id=1234)

Person.filter(name="Gonzo")
```


## Updating

###  A single document

A single document can be updated simply using the **.save()** method

```python

person = Person.get(id=1234)
person.name = "Another Name"
person.save()

```

### Updating a Resultset

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


### The use of **reload** method
 
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

### Deleting documents


#### A ResultSet

```python
people = Person.all()
people.delete()
```

#### A single document

```python
Person.get(id=123).delete()
```

## Bulk operations

ESEngine takes advantage of elasticsearch-py helpers for bulk actions, 
the **ResultSet** object uses **bulk** melhod to **update** and **delete** documents.

But you can use it in a explicit way using Document's **update_all**, **save__all** and **delete_all** methods.

#### Lets create a bunch of document instances


```python
top_5_racing_bikers = []

for name in ['Eddy Merckx', 
             'Bernard Hinault', 
             'Jacques Anquetil', 
             'Sean Kelly', 
             'Lance Armstrong']:
     top_5_racing_bikers.append(Person(name=name))
```

#### Save it all 

```python
Person.save_all(top_5_racing_bikers)
```

#### Using the **create** shortcut

The above could be achieved using **create** shortcut


##### A single

```python
Person.create(name='Eddy Merckx', active=False)
```

> Create will return the instance of the indexed Document

##### All using list comprehension

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

#### Updating all

Turning the field **active** to **True** for all documents

```python
Person.update_all(top_5_racing_bikes, active=True)
```

#### Deleting all

```python
Person.delete_all(top_5_racing_bikes)
```


#### Chunck size

chunk_size is number of docs in one chunk sent to ES (default: 500)
you can change using **meta** argument.

```python
Person.update_all(
    top_5_racing_bikes, # the documents
    active=True,  # values to be changed
    metal={'chunk_size': 200}  # meta data passed to **bulk** operation    
)
```

#### Utilities

#### Mapping and Mapping migrations

ESEngine does not saves mappings automatically, but it offers an utility to generate and save mappings on demand
You can create a cron job to refresh mappings once a day or run it every time your model changes

##### Using the document

```python
Person.put_mapping()
```

##### Using Mapping

```python
from esengine.mapping import Mapping
mapping = Mapping(Person, enable_all=False)
print mapping.generate()  # shows mapping payload
mapping.save()  # put mapping
```

> Include above in your cron jobs or migration scripts

#### Validators

##### Field Validator

To validate each field separately you can set a list of validators, each 
validator is a callable receiving field_name and value as arguments and
should return None to be valid. If raise or return the data will be invalidated

```python
from esengine.exceptions import ValidationError

def category_validator(field_name, value):
    # check if value is in valid categories
    if value not in ["primary", "secondary", ...]:
        raise ValidationError("Invalid category!!!")
    
class Obj(Document):
    category = StringField(validators=[category_validator])

obj = Obj()
obj.category = "another"
obj.save()
Traceback: ValidationError(....)

```

##### Document Validator

To validate the whole document you can set a list of validators, each 
validator is a callable receiving the document instance and
should return None to be valid. If raise or return the data will be invalidated

```python
from esengine.exceptions import ValidationError

def if_city_state_is_required(obj):
    if obj.city and not obj.state:
        raise ValidationError("If city is defined you should define state")
        
class Obj(Document):
    _validators = [if_city_state_is_required]
    
    city = StringField()
    state = StringField()

obj = Obj()
obj.city = "Sao Paulo"
obj.save()
Traceback: ValidationError(....)

```

#### Refreshing

Sometimes you need to force indices-shards refresh for testing, you can use

```python
# Will refresh all indices
Document.refresh()
```

# Payload builder

Sometimes queries turns in to complex and verbose data structures, to help you
(use with moderation) you can use Payload utils to build queries.


## Example using a raw query:

```python
query = {
    "query": {
        "filtered": {
            "query": {
                "match_all": {}
            },
            "filter": {
                "ids": {
                    "values": [1, 2]
                }
            }
        }
    }
}

Person.search(query=query, size=10)
```

## Same example using payload utils

```python
from esengine import Payload, Query, Filter
payload = Payload(
    query=Query.filtered(query=Query.match_all(), filter=Filter.ids([1, 2]))
)
Person.search(payload, size=10)
```

> Payload utils exposes Payload, Query, Filter, Aggregate, Suggesters

## chaining

Payload object is chainable so you can do:
```python
payload = Payload(query=query).size(10).sort("field", order="desc")
Document.search(payload) 
# or the equivalent
payload.search(Document)
```

# Contribute

ESEngine is OpenSource! join us!
<a href="http://smallactsmanifesto.org" title="Small Acts Manifesto"><img src="http://smallactsmanifesto.org/static/images/smallacts-badge-80x15-blue.png" style="border: none;" alt="Small Acts Manifesto" /></a>
