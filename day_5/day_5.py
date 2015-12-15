#!/usr/bin/env python

"""
(c) Johannes Ahlmann, 2015-12, licensed CC0
"""

import doctest
import re
import prelude as p

def is_nice_string(string):
    """
    >>> is_nice_string('ugknbfddgicrmopn')
    True
    >>> is_nice_string('aaa')
    True
    >>> is_nice_string('jchzalrnumimnmhp') # no double letter
    False
    >>> is_nice_string('haegwjzuvuyypxyu') # contains 'xy'
    False
    >>> is_nice_string('dvszwmarrgswjxmb') # only one vowel
    False
    """
    # TODO: something faster than findall? compile rexes?
    vowels = re.findall(r'[aeiou]', string)
    double_letter = re.findall(r'(?P<letter>\w)(?P=letter)', string)
    forbidden = re.findall(r'ab|cd|pq|xy', string)
    return len(vowels) >= 3 and bool(double_letter) and not bool(forbidden)

def is_new_nice(string):
    """
    >>> is_new_nice('qjhvhtzxzqqjkmpb')
    True
    >>> is_new_nice('xxyxx')
    True
    >>> is_new_nice('uurcxstgmygtbstg')
    False
    >>> is_new_nice('ieodomkazucvgmuy')
    False
    """
    repeating_pairs = re.findall(r'(?P<pair>\w\w).*(?P=pair)', string)
    repeating_letter = re.findall(r'(?P<letter>\w)\w(?P=letter)', string)
    return bool(repeating_pairs) and bool(repeating_letter)

def read_file(filename):
    with open(filename, 'r') as inp:
        return list(line.strip() for line in inp.readlines())

def run():
    lines = read_file('input.txt')

    one = filter(is_nice_string, lines)
    print('part 1', p.ilen(one))

    two = filter(is_new_nice, lines)
    print('part 2', p.ilen(two))

if __name__ == "__main__":
    doctest.testmod()

    run()
