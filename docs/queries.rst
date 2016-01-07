Queries
=======

Note that all Query calls can also be passed additional keyword arguments not specified here, but no validation of inputs is done on them.




Query.span_or
~~~~~~~~~~~~~

.. code:: python

    Query.span_or([Query])


Query.terms
~~~~~~~~~~~

.. code:: python

    Query.terms(field, [value])


Query.has_child
~~~~~~~~~~~~~~~

.. code:: python

    Query.has_child(type, filter=Filter, query=Query)


Query.span_first
~~~~~~~~~~~~~~~~

.. code:: python

    Query.span_first(Query)


Query.prefix
~~~~~~~~~~~~

.. code:: python

    Query.prefix(field, value, boost=None)


Query.term
~~~~~~~~~~

.. code:: python

    Query.term(field, value, boost=None)


Query.fuzzy
~~~~~~~~~~~

.. code:: python

    Query.fuzzy(field, value, boost=None, fuzziness=None, prefix_length=None, max_expansions=None)


Query.nested
~~~~~~~~~~~~

.. code:: python

    Query.nested(path, Query)


Query.dis_max
~~~~~~~~~~~~~

.. code:: python

    Query.dis_max([Query])


Query.query_string
~~~~~~~~~~~~~~~~~~

.. code:: python

    Query.query_string(query, fields=[])


Query.fuzzy_like_this
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Query.fuzzy_like_this([fields], like_text)


Query.has_parent
~~~~~~~~~~~~~~~~

.. code:: python

    Query.has_parent(parent_type, filter=Filter, query=Query)


Query.function_score
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Query.function_score([functions], filter=Filter, query=Query)


Query.geo_shape
~~~~~~~~~~~~~~~

.. code:: python

    Query.geo_shape(field, type=None, coordinates=[])


Query.fuzzy_like_this_field
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Query.fuzzy_like_this_field(field, like_text, max_query_terms=None, ignore_tf=None, fuzziness=None, prefix_length=None, boost=None, analyzer=None)


Query.span_multi
~~~~~~~~~~~~~~~~

.. code:: python

    Query.span_multi(Query)


Query.match_all
~~~~~~~~~~~~~~~

.. code:: python

    Query.match_all(boost=None)


Query.span_near
~~~~~~~~~~~~~~~

.. code:: python

    Query.span_near([Query])


Query.simple_query_string
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Query.simple_query_string(query, fields=[])


Query.multi_match
~~~~~~~~~~~~~~~~~

.. code:: python

    Query.multi_match([fields], query)


Query.span_term
~~~~~~~~~~~~~~~

.. code:: python

    Query.span_term(field, value, boost=None)


Query.regexp
~~~~~~~~~~~~

.. code:: python

    Query.regexp(field, value, boost=None, flags=None)


Query.ids
~~~~~~~~~

.. code:: python

    Query.ids([values], type=None)


Query.more_like_this
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Query.more_like_this([fields], like_text)


Query.range
~~~~~~~~~~~

.. code:: python

    Query.range(field, gte=None, gt=None, lte=None, lt=None)


Query.bool
~~~~~~~~~~

.. code:: python

    Query.bool(must=[Query], must_not=[Query], should=[Query])


Query.common
~~~~~~~~~~~~

.. code:: python

    Query.common(query)


Query.wildcard
~~~~~~~~~~~~~~

.. code:: python

    Query.wildcard(field, value, boost=None)


Query.indices
~~~~~~~~~~~~~

.. code:: python

    Query.indices([indices], query=Query, no_match_query=Query)


Query.filtered
~~~~~~~~~~~~~~

.. code:: python

    Query.filtered(filter=Filter, query=Query)


Query.span_not
~~~~~~~~~~~~~~

.. code:: python

    Query.span_not(include=Query, exclude=Query)


Query.boost
~~~~~~~~~~~

.. code:: python

    Query.boost(positive=None, negative=None)


Query.constant_score
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Query.constant_score(filter=Filter, query=Query)


Query.match
~~~~~~~~~~~

.. code:: python

    Query.match(field, query, operator=None, zero_terms_query=None, cutoff_frequency=None, boost=None)


Query.top_children
~~~~~~~~~~~~~~~~~~

.. code:: python

    Query.top_children(type, query=Query)

