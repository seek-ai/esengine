Payload
===================

The main ``Payload`` class allows you to build Elasticsearch queries

.. code:: python

    from eengine import Payload, Query, Aggregate

    # Create a new payload
    p = payload()

    # Match something
    p.query(Query.match('some_field', 'some_text'))

    # Aggregate something
    p.aggregate(Aggregate.terms('my_terms', 'some_field'))


API
---

.. automodule:: esengine.utils.payload.base
    :members:
    :undoc-members:


Exceptions
----------

.. automodule:: esengine.utils.payload.exception
    :members:
    :undoc-members:
