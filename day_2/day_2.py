#!/usr/bin/env python

import itertools as it
import operator

def getSingleArea(l, w, h):
    """
    return required area of wrapping paper for present
    >>> getSingleArea(2, 3, 4)
    58
    >>> getSingleArea(1, 1, 10)
    43
    """
    sides = [l*w, l*h, w*h]
    area = 2 * sum(sides) 
    smallestSide = min(sides)
    return area + smallestSide


def getRibbonLength(l, w, h):
    """
    >>> getRibbonLength(2, 3, 4)
    34
    >>> getRibbonLength(1, 1, 10)
    14
    """
    perimeters = [2*(l+h), 2*(l+w), 2*(h+w)]
    smallestPerim = min(perimeters)
    volume = l*w*h
    bowLength = volume
    return smallestPerim + bowLength


def parseDimensions(string):
    res = re.findall(r'(\d+)x(\d+)x(\d+)', string)[0]
    return [int(r) for r in res]


if __name__ == "__main__":
    import doctest
    import re
    doctest.testmod()

    with open('input.txt', 'r') as f:
        dimensions = [parseDimensions(line) for line in f.readlines()]
        areas = [getSingleArea(*dim) for dim in dimensions]
        ribbons = [getRibbonLength(*dim) for dim in dimensions]
        print 'paper:', sum(areas), 'ribbon:', sum(ribbons)

