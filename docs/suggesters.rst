Suggesters
==========

Note that all Suggester calls can also be passed additional keyword arguments not specified here, but no validation of inputs is done on them.




Suggester.completion
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Suggester.completion(field, size=None)


Suggester.phrase
~~~~~~~~~~~~~~~~

.. code:: python

    Suggester.phrase(field, gram_size=None, real_word_error_likelihood=None, confidence=None, max_errors=None, separator=None, size=None, analyzer=None, shard_size=None, collate=None)


Suggester.term
~~~~~~~~~~~~~~

.. code:: python

    Suggester.term(field, analyzer=None, size=None, sort=None, suggest_mode=None)

