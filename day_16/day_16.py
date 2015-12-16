#!/usr/bin/env python

"""
logic programming.
trying logpy and pyke.
(c) Johannes Ahlmann, 2015-12-16, licensed CC0
"""

import doctest
from functools import reduce
import re

def check(dct, key_val):
    """ check dictionary against equal integer or missing """
    key, val = key_val
    try:
        return dct[key] == val
    except KeyError:
        return True

def check2(dct, key_val):
    """ check dictionary against key-specific metrics or missing """
    key, val = key_val
    try:
        if key in ['cats', 'trees']:
            return dct[key] > val
        if key in ['pomeranians', 'goldfish']:
            return dct[key] < val
        else:
            return dct[key] == val
    except KeyError:
        return True

def parse(line):
    """
    >>> a, b = parse('Sue 1: goldfish: 9, cars: 0, samoyeds: 9')
    >>> (a, sorted(b.items()))
    (1, [('cars', 0), ('goldfish', 9), ('samoyeds', 9)])
    """
    aunt, rest = re.match(r'Sue (\d+): (.*)', line).groups()
    parts = [(a, int(b)) for a, b in
             [tuple(s.split(r': ')) for s in rest.split(', ')]]
    return (int(aunt), dict(parts))

def solve(aunts, mfcsam, check_func):
    """ filter aunts against all records in mfcsam """
    def func(lst, item):
        return [(i, c) for i, c in lst if check_func(c, item)]
    return reduce(func, mfcsam.items(), aunts)

MFCSAM = {'children': 3,
          'cats': 7,
          'samoyeds': 2,
          'pomeranians': 3,
          'akitas': 0,
          'vizslas': 0,
          'goldfish': 5,
          'trees': 3,
          'cars': 2,
          'perfumes': 1
         }

if __name__ == "__main__":
    doctest.testmod()

    with open('input.txt', 'r') as inp:
        AUNTS = [parse(line) for line in inp.readlines()]
        print(solve(AUNTS, MFCSAM, check))
        print(solve(AUNTS, MFCSAM, check2))

