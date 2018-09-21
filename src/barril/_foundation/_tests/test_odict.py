from __future__ import unicode_literals

from barril._foundation.odict import odict


def testInsert():
    d = odict()
    d[1] = 'alpha'
    d[3] = 'charlie'

    assert list(d.items()) == [(1, 'alpha'), (3, 'charlie')]

    d.insert(0, 0, 'ZERO')
    assert list(d.items()) == [(0, 'ZERO'), (1, 'alpha'), (3, 'charlie')]

    d.insert(2, 2, 'bravo')
    assert list(d.items()) == [(0, 'ZERO'), (1, 'alpha'), (2, 'bravo'), (3, 'charlie')]

    d.insert(99, 4, 'echo')
    assert list(d.items()) == [(0, 'ZERO'), (1, 'alpha'), (2, 'bravo'), (3, 'charlie'), (4, 'echo')]


def testDelWithSlices():
    d = odict()
    d[1] = 1
    d[2] = 2
    d[3] = 3

    del d[1:]

    assert len(d) == 1
    assert d[1] == 1
