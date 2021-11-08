import copy

import pytest

from barril.basic.fraction import Fraction
from barril.basic.fraction import FractionValue


def testBasicUsage() -> None:
    f = FractionValue(3, Fraction(5, 3))
    assert f.number == 3
    assert f.fraction == Fraction(5, 3)

    f.number = 5.5
    f.fraction = Fraction(6, 5)
    assert f.number == 5.5
    assert f.fraction == Fraction(6, 5)

    with pytest.raises(TypeError):
        f.SetNumber("hello")  # type:ignore[arg-type]
    with pytest.raises(TypeError):
        f.SetFraction("hello")  # type:ignore[arg-type]
    with pytest.raises(ValueError):
        f.SetFraction((1, 2, 3))  # type:ignore[arg-type]

    assert FractionValue(3).GetFraction() == Fraction(0, 1)


def testDefault() -> None:
    f = FractionValue()
    assert f.number == 0.0
    assert f.fraction == Fraction(0, 1)


def testPartsArentNone() -> None:
    """
    FractionValue can't be initialized nor modified to have None as number or fraction part.
    """
    with pytest.raises(TypeError):
        FractionValue(1, None)  # type:ignore[arg-type]
    with pytest.raises(TypeError):
        FractionValue(None, (0 / 1))  # type:ignore[arg-type]
    with pytest.raises(TypeError):
        FractionValue(None, None)  # type:ignore[arg-type]

    f = FractionValue(1, Fraction(0, 1))
    with pytest.raises(TypeError):
        f.SetNumber(None)  # type:ignore[arg-type]
    with pytest.raises(TypeError):
        f.SetFraction(None)  # type:ignore[arg-type]


def testMatchFractionPart() -> None:
    # Text Ok, should not raise error
    FractionValue.MatchFractionPart("3/4")
    with pytest.raises(ValueError):
        FractionValue.MatchFractionPart("2 3/4")


def testStr() -> None:
    f = FractionValue(3, Fraction(5, 3))
    assert str(f) == "3 5/3"
    assert repr(f) == "FractionValue(3, 5/3)"

    f = FractionValue(3)
    assert str(f) == "3"
    assert repr(f) == "FractionValue(3, 0/1)"


def testEquality() -> None:
    assert FractionValue(3, Fraction(5, 3)) == FractionValue(3, Fraction(5, 3))
    assert not FractionValue(3, Fraction(5, 3)) != FractionValue(3, Fraction(5, 3))

    assert FractionValue(3) == FractionValue(3)
    assert not FractionValue(3) != FractionValue(3)

    assert FractionValue(10, Fraction(5, 3)) != FractionValue(3, Fraction(5, 3))
    assert not FractionValue(10, Fraction(5, 3)) == FractionValue(3, Fraction(5, 3))

    assert FractionValue(10, (5, 3)) == FractionValue(10, Fraction(5, 3))


def testFloat() -> None:
    assert float(FractionValue(3, Fraction(5, 3))) == 3 + 5 / 3.0
    assert float(FractionValue(3)) == 3.0


def testCopy() -> None:
    f = FractionValue(3, (5, 3))
    cf = copy.copy(f)
    assert f == cf
    assert f is not cf

    cf.fraction.numerator = 10
    cf.fraction.denominator = 4
    assert f == FractionValue(3, (5, 3))


def testComparison() -> None:
    assert FractionValue(3) < FractionValue(3, (3, 4))
    assert FractionValue(3) <= FractionValue(3, (3, 4))
    assert FractionValue(3, (3, 4)) > FractionValue(3)
    assert FractionValue(3, (3, 4)) >= FractionValue(3)


def testCreateFromString() -> None:
    """
    Allow the user enter only the fraction value
    """

    def AssertCreateFromString(text, whole, fraction=None):
        assert (
            FractionValue.CreateFromString(text) == FractionValue(whole, fraction)
            if fraction is not None
            else FractionValue(whole)
        )

    AssertCreateFromString("1 1/2", 1, (1, 2))
    AssertCreateFromString("1", 1)
    AssertCreateFromString("1.2 1.1/3", 1.2, (1.1, 3))
    AssertCreateFromString("1.2", 1.2)
    AssertCreateFromString("1/3", 0, (1, 3))
    AssertCreateFromString("3.3/4", 0, (3.3, 4))

    AssertCreateFromString("33/4", 0, (33, 4))
    AssertCreateFromString("  35/4", 0, (35, 4))
    AssertCreateFromString("3 36/4", 3, (36, 4))


def testCreateFromFloat() -> None:
    """
    Allow the user enter only the fraction value
    """
    assert FractionValue.CreateFromFloat(1.375) == FractionValue(1, (3, 8))
    assert FractionValue.CreateFromFloat(2.5) == FractionValue(2, (1, 2))
