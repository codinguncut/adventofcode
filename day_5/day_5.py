#!/usr/bin/env python

import re
import sys

def isNiceString(string):
    """
    >>> isNiceString('ugknbfddgicrmopn')
    True
    >>> isNiceString('aaa')
    True
    >>> isNiceString('jchzalrnumimnmhp') # no double letter
    False
    >>> isNiceString('haegwjzuvuyypxyu') # contains 'xy'
    False
    >>> isNiceString('dvszwmarrgswjxmb') # only one vowel
    False
    """
    vowels = re.findall(r'[aeiou]', string)
    doubleLetter = re.findall(r'(?P<letter>\w)(?P=letter)', string)
    forbidden = re.findall(r'ab|cd|pq|xy', string)
    return len(vowels) >= 3 and bool(doubleLetter) and not bool(forbidden)


def isNewNice(string):
    """
    >>> isNewNice('qjhvhtzxzqqjkmpb')
    True
    >>> isNewNice('xxyxx')
    True
    >>> isNewNice('uurcxstgmygtbstg')
    False
    >>> isNewNice('ieodomkazucvgmuy')
    False
    """
    repeatingPairs = re.findall(r'(?P<pair>\w\w).*(?P=pair)', string)
    repeatingLetter = re.findall(r'(?P<letter>\w)\w(?P=letter)', string)
    return bool(repeatingPairs) and bool(repeatingLetter)


def readFile(filename):
    with open(filename, 'r') as f:
        return list(line.strip() for line in f.readlines())



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    lines = readFile('input.txt')

    res = filter(isNiceString, lines)
    print 'part 1', len(res)

    two = filter(isNewNice, lines)
    print 'part 2', len(two)
