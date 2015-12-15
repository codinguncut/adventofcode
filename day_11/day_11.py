#!/usr/bin/env python

"""
(c) Johannes Ahlmann, 2015-12, licensed CC0
"""

import doctest
import re
import prelude as p

# using postfix to make it tail recursive
def inc_string(string, postfix=''):
    """
    >>> inc_string('xydzf')
    'xydzg'
    >>> inc_string('azzz')
    'baaa'
    """
    if not string:
        # alternatively raise exception
        return 'a' + postfix

    rest, last = (string[:-1], string[-1])
    nxt = ord(last) + 1

    if nxt > ord('z'):
        return inc_string(rest, 'a' + postfix)
    else:
        return rest + chr(nxt) + postfix

def alpharange():
    return 'abcdefghijklmnopqrstuvwxyz'

AR = alpharange()
RE_TRIPLES = re.compile(
    '|'.join(a+b+c for a, b, c in
             zip(AR, p.tail(AR), p.tail(p.tail(AR)))))
RE_FORBIDDEN = re.compile(r'i|o|l')
RE_DOUBLES = re.compile(r'(?P<letter1>\w)(?P=letter1).*?(?P<letter2>\w)(?P=letter2)')

def meets_reqs(string):
    """
    >>> meets_reqs('hijklmmn')
    False
    >>> meets_reqs('abbceffg')
    False
    >>> meets_reqs('abbcegjk')
    False
    >>> meets_reqs('abcdefgj')
    False
    >>> meets_reqs('abbcdeeg')
    True
    """
    # 'search' faster than 'findall'?
    if re.findall(RE_FORBIDDEN, string):
        return False
    if not re.findall(RE_DOUBLES, string):
        return False
    if not re.findall(RE_TRIPLES, string):
        return False
    return True

def get_passwords(string):
    """
    >>> next(get_passwords('abcdefgh'))
    'abcdffaa'

    >> next(get_passwords('ghijklmn'))
    'ghjaabcc'
    """
    seq = p.drop(1, p.iterate(inc_string, string))
    passwords = filter(meets_reqs, seq)
    return passwords

if __name__ == "__main__":
    doctest.testmod()

    PASSWORDS = get_passwords('hepxcrrq')
    print(next(PASSWORDS))
    print(next(PASSWORDS))

