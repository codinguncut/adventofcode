#!/usr/bin/env python

from collections import Counter, deque

def singleMove((x, y), char):
    """
    evaluate single move
    >>> singleMove((1, 2), '>')
    (2, 2)
    >>> singleMove((1, 2), 'a')
    Traceback (most recent call last):
    ...
    AssertionError
    """
    dirs = {'>': (x+1,  y),
            '<': (x-1,  y),
            '^': (x,    y-1),
            'v': (x,    y+1)}
    assert char in dirs 
    return dirs[char]


def moveSanta(directions):
    """
    >>> moveSanta('>')
    Counter({(1, 0): 1, (0, 0): 1})
    >>> moveSanta('^v^v^v^v^v')
    Counter({(0, 0): 6, (0, -1): 5})
    """
    def scan(lst, d):
        return lst + [singleMove(lst[-1], d)]

    return Counter(reduce(scan, directions, [(0, 0)]))


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
    return len(moveSanta(santa) + moveSanta(robot))


def readFile(filename):
    with open(filename, 'r') as f:
        return f.read()


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    directions = readFile('input.txt')
    print 'santa', housesVisited(directions)
    print 'alternating', alternating(directions)
    

