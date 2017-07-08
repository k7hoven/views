`views`` -- efficient tools for generators and sequences
========================================================

The ``views`` module provides additions to the existing python comprehensions and generator expressions. (Chained) sequence views can be made using ``seq`` and generators can be chained with `gen`, as shown in the examples below.

Any feedback or suggestions are very welcome: koos.zevenhoven@aalto.fi.

Getting Started
===============

Requirements
------------

* Python 3.6

Installation
------------

The package can be installed with ``pip`` (make sure you have it installed):

.. code-block:: bash

    pip3 install git+http://github.com/k7hoven/coils

Or if your default python is Python 3:

.. code-block:: bash

    pip install git+http://github.com/k7hoven/coils


Basic Usage
===========

Basic introductory examples here, but they should get you started.

Sequence view comprehension syntax: resulting objects support slicing and indexing.
 
Example:

.. code-block:: python
   >>> from views import seq
   >>> seq[::range(3), None, ::"abc", "Hi!"]
   <sequence view 8: [0, 1, 2, None, 'a', 'b', 'c', 'Hi!'] >
   >>> seq[::range(100)]
   <sequence view 100: [0, 1, 2, 3, 4, ..., 96, 97, 98, 99]


Generator comprehension syntax.

Example:

.. code-block:: python
    >>> list(gen[::range(3), 3, 4, ::range(5,7), 7])
    [0, 1, 2, 3, 4, 5, 6, 7


Have fun!
