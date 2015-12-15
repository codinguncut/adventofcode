#!/usr/bin/env python

"""
(c) Johannes Ahlmann, 2015-12, licensed CC0
"""

import doctest
import re
from collections import defaultdict
import itertools as it
import functools as ft
import prelude as p

def parse(string):
    """
    >>> parse('Alice would gain 54 happiness units by sitting next to Bob.')
    (('Alice', 'Bob'), 54)
    >>> parse('Alice would lose 79 happiness units by sitting next to Carol.')
    (('Alice', 'Carol'), -79)
    """
    name1, gain_lose, val, name2 = re.match(r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.', string).groups()
    sign = {'gain': 1, 'lose': -1}[gain_lose]
    return ((name1, name2), sign*int(val))

def make_pairs(seating):
    """
    >>> list(make_pairs([1,2,3]))
    [(1, 2), (2, 3)]
    """
    return zip(seating, p.drop(1, seating))

def calc_happiness(lookup, seating):
    """
    >>> lup = {('Alice', 'David'): -2, ('David', 'Alice'): 46,\
            ('Alice', 'Bob'): 54, ('Bob', 'Alice'): 83,\
            ('Bob', 'David'): -63, ('David', 'Bob'): -7}
    >>> calc_happiness(lup, ['David', 'Alice', 'Bob'])
    111
    """
    if len(seating) == 2:
        raise Exception("logic double-counts for a table of two!")
    pairs = list(make_pairs(seating)) + [(seating[-1], seating[0])]
    return sum(lookup[(a, b)] + lookup[(b, a)] for a, b in pairs)

def get_lookup(filename):
    """read lookup from file"""
    with open(filename, 'r') as inp:
        return dict(parse(line) for line in inp.readlines())

def best_seating(lookup):
    """
    >>> best_seating(get_lookup('test.txt'))
    330
    """
    guests = set(a for a, _ in lookup.keys())

    # '<=' without loss of generality (problem is symmetric)
    perms = (p for p in it.permutations(guests) if p[0] <= p[-1])
    happiness = p.parmap(ft.partial(calc_happiness, lookup), perms)
    return max(happiness)

def run():
    lookup = get_lookup('input.txt')
    print('stage 1:', best_seating(lookup))

    new_lookup = defaultdict(int) # will return 0 for all pairs including 'myself'
    new_lookup.update(lookup)
    new_lookup.update({('myself', 'myself'): 0}) # to get 'myself' into guest list
    print('stage 2:', best_seating(new_lookup))

if __name__ == "__main__":
    doctest.testmod()
    run()
