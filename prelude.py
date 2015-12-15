#!/usr/bin/env python

"""
Python functional tools inspired by Haskell Prelude.
Also compare "https://docs.python.org/3/library/itertools.html#itertools-recipes"
"""

import doctest
import itertools as it
import operator
from multiprocessing import Pool
import functools as ft

def take(num, seq):
    """
    >>> list(take(5, it.count(1)))
    [1, 2, 3, 4, 5]
    """
    return it.islice(seq, num)

def drop(num, seq):
    """
    >>> list(drop(5, range(1, 8)))
    [6, 7]
    """
    return it.islice(seq, num, None)

def tail(seq):
    """
    >>> list(tail(range(5)))
    [1, 2, 3, 4]
    """
    return it.islice(seq, 1, None)

def nth(num, seq):
    """
    >>> nth(5, it.count(1))
    5
    """
    return next(drop(num-1, seq))

def last(seq):
    """
    >>> last(range(5))
    4
    """
    return ft.reduce(lambda _, x: x, seq)

def product(seq):
    """
    >>> product(range(1, 5))
    24
    """
    return ft.reduce(operator.mul, seq, 1)

def scan(func, seq, state):
    """
    >>> list(scan(lambda x,y: x+y, [1,2,3], 0))
    [0, 1, 3, 6]
    """
    yield state
    for elt in seq:
        state = func(state, elt)
        yield state

def ilen(seq):
    """
    >>> ilen(range(5))
    5
    """
    return sum(1 for _ in seq)

def iterate(func, init_state):
    """
    >>> list(take(5, iterate(lambda x: x*2, 1)))
    [1, 2, 4, 8, 16]
    """
    state = init_state
    yield state
    while True:
        state = func(state)
        yield state

def concat(seq):
    """
    >>> concat([[1, 2], [3, 4]])
    [1, 2, 3, 4]
    """
    return sum(seq, [])

def const(val):
    """
    >>> const(42)(113123)
    42
    """
    return lambda _: val

def zipwith(func, *parts):
    """
    >>> list(zipwith(operator.add, [1,2,3], [4,5,6]))
    [5, 7, 9]
    """
    return (func(*x) for x in zip(*parts))

def iindex(iterable, search_elt):
    """
    >>> iindex(range(10), 8)
    8
    """
    for i, elt in enumerate(iterable):
        if elt == search_elt:
            return i
    return -1

"""
fold*, unfold
sequence
span
List.tails, inits
intersperse
transpose
curry, uncurry
pairwise
"""

###

# source: http://stackoverflow.com/questions/24527006
def chunks(iterable, size):
    """
    >>> [list(c) for c in chunks(range(10), 3)]
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    iterator = iter(iterable)
    for first in iterator:
        yield it.chain([first], it.islice(iterator, size - 1))

def parfilter(pred, iterable, chunksize=10000):
    """
    pred has to be a picklable function (i.e. globally defined non-closure)
    >>> list(parfilter(ft.partial(operator.lt, 3), range(10)))
    [4, 5, 6, 7, 8, 9]
    """
    it1, it2 = it.tee(iterable)
    return (x for x, y in zip(it1, parmap(pred, it2, chunksize)) if y)

# NOTE: Pool.imap would be more elegant, but unfortunately it is very broken ;(
def parmap(func, iterable, chunksize=10000):
    """
    >>> list(parmap(ft.partial(operator.add, 1), range(5)))
    [1, 2, 3, 4, 5]
    """
    pool = Pool()

    def helper():
        for chunk in chunks(iterable, chunksize):
            yield pool.map(func, chunk)

    return it.chain.from_iterable(helper())

if __name__ == "__main__":
    doctest.testmod()
