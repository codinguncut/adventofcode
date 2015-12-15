#!/usr/bin/env python

"""
(c) Johannes Ahlmann, 2015-12, licensed CC0
"""

import doctest
import itertools as it
import operator
import prelude as p

def is_max(seq):
    """
    >>> is_max((1,2,3,2,3))
    [0, 0, 1, 0, 1]
    """
    maxi = max(seq)
    return [int(x == maxi) for x in seq]

def enqueue(reindeer):
    """
    >>> list(p.take(6, enqueue(('Vixen', 8, 2, 2))))
    [8, 16, 16, 16, 24, 32]
    """
    _, speed, running, resting = reindeer
    one_cycle = it.chain(it.repeat(speed, running), it.repeat(0, resting))
    return p.drop(1, p.scan(operator.add, it.cycle(one_cycle), 0))

def accum(reindeers, num):
    """
    >>> rds = [('Comet', 14, 10, 127), ('Dancer', 16, 11, 162)]
    >>> list(accum(rds, 1000))
    [312, 689]
    """
    queues = [enqueue(r) for r in reindeers]
    winners = (is_max(x) for x in zip(*queues))
    scores = p.scan(lambda s, x: map(sum, zip(s, x)), winners, it.repeat(0))
    return p.nth(num+1, scores)

def run(reindeers, num):
    """
    >>> rds = [('Comet', 14, 10, 127), ('Dancer', 16, 11, 162)]
    >>> list(run(rds, 1000))
    [1120, 1056]
    """
    queues = [enqueue(r) for r in reindeers]
    distances = zip(*queues)
    return p.nth(num+1, distances)

REINDEERS = [
    ('Vixen', 8, 8, 53),
    ('Blitzen', 13, 4, 49),
    ('Rudolph', 20, 7, 132),
    ('Cupid', 12, 4, 43),
    ('Donner', 9, 5, 38),
    ('Dasher', 10, 4, 37),
    ('Comet', 3, 37, 76),
    ('Prancer', 9, 12, 97),
    ('Dancer', 37, 1, 36)
    ]

if __name__ == "__main__":
    doctest.testmod()

    print('part 1:', max(run(REINDEERS, 2503)))
    print('part 2:', max(accum(REINDEERS, 2503)))

