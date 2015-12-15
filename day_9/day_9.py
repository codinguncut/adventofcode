#!/usr/bin/env python

"""
lots of optimization possible:
- use proper graph library (shortest path, travelling salesman)
- split into and cache/memoize subpaths (i.e. of length 2^n)
- only calculate paths where p[0] < p[-1], and use reverse for inverse path
- operate on one-hot int encoding rather than full string (faster hash?)
"""

import doctest
import re
import itertools as it
import functools as ft
import prelude as p

def parse(string):
    """
    >>> parse('London to Dublin = 464')
    (('London', 'Dublin'), 464)
    """
    start, end, dist = re.match(r'(\w+) to (\w+) = (\d+)', string).groups()
    return ((start, end), int(dist))

def get_lookup(strings):
    """
    >>> sorted(get_lookup(['London to Dublin = 464']).items())
    [(('Dublin', 'London'), 464), (('London', 'Dublin'), 464)]
    """
    tups = [parse(s) for s in strings]
    dists = [[(tup, dist), (tuple(reversed(tup)), dist)] for (tup, dist) in tups]
    return dict(p.concat(dists))

def segment(path):
    """
    >>> list(segment((1, 2, 3, 4)))
    [(1, 2), (2, 3), (3, 4)]
    """
    return zip(path, path[1:])

def read_file(filename):
    with open(filename, 'r') as f:
        return f.readlines()

def calc(lookup, path_segs):
    # TODO: doctest
    path, segs = path_segs
    return (path, sum(lookup[s] for s in segs))

def distances(strings):
    """
    >>> sorted(list(d for (_, d) in distances(read_file('test.txt'))))
    [605, 605, 659, 659, 982, 982]
    """
    lookup = get_lookup(strings)
    cities = set(a for a, _ in lookup.keys())

    paths = it.permutations(cities)
    segss = ((p, segment(p)) for p in paths)

    dists = p.parmap(ft.partial(calc, lookup), segss)
    return list(dists)

if __name__ == "__main__":
    doctest.testmod()

    DISTS = distances(read_file('input.txt'))
    print('part 1:', min(d for _, d in DISTS))
    print('part 2:', max(d for _, d in DISTS))

