#!/usr/bin/env python

import sys
import itertools as it

def consume(lst, paren):
    delta = 1 if paren=='(' else -1
    lst.append(lst[-1] + delta)
    return lst

parens = sys.stdin.read().strip()
scan = reduce(consume, parens, [0])
aboveGround = list(it.takewhile(lambda x: x>=0, scan))

print scan
print 'final floor: ', scan[-1], ', entering basement: ', len(aboveGround)

