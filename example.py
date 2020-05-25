# coding: utf-8

import time
import datetime
from elasticsearch import Elasticsearch
from esengine import (
    Document, KeywordField, IntegerField, BooleanField,
    FloatField, GeoPointField, DateField
)


class ExampleDoc(Document):
    _index = 'esengine_test'
    _doctype = 'example'
    _es = Elasticsearch()

    name = KeywordField()
    age = IntegerField()
    active = BooleanField()
    weight = FloatField()
    location = GeoPointField(mode="array")
    birthday = DateField(date_format="%Y-%m-%d")
    city = KeywordField()


ExampleDoc.put_mapping()

########################################################################
instances = []
gonzo = ExampleDoc(
    id=123456,
    name="Gonzo",
    age="2",
    active=True,
    weight="30.5",
    location=[0.345, 1.456],
    city="Tunguska"
)
gonzo.birthday = '2015-01-01'
gonzo.save()
instances.append(gonzo)


mongo = ExampleDoc(
    id=789100,
    name="Mongo",
    age="3",
    active=False,
    weight="10.5",
    location=[0.342, 2.456],
    birthday=datetime.datetime.today(),
    city="Tunguska"
)
mongo.save()
instances.append(mongo)



########################################################################

for instance in instances:
    print instance

    print "get by id=", instance.id, ExampleDoc.get(id=instance.id)

    print "Filter by name=", instance.name, [
        item.to_dict() for item in ExampleDoc.filter(name=instance.name, size=2)
    ]

    print "Filter by name='" + instance.name + "', active=", instance.active, [
        item.to_dict()
        for item in ExampleDoc.filter(name="Gonzo", active=instance.active, size=2)
    ]

    QUERY = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"name": instance.name}}
                ]
            }
        }
    }

    print "Search by query:", QUERY, [
        item.to_dict()
        for item in ExampleDoc.search(QUERY)
    ]
    print "#" * 120


for instance in instances:
    print instance.name, "Old age:", instance.age
    instance.age += 1
    print instance.name, "New age:", instance.age

ExampleDoc.save_all(instances)

for instance in instances:
    print instance.name, "Saved age is now:", instance.age

for instance in instances:
    print "{i.name} activation is {i.active}".format(i=instance)

########################################################################

time.sleep(2)

print "updating turning activations to True"

QUERY = {
    "query": {
        "bool": {
            "must": [
                {"match": {"city": "Tunguska"}}
            ]
        }
    }
}

print "for", QUERY

results = ExampleDoc.search(QUERY)
for res in results:
    print res


results.update(active=True)
results.reload()
for res in results:
    print "{i.name} activation is {i.active}".format(i=res)

print "Will update the names to Jonson"

# results.update(name="Jonson")
# results.reload()
# for res in results:
#     print "{i.name} activation is {i.active}".format(i=res)

# print "Updating using Model.update_all"
# ExampleDoc.update_all(results, city="Itapopoca")
# time.sleep(1)
# results = ExampleDoc.filter(city="Itapopoca")
# for res in results:
#     print "{i.name} city is {i.city}".format(i=res)

print "All documents"
for doc in ExampleDoc.all():
    print doc.to_dict()

#print "Deleting everything"
#results.delete()
