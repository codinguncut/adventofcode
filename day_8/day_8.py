#!/usr/bin/env python

import ast
import re


def unescape(string):
    """
    >>> len(unescape('""'))
    0
    >>> len(unescape(r'"aaa\\"aaa"'))
    7
    >>> len(unescape(r'''"\x27"'''))
    1
    """
    # supposedly safe ;)
    return ast.literal_eval(string)


def escape(string):
    """
    >>> len(escape(r'''""'''))
    6
    >>> len(escape(r'''"abc"'''))
    9
    >>> len(escape(r'''"aaa\\"aaa"'''))
    16
    """
    return '"' + re.escape(string) + '"'


def run(func, filename):
    """
    >>> run(unescape, 'test.txt')
    12
    >>> run(escape, 'test.txt')
    19
    """
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        raw = sum(len(s) for s in lines)
        res = sum(len(func(s)) for s in lines)
        return abs(raw - res)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print('part 1:', run(unescape, 'input.txt'))
    print('part 2:', run(escape, 'input.txt'))
