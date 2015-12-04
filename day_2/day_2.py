#!/usr/bin/env python

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
    perimeters = [2*(l+w), 2*(l+h), 2*(w+h)]
    smallestPerim = min(perimeters)
    volume = l*w*h
    bowLength = volume
    return smallestPerim + bowLength


def parseDimensions(string):
    res = re.findall(r'(\d+)x(\d+)x(\d+)', string)[0]
    return list(int(r) for r in res)


if __name__ == "__main__":
    import doctest
    import re
    doctest.testmod()

    with open('input.txt', 'r') as f:
        lines = f.readlines()
        dimensions = [parseDimensions(line) for line in lines]
        areas = [getSingleArea(dim[0], dim[1], dim[2]) 
                for dim in dimensions]
        ribbons = [getRibbonLength(dim[0], dim[1], dim[2])
                for dim in dimensions]
        print 'paper:', sum(areas), 'ribbon:', sum(ribbons)
