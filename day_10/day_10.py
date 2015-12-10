#!/usr/bin/env python

import itertools as it
from functools import reduce

def rle(string):
    """
    >>> rle('aaabcc')
    [(3, 'a'), (1, 'b'), (2, 'c')]
    """
    return [(len(list(g)), k) for k,g in it.groupby(string)]



# TODO: split into <num processors> segments between changing digits and parallelize.
#   minLength i.e. 10,000
def lookAndSay(string):
    """
    >>> lookAndSay('1')
    '11'
    >>> lookAndSay('11')
    '21'
    >>> lookAndSay('21')
    '1211'
    >>> lookAndSay('1211')
    '111221'
    >>> lookAndSay('111221')
    '312211'
    """
    return ''.join(str(a) + str(b) for a,b in rle(string))


def run(string, n):
    """
    >>> run('1', 5)
    6
    """
    res = reduce(lambda s,_: lookAndSay(s), range(n), string)
    return len(res)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    inp = '3113322113'
    print(run(inp, 40))
    print(run(inp, 50))
