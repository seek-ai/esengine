Filters
=======

Note that all Filter calls can also be passed additional keyword arguments not specified here, but no validation of inputs is done on them.




Filter.geohash_shell
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Filter.geohash_shell(field, lat=None, lon=None)


Filter.geo_polygon
~~~~~~~~~~~~~~~~~~

.. code:: python

    Filter.geo_polygon(field, [points])


Filter.exists
~~~~~~~~~~~~~

.. code:: python

    Filter.exists(field)


Filter.not\_
~~~~~~~~~~~~

.. code:: python

    Filter.not_(filter=Filter, query=Query)


Filter.nested
~~~~~~~~~~~~~

.. code:: python

    Filter.nested(path, Filter)


Filter.prefix
~~~~~~~~~~~~~

.. code:: python

    Filter.prefix(field, value)


Filter.has_parent
~~~~~~~~~~~~~~~~~

.. code:: python

    Filter.has_parent(parent_type, filter=Filter, query=Query)


Filter.geo_distance_range
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Filter.geo_distance_range(field, lat=None, lon=None)


Filter.script
~~~~~~~~~~~~~

.. code:: python

    Filter.script(script)


Filter.bool
~~~~~~~~~~~

.. code:: python

    Filter.bool(must=[Filter], must_not=[Filter], should=[Filter])


Filter.type
~~~~~~~~~~~

.. code:: python

    Filter.type(value)


Filter.terms
~~~~~~~~~~~~

.. code:: python

    Filter.terms(field, [value])


Filter.has_child
~~~~~~~~~~~~~~~~

.. code:: python

    Filter.has_child(type, filter=Filter, query=Query)


Filter.missing
~~~~~~~~~~~~~~

.. code:: python

    Filter.missing(field)


Filter.term
~~~~~~~~~~~

.. code:: python

    Filter.term(field, value)


Filter.geo_shape
~~~~~~~~~~~~~~~~

.. code:: python

    Filter.geo_shape(field, type=None, coordinates=[])


Filter.regexp
~~~~~~~~~~~~~

.. code:: python

    Filter.regexp(field, value, flags=None, max_determinized_states=None)


Filter.or\_
~~~~~~~~~~~

.. code:: python

    Filter.or_([Filter])


Filter.match_all
~~~~~~~~~~~~~~~~

.. code:: python

    Filter.match_all(None)


Filter.geo_distance
~~~~~~~~~~~~~~~~~~~

.. code:: python

    Filter.geo_distance(field, lat=None, lon=None)


Filter.geo_bounding_box
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Filter.geo_bounding_box(field, top_left=None, bottom_right=None)


Filter.and\_
~~~~~~~~~~~~

.. code:: python

    Filter.and_([Filter])


Filter.ids
~~~~~~~~~~

.. code:: python

    Filter.ids([values], type=None)


Filter.range
~~~~~~~~~~~~

.. code:: python

    Filter.range(field, gte=None, gt=None, lte=None, lt=None)


Filter.limit
~~~~~~~~~~~~

.. code:: python

    Filter.limit(value)


Filter.indices
~~~~~~~~~~~~~~

.. code:: python

    Filter.indices([indices], filter=Filter, no_match_filter=Filter)

