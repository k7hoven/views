# -*- coding: utf-8 -*-
"""
Copyright (C) Koos Zevenhoven. 

See LICENSE.txt at http://github.com/k7hoven/views for license information.

@author: Koos Zevenhoven
"""

__all__ = ['gen', 'seq']

def make(callable):
    return callable()
        
@make
class gen:
    """Generator comprehension syntax.

    Example:

    >>> list(gen[::range(3), 3, 4, ::range(5,7), 7])
    [0, 1, 2, 3, 4, 5, 6, 7]

    """

    def __getitem__(self, args):
        if not isinstance(args, tuple):
            args = args,

        @tuple
        @make
        def parts():
            part = []
            for obj in args:
                if isinstance(obj, slice):
                    if obj.start is None and obj.stop is None:
                        obj = obj.step
                        objtype = type(obj)
                        if hasattr(objtype, '__iter__'):
                            obj = iter(obj)
                        if not hasattr(type(obj), '__next__'):
                            raise TypeError(
                                f"'{objtype.__name__}' object is not "
                                "iterable and cannot be chained"
                            )
                        if part:
                            yield part
                            part = []
                        yield obj
                    else:
                        raise SyntaxError(
                            'invalid syntax in generator comprehension'
                        )
                else:
                    part.append(obj)
            if part:
                yield part

        return self.chain(*parts)
    
    @staticmethod
    def chain(*parts):
        for part in parts:
            yield from part
    chain.__qualname__ = '<views.gen>'


class LengthChangedError(RuntimeError):
    pass

def issequence(obj):
    otype = type(obj)
    return hasattr(otype, '__getitem__') and hasattr(otype, '__len__')

class Repr(str):
    def __repr__(self):
        return self

class SeqMixin:
    REPR_ITEMS = 10
    REPR_SPLIT = 5, 4
    def __repr__(self):
        template = f"<sequence view {len(self)}:" " {} >"
        if len(self) <= self.REPR_ITEMS:
            return template.format(repr([*self]))
        return template.format(
            repr([*self[:self.REPR_SPLIT[0]],
                  Repr("..."),
                  *self[-self.REPR_SPLIT[1]:]])
        )

class Seq(SeqMixin):
    def __init__(self, seq, start=None, stop=None, step=None):
        if not issequence(seq):
            raise TypeError(
                f"'{type(seq).__name__}' object is not a sequence"
            )
        self._seq = seq
        self._len_orig = len(seq)
        self._slice = slice(*slice(start, stop, step).indices(len(seq)))
        self._len = len(range(self._len_orig)[self._slice])

    @property
    def deps(self):
        return self._seq,

    def __len__(self):
        return self._len

    def __getitem__(self, subscript):
        if isinstance(subscript, tuple):
            raise TypeError("multi-indices not supperted")

        if len(self._seq) != self._len_orig:
            raise LengthChangedError(
                "length of underlying sequence has changed"
            )

        if isinstance(subscript, slice):
            idx = subscript.indices(len(self))
            start = self._slice.start + idx[0] * self._slice.step
            stop = start + self._slice.step * (idx[1] - idx[0])
            step = self._slice.step * idx[2]
            return SeqView(self._seq, start, stop, step)

        try:
            subscript.__index__
        except AttributeError:
            raise TypeError(
                "index must be an integer, a slice or have an __index__ method"
            ) from None
            
        subscript = subscript.__index__()
        if subscript < 0:
            subscript = self._len + subscript
        if subscript < 0 or subscript >= self._len:
            raise IndexError("index out of range")

        return self._seq[self._slice.start + subscript * self._slice.step]


class SeqChain(SeqMixin):
    def __init__(self, *parts):
        _len = 0
        for p in parts:
            if not issequence(p):
                raise TypeError(
                    f"'{type(p).__name__}' object is not a sequence"
                )
            _len += len(p)
        self._parts = parts
        self._len = _len

    @property
    def deps(self):
        return self._parts
    
    def __len__(self):
        return self._len

    def _find_position(self, index):
        start = 0
        if index < 0 or index >= self._len:
            return None
        for i, p in enumerate(self._parts):
            newstart = start + len(p)
            if start <= index < newstart:
                ret = (i, index - start)
            start = newstart
        if not start == self._len:
            raise LengthChangedError(
                "length of one of chained sequences has changed"
            )
        return ret
        
    def __getitem__(self, subscript):
        if isinstance(subscript, tuple):
            raise TypeError("multi-indices not supperted")
        
        if isinstance(subscript, slice):
            # Memory use could be optimized further by making a smarter
            # slice which does not hold references to unused parts
            return Seq(self, subscript.start, subscript.stop, subscript.step)
    
        try:
            subscript.__index__
        except AttributeError:
            raise TypeError(
                "index must be an integer, a slice or have an __index__ method"
            ) from None
        
        pos = self._find_position(subscript.__index__())
        if pos is None:
            raise IndexError("sequence index out of bounds")
        return self._parts[pos[0]][pos[1]]
        

@make
class seq:
    """Sequence view comprehension syntax.

    Resulting objects support slicing and indexing.

    Examples:

    >>> seq[::range(3), None, ::"abc", "Hi!"]
    <sequence view 8: [0, 1, 2, None, 'a', 'b', 'c', 'Hi!'] >

    >>> seq[::range(100)]
    <sequence view 100: [0, 1, 2, 3, 4, ..., 96, 97, 98, 99] >

    """

    def __getitem__(self, args):
        if not isinstance(args, tuple):
            args = args,
        
        @tuple
        @make
        def parts():
            part = []
            for obj in args:
                if isinstance(obj, slice):
                    if obj.start is None and obj.stop is None:
                        obj = obj.step
                        if not issequence(obj):
                            raise TypeError(
                                f"'{type(obj).__name__}' object is not "
                                "a sequence and cannot be chained"
                            )
                        if part:
                            yield part
                            part = []
                        yield obj
                    else:
                        raise SyntaxError(
                            'Invalid syntax in chain generator expression'
                        )
                else:
                    part.append(obj)
            if part:
                yield part

        return SeqChain(*parts)

    chain = staticmethod(SeqChain)

_range = range

class range:
    def __new__(cls, *args, **kwargs):
        if ... not in args:
            return cls._from_std_range(_range(*args, **kwargs))
        
        start = args[0]
        ind = args.index(...)
        if ind == 1:
            if len(args) != 3:
                if len(args) > 3:
                    raise TypeError(
                        "too many arguments to " 
                        "range(first, ..., last [, step=step])"
                    )
                elif len(args) < 3:
                    raise TypeError(
                        "missing last value for "
                        "range(first, ..., last[, step=step])"
                    )
            step = kwargs.pop('step', 1)
            last = args[2]
        elif ind == 2:
            if len(args) != 4:
                if len(args) > 4:
                    raise TypeError(
                        "too many arguments to "
                        "range(first, second, ..., last)"
                    )
                elif len(args) < 4:
                    raise TypeError(
                        "missing last value for "
                        "range(first, second, ..., last)"
                    )
            step = args[1] - start
            last = args[3]

            if 'step' in kwargs:
                if kwargs['step'] == step:
                    raise TypeError("redundant 'step' argument")
                else:
                    raise TypeError("conflicting 'step' argument")
        elif ind == 0:
            raise TypeError("missing first value for range(first, ..., last)")
        elif ind > 2:
            raise TypeError("misplaced ellipsis (...)")
        else:
            assert False  # Should never get here

        if step > 0:
            stop = last + 1
            if stop < start:
                raise ValueError(
                    "expected negative step for {}, ..., {}"
                        .format(start, last)
                )
                
        else:
            stop = last - 1
            if stop > start:
                raise ValueError(
                    "expected positive step for {}, ..., {}"
                        .format(start, last)
                )

        if kwargs:
            raise TypeError(
                "unexpected keyword argument(s): {}"\
                    .format(", ".join(kwargs.keys()))
            )

        return cls._from_std_range(_range(start, stop, step))

    @classmethod
    def _from_std_range(cls, rng):
        new = object.__new__(cls)
        new._range = rng
        return new

    def __repr__(self):
        template = "range({}, ..., {}{})" 
        if self._range.step == 1:
            stepstr = ""
        else:
            stepstr = ", step={}".format(self._range.step)
        try:
            return template.format(self[0], self[-1], stepstr)
        except IndexError:
            return repr(self._range)

    @property
    def start(self):
        return self._range.start
    
    @property
    def stop(self):
        return self._range.stop

    @property
    def step(self):
        return self._range.step

from types import MethodType as _MethodType
import functools as _functools

def _inject_range_methods():
    _dont_copy = ['__getattribute__', '__init__'] + list(vars(range))
    
    def make_range_method(function):
        @_functools.wraps(function)
        def method(self, *args, **kwargs):
            ret = function(self._range, *args, **kwargs)
            if type(ret) is _range:
                return range._from_std_range(ret)
            return ret
    
        return method
    
    for name, function in vars(_range).items():
        if hasattr(function, '__call__') and name not in _dont_copy:
            setattr(range, name, make_range_method(function))

_inject_range_methods()
