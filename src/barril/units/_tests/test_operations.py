import operator

import pytest

from barril import units
from barril.units import ObtainQuantity
from barril.units.unit_database import UnitDatabase


def testOperation() -> None:
    unit_database = UnitDatabase.GetSingleton()
    unit_database.CheckDefaultUnitDatabase()
    q = ObtainQuantity(unit="m", category="length")

    SCALAR_OPERATION = [operator.add, operator.sub, operator.truediv, operator.mul, operator.mod]
    SCALAR_TYPES = (int, float)

    for operation in SCALAR_OPERATION:
        for cast_type in SCALAR_TYPES:
            # Left
            q2 = operation(cast_type(2), q)
            assert q2.GetQuantityType() == "length"
            assert q2.GetUnit() == "m"

            # Right
            q2 = operation(q, cast_type(2))
            assert q2.GetQuantityType() == "length"
            assert q2.GetUnit() == "m"

    q2 = abs(q)
    assert q2.GetQuantityType() == "length"
    assert q2.GetUnit() == "m"

    q2 = q + q
    assert q2.GetQuantityType() == "length"
    assert q2.GetUnit() == "m"

    q2 = q - q
    assert q2.GetQuantityType() == "length"
    assert q2.GetUnit() == "m"

    q2 = q * int(2)
    assert q2.GetQuantityType() == "length"
    assert q2.GetUnit() == "m"

    q2 = q * 2.0
    assert q2.GetQuantityType() == "length"
    assert q2.GetUnit() == "m"

    q2 = q * q
    assert q2.GetQuantityType() == "(length) ** 2"
    assert q2.GetUnit() == "m2"

    q2 = q * q * q
    assert q2.GetQuantityType() == "(length) ** 3"
    assert q2.GetUnit() == "m3"

    # Check pow
    q2 = q ** 1
    assert q2.GetQuantityType() == "length"
    assert q2.GetUnit() == "m"

    q2 = q ** 2
    assert q2.GetQuantityType() == "(length) ** 2"
    assert q2.GetUnit() == "m2"

    q2 = q ** 3
    assert q2.GetQuantityType() == "(length) ** 3"
    assert q2.GetUnit() == "m3"

    q2 = pow(q, 3)
    assert q2.GetQuantityType() == "(length) ** 3"
    assert q2.GetUnit() == "m3"

    q2 = (q * q) / q
    assert q2.GetQuantityType() == "length"
    assert q2.GetUnit() == "m"

    q2 = (q * q) / ObtainQuantity(unit="d", category="time")
    assert q2.GetQuantityType() == "(length) ** 2 / time"
    assert q2.GetUnit() == "m2/d"

    with pytest.raises(TypeError):
        operator.mul(q, "s")


def MakeArray(values):
    """Creates a standard array used by testScalarOperations"""
    return units.Array("length", values, "m")


def MakeFixedArray(values):
    """Creates a fixed array with 3 dimensions used by testScalarOperations"""
    return units.FixedArray(3, "length", values, "m")


@pytest.mark.parametrize(
    "left, op, right, expected",
    [
        ([100, 80, 50], operator.truediv, 2, [50, 40, 25]),
        ([100, 80, 50], operator.sub, 2, [98, 78, 48]),
        (2, operator.sub, [100, 80, 50], [-98, -78, -48]),
        (2, operator.add, [100, 80, 50], [102, 82, 52]),
        ([100, 80, 50], operator.add, 2, [102, 82, 52]),
        (2, operator.mul, [100, 80, 50], [200, 160, 100]),
        ([100, 80, 50], operator.mul, 2, [200, 160, 100]),
    ],
)
@pytest.mark.parametrize("array_maker", [MakeArray, MakeFixedArray])
def testScalarOperations(left, op, right, expected, array_maker) -> None:
    if isinstance(left, list):
        left = array_maker(left)
    if isinstance(right, list):
        right = array_maker(right)

    result = op(left, right)
    assert result == array_maker(expected)
