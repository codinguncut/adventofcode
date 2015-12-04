#!/usr/bin/env python

import sys

def consume(lst, paren):
    delta = 1 if paren=='(' else -1
    return lst + [lst[-1] + delta]

parens = sys.stdin.read().strip()
scan = reduce(consume, parens, [0])
enteringBasement = scan.index(-1)

print 'final floor: ', scan[-1], ', entering basement: ', enteringBasement

