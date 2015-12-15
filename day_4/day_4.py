#!/usr/bin/env python

"""
(c) Johannes Ahlmann, 2015-12, licensed CC0
"""

import doctest
import hashlib
import re
import itertools as it
import functools as ft
import prelude as p

def get_md5(string):
    """
    >>> get_md5('abcdef609043')[:11]
    '000001dbbfa'
    >>> get_md5('pqrstuv1048970')[:11]
    '000006136ef'
    """
    return hashlib.md5(string.encode()).hexdigest()

def match(prefix, rex, i):
    """
    TODO: is substring matching faster than rex?
    >>> rex = re.compile(r'^0{5}')
    >>> match('abcdef', rex, 609043)
    (609043, True)
    >>> match('abcdef', rex, 609042)
    (609042, False)
    """
    hashed = get_md5(prefix + str(i))
    return (i, bool(rex.match(hashed)))

def search_postfix(prefix, zeroes=5):
    """
    >>> search_postfix('pqrstuv')
    1048970
    """
    rex = re.compile(r'^0{'+str(zeroes)+r'}')
    matches = p.parmap(ft.partial(match, prefix, rex), it.count(1))
    filtered = (a for a, b in matches if b)
    return next(filtered)

if __name__ == "__main__":
    doctest.testmod()

    PREFIX = 'iwrupvqb'
    print('5 zeroes', search_postfix(PREFIX, 5))
    print('6 zeroes', search_postfix(PREFIX, 6))

