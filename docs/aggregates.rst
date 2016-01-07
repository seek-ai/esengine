Aggregates
==========

Note that all Aggregate calls can also be passed additional keyword arguments not specified here, but no validation of inputs is done on them.




Aggregate.geo_bounds
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.geo_bounds(name, field)


Aggregate.date_histogram
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.date_histogram(name, field, interval)


Aggregate.global
~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.global(name)


Aggregate.nested
~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.nested(name, path)


Aggregate.ip_range
~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.ip_range(name, field, [ranges])


Aggregate.filters
~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.filters(name, [Filter])


Aggregate.avg
~~~~~~~~~~~~~

.. code:: python

    Aggregate.avg(name, field)


Aggregate.children
~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.children(name, type)


Aggregate.stats
~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.stats(name, field)


Aggregate.scripted_metric
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.scripted_metric(name)


Aggregate.min
~~~~~~~~~~~~~

.. code:: python

    Aggregate.min(name, field)


Aggregate.sum
~~~~~~~~~~~~~

.. code:: python

    Aggregate.sum(name, field)


Aggregate.extended_stats
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.extended_stats(name, field)


Aggregate.value_count
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.value_count(name, field)


Aggregate.percentiles
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.percentiles(name, field)


Aggregate.terms
~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.terms(name, field)


Aggregate.missing
~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.missing(name, field)


Aggregate.max
~~~~~~~~~~~~~

.. code:: python

    Aggregate.max(name, field)


Aggregate.histogram
~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.histogram(name, field, interval)


Aggregate.date_range
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.date_range(name, field, [ranges])


Aggregate.cardinality
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.cardinality(name, field)


Aggregate.geohash_grid
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.geohash_grid(name, field)


Aggregate.geo_distance
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.geo_distance(name, field, origin, [ranges])


Aggregate.filter
~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.filter(name, Filter)


Aggregate.percentile_ranks
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.percentile_ranks(name, field)


Aggregate.range
~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.range(name, field, [ranges])


Aggregate.significant_terms
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.significant_terms(name, field)


Aggregate.top_hits
~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.top_hits(name)


Aggregate.reverse_nested
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Aggregate.reverse_nested(name)

