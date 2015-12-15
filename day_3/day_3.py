#!/usr/bin/env python

"""
(c) Johannes Ahlmann, 2015-12, CC0
"""

import doctest
import prelude as p

def single_move(x_y, char):
    """
    evaluate single move
    >>> single_move((1, 2), '>')
    (2, 2)
    """
    x, y = x_y
    dirs = {'>': (x+1, y),
            '<': (x-1, y),
            '^': (x, y-1),
            'v': (x, y+1)}
    return dirs[char]

def move_santa(directions):
    """
    >>> move_santa('>')
    {(1, 0), (0, 0)}
    >>> move_santa('^v^v^v^v^v')
    {(0, -1), (0, 0)}
    """
    return set(p.scan(single_move, directions, (0, 0)))

def houses_visited(directions):
    """
    >>> houses_visited('>')
    2
    >>> houses_visited('^>v<')
    4
    >>> houses_visited('^v^v^v^v^v')
    2
    """
    return len(move_santa(directions))

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
    return len(move_santa(santa) | move_santa(robot))

def run(directions):
    print('santa', houses_visited(directions))
    print('alternating', alternating(directions))

if __name__ == "__main__":
    doctest.testmod()

    with open('input.txt', 'r') as f:
        run(f.read())
