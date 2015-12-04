#!/usr/bin/env python

import itertools as it
import operator

def getSingleArea(dims):
    """
    return required area of wrapping paper for present
    >>> getSingleArea([2, 3, 4])
    58
    >>> getSingleArea([1, 1, 10])
    43
    """
    sides = [a*b for (a,b) in it.combinations(dims, 2)]
    area = 2 * sum(sides) 
    smallestSide = min(sides)
    return area + smallestSide


def getRibbonLength(dims):
    """
    >>> getRibbonLength([2, 3, 4])
    34
    >>> getRibbonLength([1, 1, 10])
    14
    """
    perimeters = [2*(a+b) for (a,b) in it.combinations(dims, 2)]
    smallestPerim = min(perimeters)
    volume = reduce(operator.mul, dims, 1)
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
        lines = f.readlines()
        dimensions = [parseDimensions(line) for line in lines]
        areas = [getSingleArea(dim) for dim in dimensions]
        ribbons = [getRibbonLength(dim) for dim in dimensions]
        print 'paper:', sum(areas), 'ribbon:', sum(ribbons)

