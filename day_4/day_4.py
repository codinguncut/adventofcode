#!/usr/bin/env python

"""
NOTE: python Pool.imap is broken and does not close properly
"""

import md5 # deprecated
import re
import itertools as it
from multiprocessing import Pool


# deprecated, use hashlib
def getMd5(string):
    """
    >>> getMd5('abcdef609043')[:11]
    '000001dbbfa'
    >>> getMd5('pqrstuv1048970')[:11]
    '000006136ef'
    """
    return md5.new(string).hexdigest()


# function class for Pool.map
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
    pool = Pool()
    chunksize = 10000
    
    # TODO: Pool.imap would be infinitely more elegant,
    #   but unfortunately it is very broken ;(
    # NOTE: might use a generator to hide the chunk plumbing
    nums = it.count(1)
    while True:
        seg = list(it.islice(nums, chunksize))
        matches = pool.map(Matcher(prefix, zeroes), seg)
        filtered = filter(lambda (x, b): b, matches)
        if filtered:
            return filtered[0][0]


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    prefix = 'iwrupvqb'
    print '5 zeroes', searchPostfix(prefix, 5)
    print '6 zeroes', searchPostfix(prefix, 6)

