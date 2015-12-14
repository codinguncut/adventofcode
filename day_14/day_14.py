#!/usr/bin/env python

import itertools as it
import operator

def take(n, xs):
    return it.islice(xs, n)


def drop(n, xs):
    return it.islice(xs, n, None)


def nth(n, xs):
    return next(drop(n-1, xs))


def scan(f, it, state):
  for x in it:
    state = f(state, x)
    yield state


def isMax(seq):
    """
    >>> isMax((1,2,3,2,3))
    [0, 0, 1, 0, 1]
    """
    mx = max(seq)
    return [int(x == mx) for x in seq]


###


def enqueue(reindeer):
    """
    >>> list(take(6, enqueue(('Vixen', 8, 2, 2))))
    [8, 16, 16, 16, 24, 32]
    """
    _, speed, running, resting = reindeer
    oneCycle = it.chain(it.repeat(speed, running), it.repeat(0, resting))
    return scan(operator.add, it.cycle(oneCycle), 0)

    
def accum(reindeers, n):
    """
    >>> rds = [('Comet', 14, 10, 127), ('Dancer', 16, 11, 162)]
    >>> list(accum(rds, 1000))
    [313, 689]
    """
    queues = [enqueue(r) for r in reindeers]
    winners = map(isMax, zip(*queues))
    scores = scan(lambda s,x: map(sum, zip(s, x)), winners, it.repeat(0))
    return nth(n+1, scores)
    

def run(reindeers, n):
    """ 
    >>> rds = [('Comet', 14, 10, 127), ('Dancer', 16, 11, 162)]
    >>> list(run(rds, 1000))
    [1120, 1056]
    """
    queues = [enqueue(r) for r in reindeers]
    distances = zip(*queues)
    return nth(n+1, distances)


reindeers = [
        ('Vixen', 8, 8, 53),
        ('Blitzen', 13, 4, 49),
        ('Rudolph', 20, 7, 132),
        ('Cupid', 12, 4, 43),
        ('Donner', 9, 5, 38),
        ('Dasher', 10, 4, 37),
        ('Comet', 3, 37, 76),
        ('Prancer', 9, 12, 97),
        ('Dancer', 37, 1, 36)
        ]


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print('part 1:', max(run(reindeers, 2503)))
    print('part 2:', max(accum(reindeers, 2503)))

