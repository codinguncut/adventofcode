#!/usr/bin/env python

import itertools as it
from multiprocessing import Pool
import operator
import functools as ft


def take(n, xs):
    """
    >>> list(take(5, it.count(1)))
    [1, 2, 3, 4, 5]
    """
    return it.islice(xs, n)


def drop(n, xs):
    """
    >>> list(drop(5, range(1, 8)))
    [6, 7]
    """
    return it.islice(xs, n, None)


def tail(xs):
    return it.islice(xs, 1, None)


def nth(n, xs):
    """
    >>> nth(5, it.count(1))
    5
    """
    return next(drop(n-1, xs))


def scan(f, it, state):
    """
    >>> list(scan(lambda x,y: x+y, [1,2,3], 0))
    [0, 1, 3, 6]
    """
    yield state
    for x in it:
        state = f(state, x)
        yield state


def ilen(xs):
    """
    >>> ilen(range(5))
    5
    """
    return sum(1 for _ in xs)


def iterate(f, x):
    """
    >>> list(take(5, iterate(lambda x: x*2, 1)))
    [1, 2, 4, 8, 16]
    """
    s = x
    while True:
        yield s
        s = f(s)


def concat(xs):
    """
    >>> concat([[1, 2], [3, 4]])
    [1, 2, 3, 4]
    """
    return sum(xs, [])


def const(x):
    """
    >>> const(42)(113123)
    42
    """
    return lambda _: x


"""
fold*, unfold
sequence
span
groupBy
List.tails, inits
intersperse
transpose
takeWhile
unzip, zipWith
curry, uncurry
"""

###


# TODO: Pool.imap would be infinitely more elegant,
#   but unfortunately it is very broken ;(
def imap(func, iterable, chunksize=10000):
    """
    >>> list(take(5, imap(ft.partial(operator.add, 1), range(5))))
    [1, 2, 3, 4, 5]
    """
    pool = Pool()

    # had trouble using it.chain with infinite iterable ;(
    def chain(gss):
        for gs in gss:
            for g in gs:
                yield g

    def helper():
        while True:
            seg = it.islice(iterable, chunksize)
            # TODO: abort loop when iterable is exhausted
            yield pool.map(func, seg)

    return chain(helper())


if __name__ == "__main__":
    import doctest
    doctest.testmod()
