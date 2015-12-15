#!/usr/bin/env python

"""
(c) Johannes Ahlmann, 2015-12, licensed CC0
"""

import doctest
from functools import reduce
import prelude as p

def consume(level, paren):
    """
    >>> consume(0, '(')
    1
    """
    ops = {'(': 1,
           ')': -1}
    return level + ops[paren]

def last_floor(ops):
    """
    >>> last_floor('(()(()(')
    3
    >>> last_floor(')())())')
    -3
    """
    return reduce(consume, ops, 0)

def entering_basement(ops):
    """
    >>> entering_basement('()())')
    5
    """
    levels = p.scan(consume, ops, 0)
    return p.iindex(levels, -1)

def correct():
    """
    >> last_floor(ops)
    232
    >> entering_basement(ops)
    1783
    """
    pass

if __name__ == "__main__":
    doctest.testmod()

    with open('input.txt', 'r') as f:
        OPS = f.read()
        print('final floor:', last_floor(OPS))
        print('entering basement:', entering_basement(OPS))

