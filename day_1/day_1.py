#!/usr/bin/env python

from functools import reduce
from prelude import *

###


def consume(level, paren):
    ops = { '(': 1,
            ')': -1}
    return level + ops[paren]


def levels(ops):
    return list(scan(consume, ops, 0))


def lastFloor(ops):
    """
    >>> lastFloor('(()(()(')
    3
    >>> lastFloor(')())())')
    -3
    """
    return reduce(consume, ops, 0)


def enteringBasement(ops):
    """
    >>> enteringBasement('()())')
    5
    """
    return levels(ops).index(-1)



def correct():
    """
    >> lastFloor(ops)
    232
    >> enteringBasement(ops)
    1783
    """
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    with open('input.txt', 'r') as f:
        ops = f.read()
        print('final floor:', lastFloor(ops))
        print('entering basement:', enteringBasement(ops))

