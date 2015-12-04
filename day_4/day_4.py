#!/usr/bin/env python

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


# pool needs global function, not sure how best to pass prefix in...
def f(i):
    prefix = 'iwrupvqb'
    return (i, getMd5(prefix + str(i)))


def searchPostfix(zeroes=5):
    """
     searchPostfix('pqrstuv')
    1048970
    """
    pool = Pool(4)
    hashes = pool.imap(f, it.count(), chunksize=1000)
    rex = re.compile(r'^0{'+str(zeroes)+r'}')
    for i, h in hashes:
        if rex.match(h):
            return i


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print '5 zeroes', searchPostfix(5)
    print '6 zeroes', searchPostfix(6)
