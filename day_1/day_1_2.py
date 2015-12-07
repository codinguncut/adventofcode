#!/usr/bin/env python

import sys

def scan(f, it, state):
  yield state 
  for x in it:
    state = f(state, x)
    yield state


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
    return levels(ops)[-1]


def enteringBasement(ops):
    """
    >>> enteringBasement('()())')
    5
    """
    return levels(ops).index(-1)


ops = sys.stdin.read().strip()
print 'final floor:', lastFloor(ops), ', entering basement:', enteringBasement(ops)


def correct():
    """
    >>> lastFloor(ops)
    232
    >>> enteringBasement(ops)
    1783
    """
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()

