#!/usr/bin/env python

"""
(c) Johannes Ahlmann, 2015-12, licensed CC0
"""

import doctest
import re
import json

def extract_nums_rex(string):
    """
    assumes no numbers in strings (or dict keys)
    >>> list(extract_nums_rex('[1,2,3]'))
    [1, 2, 3]
    >>> list(extract_nums_rex('{"a":2,"b":4}'))
    [2, 4]
    >>> list(extract_nums_rex('{"a":[-1,1]}'))
    [-1, 1]
    >>> list(extract_nums_rex('[-1,{"a":1}]'))
    [-1, 1]
    >>> list(extract_nums_rex('[]'))
    []
    """
    return (int(i) for i in re.findall(r'-?\d+', string))

def extract_nums_tree(node):
    """
    >>> list(extract_nums_tree([1,2,3]))
    [1, 2, 3]
    """
    if isinstance(node, list):
        for elt in node:
            for val in extract_nums_tree(elt):
                yield val
    elif isinstance(node, dict):
        # TODO: ideally split 'filter' and 'flatten'
        if 'red' not in node.values():
            for key, val in node.items():
                for res in extract_nums_tree(key):
                    yield res
                for res in extract_nums_tree(val):
                    yield res
    elif isinstance(node, str):
        pass
    elif isinstance(node, int):
        yield node
    else:
        raise Exception('unsupported type: ' + str(node) + ' ' + str(type(node)))

if __name__ == "__main__":
    doctest.testmod()

    with open('input.txt', 'r') as f:
        STRING = f.read()
        JS = json.loads(STRING)
        print(sum(extract_nums_rex(STRING)))
        print(sum(extract_nums_tree(JS)))

