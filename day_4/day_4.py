#!/usr/bin/env python

#import md5 # deprecated
import hashlib
import re
import itertools as it
from prelude import *


def getMd5(string):
    """
    >>> getMd5('abcdef609043')[:11]
    '000001dbbfa'
    >>> getMd5('pqrstuv1048970')[:11]
    '000006136ef'
    """
    return hashlib.md5(string.encode()).hexdigest()



# function class for calling from Pool.map
# in python 3 we could use "partial"
class Matcher(object):
    def __init__(self, prefix, zeroes):
        self.prefix = prefix
        self.rex = re.compile(r'^0{'+str(zeroes)+r'}')

    def __call__(self, i):
        h = getMd5(self.prefix + str(i))
        return (i, bool(self.rex.match(h)))


def searchPostfix(prefix, zeroes=5):
    """
    >>> searchPostfix('pqrstuv')
    1048970
    """
    # TODO: use partial
    matches = imap(Matcher(prefix, zeroes), it.count())
    filtered = filter(lambda m: m[1], matches)
    return next(filtered)[0]


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    prefix = 'iwrupvqb'
    print('5 zeroes', searchPostfix(prefix, 5))
    print('6 zeroes', searchPostfix(prefix, 6))

