from __future__ import absolute_import, division, unicode_literals

import copy

import pytest
import six

from barril.basic.fraction import Fraction


def testBasicUsage():
    f = Fraction(5, 3)
    assert tuple(f) == (5, 3)
    assert len(f) == 2
    assert f[0] == 5
    assert f[1] == 3
    assert f.numerator == 5
    assert f.denominator == 3
    f.numerator = 10
    assert tuple(f) == (10, 3)
    f.denominator = 4
    assert tuple(f) == (5, 2)


def testStr():
    assert six.text_type(Fraction(5, 3)) == '5/3'
    assert repr(Fraction(5, 3)) == 'Fraction(5, 3)'

    assert six.text_type(Fraction(3 / 1000, 4)) == '3/4000'


def testReduce():
    f = Fraction(5, 3)
    f[0] = 15
    assert tuple(f) == (5, 1)


def testOperations():
    # float operator
    assert float(Fraction(5, 3)) == 5.0 / 3.0

    # sum
    assert Fraction(5, 3) + Fraction(2, 3) == Fraction(7, 3)
    assert Fraction(5, 3) + 5.0 == Fraction(20, 3)
    assert 5.0 + Fraction(5, 3) == Fraction(20, 3)

    # sub
    assert Fraction(5, 3) - Fraction(2, 3) == Fraction(3, 3)
    assert Fraction(5, 3) - 1.0 == Fraction(2, 3)
    assert 1.0 - Fraction(5, 3) == Fraction(-2, 3)

    # mul
    assert Fraction(5, 3) * Fraction(4, 3) == Fraction(20, 9)
    assert 3 * Fraction(5, 3) == Fraction(15, 3)
    assert Fraction(5, 3) * 3 == Fraction(15, 3)

    # div
    assert Fraction(5, 3) / Fraction(5, 3) == Fraction(15, 15)
    assert Fraction(5, 3) / 3 == Fraction(5, 9)
    assert 3 / Fraction(5, 3) == Fraction(9, 5)

    # inv
    assert Fraction(5, 3).inv() == Fraction(3, 5)

    # neg
    assert -Fraction(5, 3) == Fraction(-5, 3)


def testCopy():
    f = Fraction(5, 3)
    cf = copy.copy(f)
    assert f == cf
    assert not f != cf
    assert f is not cf

    assert f != Fraction(3, 5)
    assert not f == Fraction(3, 5)


def testStrFormat():
    '''
    Scalar field behavior. In this test we make sure that the
    Fraction.__str__ method calls FormatFloat, which handles
    the locale properly.
    '''
    import barril.basic.format_float

    # By default, the numbers are formatted using "%g"
    f = Fraction(5, 3)
    assert six.text_type(f), '5/3'

    # Test the use of FormatFloat | 5.6 is 28/5 | 5.6/3 is 28/15
    f = Fraction(5.6, 3)
    assert six.text_type(f) == '28/15'

    original_format_float = barril.basic.format_float.FormatFloat
    barril.basic.format_float.FormatFloat = lambda x, y: 'X%.2fX' % y
    try:
        assert six.text_type(f) == 'X28.00X/X15.00X'
    finally:
        barril.basic.format_float.FormatFloat = original_format_float

    assert six.text_type(f) == '28/15'


@pytest.mark.skipif(condition=not six.PY2, reason="Long type is no longer available in Python 3")
def testLong():
    f = Fraction(20000000000000000, None)
    assert tuple(f) == (20000000000000000, 1)
