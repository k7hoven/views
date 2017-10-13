``views`` -- efficient tools for generators and sequences
=========================================================

The ``views`` module provides additions to the existing python comprehensions and generator expressions. (Chained) sequence views can be made using ``seq`` and generators can be chained with ``gen``, as shown in the examples below.

Any feedback or suggestions are very welcome.

- Email: koos.zevenhoven@aalto.fi
- Twitter: `@k7hoven <https://twitter.com/k7hoven>`_


Getting Started
===============

Requirements
------------

* Python 3.6+

Installation
------------

The package can be installed with ``pip`` (make sure you have it installed):

.. code-block:: bash

    pip3 install git+http://github.com/k7hoven/views

Or if your default python is Python 3:

.. code-block:: bash

    pip install git+http://github.com/k7hoven/views


Basic Usage
-----------

Basic introductory examples here, but they should get you started.

Sequence view comprehension syntax
''''''''''''''''''''''''''''''''''

You can change chain single objects and sequences into one sequence view. Use ``::`` just like you would use ``*`` in tuple (un)packing. The resulting object supports slicing and indexing.
 
Example:

.. code-block:: python

   >>> from views import seq
   >>> seq[::range(3), None, ::"abc", "Hi!"]
   <sequence view 8: [0, 1, 2, None, 'a', 'b', 'c', 'Hi!'] >
   >>> seq[::range(100)]
   <sequence view 100: [0, 1, 2, 3, 4, ..., 96, 97, 98, 99] >


Generator comprehension syntax
''''''''''''''''''''''''''''''

Use like ``seq``. The resulting object is a generator.

Example:

.. code-block:: python

    >>> from views import gen
    >>> list(gen[::range(3), 3, 4, ::range(5,7), 7])
    [0, 1, 2, 3, 4, 5, 6, 7]


Chaining sequences and generators/iterables
'''''''''''''''''''''''''''''''''''''''''''

You can chain an arbitrary number of sequences with ``seq.chain(*sequences)`` and of generators with ``gen.chain(*iterables)``. The latter is equivalent to ``itertools.chain(*iterables)``.

Example:

.. code-block:: python

   >>> from views import seq, gen
   >>> seq.chain([1, 2, 3], [4, 5, 6])
   <sequence view 6: [1, 2, 3, 4, 5, 6] >
   >>> list(gen.chain([1, 2, 3], [4, 5, 6]))
   [1, 2, 3, 4, 5, 6]


Improved ``range`` objects
''''''''''''''''''''''''''

For a more capable and understandable replacement for the builtin ``range``, you can use ``views.range``, which takes any arguments the builtin function takes, or alternatively a ``first, second, ..., last[, step=step]`` argument list. Also the ``repr`` uses the more learning-friendly variant.

Examples:

.. code-block:: python

    >>> from views import range
    >>> range(5)
    range(0, ..., 4)
    >>> range(1, 10, 3)
    range(1, ..., 7, step=3)
    >>> range(1, ..., 5)
    range(1, ..., 5)
    >>> range(1, 3, ..., 10)
    range(1, ..., 9, step=2)
    >>> range(2, ..., 15, step=3)
    range(2, ..., 14, step=3)
    >>> range(9, ..., 4, step=-1)
    range(9, ..., 4, step=-1)
    

Have fun!
