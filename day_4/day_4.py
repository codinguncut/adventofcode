#!/usr/bin/env python

"""
NOTE: python Pool.imap is broken and does not close properly
"""

#import md5 # deprecated
import hashlib
import re
import itertools as it
from multiprocessing import Pool

# TODO: Pool.imap would be infinitely more elegant,
#   but unfortunately it is very broken ;(
def imap(func, iterable, chunksize=10000):
    pool = Pool()

    # had trouble using it.chain with infinite iterable ;(
    def chain(gss):
        for gs in gss:
            for g in gs:
                yield g

    def helper():
        while True:
            seg = it.islice(iterable, chunksize)
            yield pool.map(func, seg)

    return chain(helper())


###


# deprecated, use hashlib
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
    filtered = (m for m in matches if m[1])
    return next(filtered)[0]


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    prefix = 'iwrupvqb'
    print('5 zeroes', searchPostfix(prefix, 5))
    print('6 zeroes', searchPostfix(prefix, 6))

