Changelog
=========

0.4.0 (2017)
------------

- Add enhanced range with standard ``range`` functionality and extras: ``range(first, ..., last)``, ``range(first, second, ..., last)`` and ``range(first, ..., last, step=step)``. The ``repr`` is always given using ``...``. 


0.3.0 (2017-10-10)
------------------

- Add ``seq.chain(*sequences)`` and ``gen.chain(*iterables)``
- Some speed optimizations, especially to ``seq``.

0.2.0 (2017-09-11)
------------------

- LengthChangedError is now a subclass of ``RuntimeError``.
- Minor optimizations to ``seq`` and ``gen``.

0.1.0 (2017-06-06)
------------------

- First version
