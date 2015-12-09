#!/usr/bin/env python

"""
lots of optimization possible:
- use proper graph library (shortest path, travelling salesman)
- split into and cache/memoize subpaths (i.e. of length 2^n)
- only calculate paths where p[0] < p[-1], and use reverse for inverse path
- operate on one-hot int encoding rather than full string (faster hash?)
"""

import re
import itertools as it
from multiprocessing import Pool


def parse(string):
    """
    >>> parse('London to Dublin = 464')
    (('London', 'Dublin'), 464)
    """
    start, end, dist = re.match(r'(\w+) to (\w+) = (\d+)', string).groups()
    return ((start, end), int(dist))


def getLookup(strings):
    """
    >>> getLookup(['London to Dublin = 464'])
    {('Dublin', 'London'): 464, ('London', 'Dublin'): 464}
    """
    tups = [parse(s) for s in strings]
    ds = [[(tup, dist), (tuple(reversed(tup)), dist)] for (tup, dist) in tups]
    return dict(sum(ds, []))


def segment(path):
    """
    >>> segment((1, 2, 3, 4))
    [(1, 2), (2, 3), (3, 4)]
    """
    return zip(path, path[1:])


def readFile(filename):
    with open(filename, 'r') as f:
        return f.readlines()


# function object for Pool.map
class CalcDist(object):
    def __init__(self, lookup):
        self.lookup = lookup

    def __call__(self, (path, segs)):
        return (path, sum(self.lookup[s] for s in segs))


def distances(strings):
    """
    >>> sorted(d for (_, d) in distances(readFile('test.txt')))
    [605, 605, 659, 659, 982, 982]
    """
    lookup = getLookup(strings)
    cities = set(a for a,_ in lookup.keys())

    paths = it.permutations(cities)
    segss = ((p, segment(p)) for p in paths)

    pool = Pool()
    # for very large paht lengths, we probably will need to use "imap" again
    ds = pool.map(CalcDist(lookup), segss)
    return ds


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    dists = distances(readFile('input.txt'))
    print 'part 1:', min(d for _,d in dists)
    print 'part 2:', max(d for _,d in dists)

