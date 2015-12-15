#!/usr/bin/env python

"""
(c) Johannes Ahlmann, 2015-12, licensed CC0
"""

import doctest
import itertools as it
import prelude as p

def rle(string):
    """
    >>> rle('aaabcc')
    [(3, 'a'), (1, 'b'), (2, 'c')]
    """
    return [(p.ilen(g), k) for k, g in it.groupby(string)]

# TODO: split into <num processors> segments between changing digits and parallelize.
#   minLength i.e. 10,000
def look_and_say(string):
    """
    >>> look_and_say('1')
    '11'
    >>> look_and_say('11')
    '21'
    >>> look_and_say('21')
    '1211'
    >>> look_and_say('1211')
    '111221'
    >>> look_and_say('111221')
    '312211'
    """
    return ''.join(str(a) + str(b) for a, b in rle(string))

def run(string, num):
    """
    >>> run('1', 5)
    6
    """
    res = p.nth(num, p.iterate(look_and_say, string))
    return p.ilen(res)

if __name__ == "__main__":
    doctest.testmod()

    INP = '3113322113'
    print(run(INP, 40))
    print(run(INP, 50))
