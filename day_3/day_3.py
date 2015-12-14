#!/usr/bin/env python

from prelude import *

###


def singleMove(xy, char):
    """
    evaluate single move
    >>> singleMove((1, 2), '>')
    (2, 2)
    """
    x, y = xy
    dirs = {'>': (x+1,  y),
            '<': (x-1,  y),
            '^': (x,    y-1),
            'v': (x,    y+1)}
    return dirs[char]


def moveSanta(directions):
    """
    >>> moveSanta('>')
    {(1, 0), (0, 0)}
    >>> moveSanta('^v^v^v^v^v')
    {(0, -1), (0, 0)}
    """
    return set(scan(singleMove, directions, (0, 0)))


def housesVisited(directions):
    """
    >>> housesVisited('>')
    2
    >>> housesVisited('^>v<')
    4
    >>> housesVisited('^v^v^v^v^v')
    2
    """
    return len(moveSanta(directions))


def alternating(directions):
    """
    >>> alternating('^v')
    3
    >>> alternating('^>v<')
    3
    >>> alternating('^v^v^v^v^v')
    11
    """
    santa = directions[0::2]
    robot = directions[1::2]
    return len(moveSanta(santa) | moveSanta(robot))


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    with open('input.txt', 'r') as f:
        directions = f.read()
        print('santa', housesVisited(directions))
        print('alternating', alternating(directions))
    

