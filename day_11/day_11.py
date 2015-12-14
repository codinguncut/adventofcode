#!/usr/bin/env python

import re
from prelude import *


# using postfix to make it tail recursive
def incString(string, postfix=''):
    """
    >>> incString('xydzf')
    'xydzg'
    >>> incString('azzz')
    'baaa'
    """
    if not string:
        # alternatively raise exception
        return 'a' + postfix

    rest, last = (string[:-1], string[-1])
    nxt = ord(last) + 1

    if nxt > ord('z'):
        return incString(rest, 'a' + postfix)
    else:
        return rest + chr(nxt) + postfix


def alpharange():
    return 'abcdefghijklmnopqrstuvwxyz'


ar = alpharange()
reTriples = re.compile('|'.join(a+b+c for a,b,c in zip(ar, tail(ar), tail(tail(ar)))))
reForbidden = re.compile(r'i|o|l')
reDoubles = re.compile(r'(?P<letter1>\w)(?P=letter1).*?(?P<letter2>\w)(?P=letter2)')


def meetsReqs(string):
    """
    >>> meetsReqs('hijklmmn')
    False
    >>> meetsReqs('abbceffg')
    False
    >>> meetsReqs('abbcegjk')
    False
    >>> meetsReqs('abcdefgj')
    False
    >>> meetsReqs('abbcdeeg')
    True
    """
    if re.findall(reForbidden, string):
        return False
    if not re.findall(reDoubles, string):
        return False
    if not re.findall(reTriples, string):
        return False
    return True


def nextPassword(string):
    """
    >>> nextPassword('abcdefgh')
    'abcdffaa'

    >> next(nextPassword('ghijklmn'))
    'ghjaabcc'
    """
    seq = drop(1, iterate(incString, string))
    passwords = filter(meetsReqs, seq)
    return next(passwords)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    nxt = nextPassword('hepxcrrq')
    print(nxt)
    print(nextPassword(nxt))
