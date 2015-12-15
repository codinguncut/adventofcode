#!/usr/bin/env python

"""
(c) Johannes Ahlmann, 2015-12, licensed CC0
"""

import doctest
import re
import operator

def parse(line):
    """
    >>> parse('123 -> x')
    ('x', ['123'])
    """
    expr, wire = re.match(r'(.*) -> ([a-z]+)', line).groups()
    parts = expr.split(' ')
    return (wire, parts)

def mask16(val):
    return val & 0xFFFF

def expression(lookup, parts):
    """
    >>> d = {'x': ['123'], 'y': ['456']}
    >>> expression(d, ['x'])
    123
    >>> expression(d, ['x', 'AND', 'y'])
    72
    >>> expression(d, ['x', 'OR', 'y'])
    507
    >>> expression(d, ['x', 'LSHIFT', '2'])
    492
    >>> expression(d, ['y', 'RSHIFT', '2'])
    114
    >>> expression(d, ['NOT', 'x'])
    65412
    >>> expression(d, ['NOT', 'y'])
    65079
    """
    if len(parts) == 1:
        part = parts[0]
        if isinstance(part, int): # memoized value
            return part
        if re.match(r'\d+', part): # signal
            return int(part)
        else: # wire
            res = expression(lookup, lookup[part])
            # memoizing
            lookup[part] = [res]
            return res

    if len(parts) == 2 and parts[0] == 'NOT':
        return mask16(~ expression(lookup, [parts[1]]))

    if len(parts) == 3:
        ops = {'AND': operator.and_,
               'OR': operator.or_,
               'LSHIFT': operator.lshift,
               'RSHIFT': operator.rshift}
        a, b = [expression(lookup, [p]) for p in [parts[0], parts[2]]]
        return mask16(ops[parts[1]](a, b))

    raise Exception('unknown expression' + str(parts))

def file_to_lookup(filename):
    with open(filename, 'r') as inp:
        return dict(parse(line) for line in inp.readlines())

def run(filename, wire):
    """
    >>> run('test.txt', 'h')
    65412
    """
    lookup = file_to_lookup(filename)
    return expression(lookup, [wire])

def run2(filename):
    lookup = file_to_lookup(filename)
    lookup['b'] = [run(filename, 'a')]
    return expression(lookup, ['a'])

if __name__ == "__main__":
    doctest.testmod()

    print('part 1:', run('input.txt', 'a'))
    print('part 2:', run2('input.txt'))
