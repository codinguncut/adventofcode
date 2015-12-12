#!/usr/bin/env python

import re
import json

def extractNumsRex(string):
    """
    assumes no numbers in strings (or dict keys)
    >>> list(extractNumsRex('[1,2,3]'))
    [1, 2, 3]
    >>> list(extractNumsRex('{"a":2,"b":4}'))
    [2, 4]
    >>> list(extractNumsRex('{"a":[-1,1]}'))
    [-1, 1]
    >>> list(extractNumsRex('[-1,{"a":1}]'))
    [-1, 1]
    >>> list(extractNumsRex('[]'))
    []
    """
    return (int(i) for i in re.findall(r'-?\d+', string))


def extractNumsTree(node):
    """
    >>> list(extractNumsTree([1,2,3]))
    [1, 2, 3]
    """
    if isinstance(node, list):
        for x in node:
            for y in extractNumsTree(x):
                yield y
    elif isinstance(node, dict):
        # TODO: ideally split 'filter' and 'flatten'
        if not 'red' in node.values():
            for k,v in node.items():
                for x in extractNumsTree(k):
                    yield x
                for x in extractNumsTree(v):
                    yield x
    elif isinstance(node, str):
        pass
    elif isinstance(node, int):
        yield node
    else:
        raise Exception('unsupported type: ' + str(node) + ' ' + str(type(node))) 
    

def evalJson(string):
    return json.loads(string)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    with open('input.txt', 'r') as f:
        string = f.read()
        js = evalJson(string)
        print(sum(extractNumsRex(string)))
        print(sum(extractNumsTree(js)))

