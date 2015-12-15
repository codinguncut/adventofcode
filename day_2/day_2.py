#!/usr/bin/env python

"""
(c) Johannes Ahlmann, 2015-12, licensed CC0
"""

import doctest
import re

def get_single_area(l, w, h):
    """
    return required area of wrapping paper for present
    >>> get_single_area(2, 3, 4)
    58
    >>> get_single_area(1, 1, 10)
    43
    """
    sides = [l*w, l*h, w*h]
    area = 2 * sum(sides)
    smallest_side = min(sides)
    return area + smallest_side

def get_ribbon_length(l, w, h):
    """
    >>> get_ribbon_length(2, 3, 4)
    34
    >>> get_ribbon_length(1, 1, 10)
    14
    """
    perimeters = [2*(l+w), 2*(l+h), 2*(w+h)]
    smallest_perim = min(perimeters)
    volume = l*w*h
    bow_length = volume
    return smallest_perim + bow_length

def parse_dimensions(string):
    """
    >>> parse_dimensions('20x50x90')
    [20, 50, 90]
    """
    res = re.match(r'(\d+)x(\d+)x(\d+)', string).groups()
    return [int(r) for r in res]

def run():
    with open('input.txt', 'r') as inp:
        dimensions = [parse_dimensions(line) for line in
                      inp.readlines()]
        areas = [get_single_area(*dim) for dim in dimensions]
        ribbons = [get_ribbon_length(*dim) for dim in dimensions]
        print('paper:', sum(areas), 'ribbon:', sum(ribbons))

if __name__ == "__main__":
    doctest.testmod()

    run()
