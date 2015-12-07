#!/usr/bin/env python

def scan(f, it, state):
  yield state 
  for x in it:
    state = f(state, x)
    yield state


def singleMove((x, y), char):
    """
    evaluate single move
    >>> singleMove((1, 2), '>')
    (2, 2)
    """
    dirs = {'>': (x+1,  y),
            '<': (x-1,  y),
            '^': (x,    y-1),
            'v': (x,    y+1)}
    return dirs[char]


def moveSanta(directions):
    """
    >>> moveSanta('>')
    set([(1, 0), (0, 0)])
    >>> moveSanta('^v^v^v^v^v')
    set([(0, -1), (0, 0)])
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


def readFile(filename):
    with open(filename, 'r') as f:
        return f.read()


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    directions = readFile('input.txt')
    print 'santa', housesVisited(directions)
    print 'alternating', alternating(directions)
    

