#!/usr/bin/env python

import re
from collections import defaultdict
from prelude import *

def parse(string):
    """
    >>> parse('Alice would gain 54 happiness units by sitting next to Bob.')
    (('Alice', 'Bob'), 54)
    >>> parse('Alice would lose 79 happiness units by sitting next to Carol.')
    (('Alice', 'Carol'), -79)
    """
    name1, gainLose, val, name2 = re.match(r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.', string).groups()
    sign = {'gain': 1, 'lose': -1}[gainLose]
    return ((name1, name2), sign*int(val))


def makePairs(seating):
    return zip(seating, drop(1, seating))


def calcHappiness(lookup, seating):
    """
    >>> lup = {('Alice', 'David'): -2, ('David', 'Alice'): 46, ('Alice', 'Bob'): 54, ('Bob', 'Alice'): 83, ('Bob', 'David'): -63, ('David', 'Bob'): -7}
    >>> calcHappiness(lup, ['David', 'Alice', 'Bob'])
    111
    """
    if 2 == len(seating):
        raise Exception("logic double-counts for a table of two!")
    pairs = list(makePairs(seating)) + [(seating[-1], seating[0])]
    return sum(lookup[(a,b)] + lookup[(b,a)] for a,b in pairs)


def getLookup(filename):
    with open(filename, 'r') as f:
        return dict(map(parse, f.readlines()))
    

def run(lookup):
    """
    >>> run(getLookup('test.txt'))
    330
    """
    guests = set(a for a,_ in lookup.keys())

    # '<=' without loss of generality (problem is symmetric)
    perms = filter(lambda x: x[0] <= x[-1], it.permutations(guests))
    happiness = imap(ft.partial(calcHappiness, lookup), perms)
    return max(happiness)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    lookup = getLookup('input.txt')
    print('stage 1:', run(lookup))

    newLookup = defaultdict(int) # will return 0 for all pairs including 'myself'
    newLookup.update(lookup)
    newLookup.update({('myself', 'myself'): 0}) # to get 'myself' into guest list
    print('stage 2:', run(newLookup))

