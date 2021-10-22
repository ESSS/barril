import copy

from barril.basic.fraction import Fraction


def testBasicUsage() -> None:
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


def testStr() -> None:
    assert str(Fraction(5, 3)) == "5/3"
    assert repr(Fraction(5, 3)) == "Fraction(5, 3)"

    assert str(Fraction(3 / 1000, 4)) == "3/4000"


def testReduce() -> None:
    f = Fraction(5, 3)
    f[0] = 15
    assert tuple(f) == (5, 1)


def testOperations() -> None:
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


def testCopy() -> None:
    f = Fraction(5, 3)
    cf = copy.copy(f)
    assert f == cf
    assert not f != cf
    assert f is not cf

    assert f != Fraction(3, 5)
    assert not f == Fraction(3, 5)


def testStrFormat(mocker) -> None:
    """
    Scalar field behavior. In this test we make sure that the
    Fraction.__str__ method calls FormatFloat, which handles
    the locale properly.
    """
    # By default, the numbers are formatted using "%g"
    f = Fraction(5, 3)
    assert str(f), "5/3"

    # Test the use of FormatFloat | 5.6 is 28/5 | 5.6/3 is 28/15
    f = Fraction(5.6, 3)
    assert str(f) == "28/15"

    mocker.patch("barril.basic.format_float.FormatFloat", side_effect=lambda x, y: "X%.2fX" % y)
    assert str(f) == "X28.00X/X15.00X"
