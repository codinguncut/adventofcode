#!/usr/bin/env python

import re
import operator

def parse(line):
    """
    >>> parse('123 -> x')
    ('x', ['123'])
    """
    expression, wire = re.match(r'(.*) -> ([a-z]+)', line).groups()
    parts = expression.split(' ')
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
        if type(part) == int: # memoized value
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
        ops = { 'AND': operator.and_,
                'OR': operator.or_,
                'LSHIFT': operator.lshift,
                'RSHIFT': operator.rshift}
        a,b = [expression(lookup, [p]) for p in [parts[0], parts[2]]]
        return mask16(ops[parts[1]](a, b))

    raise Exception('unknown expression' + str(parts))

    
def fileToAssignments(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        return dict(parse(line) for line in lines)


def run(filename, wire):
    """
    >>> run('test.txt', 'h')
    65412
    """
    d = fileToAssignments(filename)
    return expression(d, [wire])


def run2(filename):
    d = fileToAssignments(filename)
    d['b'] = [run(filename, 'a')]
    return expression(d, ['a'])


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print 'part 1:', run('input.txt', 'a')
    print 'part 2:', run2('input.txt')
