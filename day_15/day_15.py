#!/usr/bin/env python

"""
This should really be solved with a discreet linear programming tools (MILP),
or a constraint solver.
Couldn't get constraint solvers to work ('python-constraint', 'constraint').

(c) Johannes Ahlmann, 2015-12-15, licensed CC0
"""

import doctest
import re
import functools as ft
import prelude as p

def parse(string):
    """
    >>> parse('Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8')
    ('Butterscotch', -1, -2, 6, 3, 8)
    """
    name, cap, dur, fla, tex, cal = (
        re.match(r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), '+
                 r'texture (-?\d+), calories (-?\d+)', string).groups())
    return (name, int(cap), int(dur), int(fla), int(tex), int(cal))

def calc_score(ingredients, spoons):
    """
    >>> calc_score([('', -1, -2, 6, 3, 8), ('', 2, 3, -2, -1, 3)], [44, 56])
    62842880
    """
    # NOTE: use matrix mult
    active = [[spoon * y for y in ing[1:5]] for ing, spoon in
              zip(ingredients, spoons)]
    sums = [max(0, sum(x)) for x in zip(*active)]
    return p.product(sums)

def calc_calories(ingredients, spoons):
    """
    >>> calc_calories([('', -1, -2, 6, 3, 8), ('', 2, 3, -2, -1, 3)], [40, 60])
    500
    """
    return sum(a*b[5] for a, b in zip(spoons, ingredients))

def combinations(min_val, max_val, num, remainder):
    """
    >>> list(combinations(1, 3, 2, 3))
    [(1, 2), (2, 1)]
    """
    if num == 1:
        if min_val <= remainder <= max_val:
            yield (remainder,)
        return
    for val in range(min_val, max_val+1):
        for comb in combinations(min_val, max_val, num-1, remainder-val):
            yield (val,) + comb

def is_500_calories(ingredients, spoons):
    """
    >>> is_500_calories([('', -1, -2, 6, 3, 8), ('', 2, 3, -2, -1, 3)], [40, 60])
    True
    """
    return calc_calories(ingredients, spoons) == 500

def solve(ingredients, pred=None):
    """
    NOTE: can extract lots of constraints from ingredient matrix
    >>> ingredients = [('', -1, -2, 6, 3, 8), ('', 2, 3, -2, -1, 3)]
    >>> max(solve(ingredients))
    (62842880, (44, 56))
    >>> max(solve(ingredients, ft.partial(is_500_calories, ingredients)))
    (57600000, (40, 60))
    """
    combs = combinations(0, 100, len(ingredients), 100)
    return ((calc_score(ingredients, tup), tup) for tup in filter(pred, combs))

def load_ingredients(filename):
    with open(filename, 'r') as inp:
        return [parse(line) for line in inp.readlines()]

if __name__ == "__main__":
    doctest.testmod()

    INGREDIENTS = load_ingredients('input.txt')
    print(max(solve(INGREDIENTS)))
    print(max(solve(INGREDIENTS, ft.partial(is_500_calories, INGREDIENTS))))

