#!/usr/bin/env python

"""
this solution is very slow, due to the poor data types available in python.
I also implemented simple solution using "array", but that didn't help at all ;(
"""

from collections import defaultdict
import re
from array import array

# abstract
class ChangeLights(object):
    """ abstract base class for change rectangles """
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def coords(self):
        for x in range(self.left, self.right+1):
            for y in range(self.top, self.bottom+1):
                yield (x, y)
    
    def op(self, grid):
        return grid


# awful use of polymorphism ;)
class Toggle(ChangeLights):
    def op(self, grid):
        return grid.toggle(self.coords())

class TurnOn(ChangeLights):
    def op(self, grid):
        return grid.turnOn(self.coords())

class TurnOff(ChangeLights):
    def op(self, grid):
        return grid.turnOff(self.coords())


class MapGrid(object):
    """ grid class for the light grid """
    def __init__(self):
        self.grid = defaultdict(int)

    # unfortunately not immutable ;(
    def update(self, coords, op):
        for coord in coords:
            self.grid[coord] = op(self.grid[coord])
        return self

    def setTo(self, val, coords):
        self.grid.update(dict((c, val) for c in coords))
        return self

    def turnOn(self, coords):
        return self.setTo(1, coords)

    def turnOff(self, coords):
        return self.setTo(0, coords)

    def toggle(self, coords):
        return self.update(coords, lambda x: 1 if x == 0 else 0)
    
    def result(self):
        return len(filter(lambda x: x==1, self.grid.values()))


class MapGrid2(MapGrid):
    """ light grid for second half of the problem """
    def turnOn(self, coords):
        return self.update(coords, lambda x: x+1)

    def turnOff(self, coords):
        return self.update(coords, lambda x: max(0, x-1))

    def toggle(self, coords):
        return self.update(coords, lambda x: x+2)

    def result(self):
        return sum(self.grid.values())


def evaluate(grid, changeLights):
    """
    >>> x = evaluate(MapGrid(), TurnOn(0, 0, 999, 999))
    >>> x.result()
    1000000

    >>> y = evaluate(x, Toggle(0, 0, 999, 0))
    >>> y.result()
    999000

    >>> z = evaluate(y, TurnOff(499, 499, 500, 500))
    >>> z.result()
    998996
    """
    res = changeLights.op(grid)
    return res


def parse(line):
    """
    >>> x = parse('turn on 0,0 through 999,999')
    >>> type(x).__name__ 
    'TurnOn'
    >>> len(list(x.coords()))
    1000000

    >>> x = parse('toggle 0,0 through 999,0')
    >>> type(x).__name__ 
    'Toggle'
    >>> len(list(x.coords()))
    1000

    >>> x = parse('turn off 499,499 through 500,500')
    >>> type(x).__name__ 
    'TurnOff'
    >>> len(list(x.coords()))
    4
    """
    rex = re.compile( r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)')
    ops = list(rex.match(line).groups())
    conversions = [lambda x: x, int, int, int, int]
    op, left, top, right, bottom = [f(x) for (f, x) in zip(conversions, ops)]

    classes = { 'turn on':  TurnOn,
                'turn off': TurnOff,
                'toggle':   Toggle}
    return (classes[op])(left, top, right, bottom)


def run(grid):
    with open('input.txt') as f:
        rects = [parse(line) for line in f.readlines()]
        res = reduce(evaluate, rects, grid)
        return res


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print 'stage 1', run(MapGrid()).result()
    print 'stage 2', run(MapGrid2()).result()

