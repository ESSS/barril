import pytest

from barril.curve.curve import Curve
from barril.units import Array
from barril.units import ObtainQuantity
from barril.units import UnitDatabase


@pytest.fixture
def unit_database():
    unit_database = UnitDatabase()
    unit_database.AddUnit("length", "milimeters", "mm", "%f * 1000.0", "%f / 1000.0")
    unit_database.AddUnitBase("length", "meters", "m")
    unit_database.AddUnit("length", "centimeters", "cm", "%f * 100.0", "%f / 100.0")
    unit_database.AddUnit("length", "kilometers", "km", "%f / 1000.0", "%f * 1000.0")

    unit_database.AddUnitBase("time", "seconds", "s")
    unit_database.AddUnit("time", "minutes", "min", "%f * 60.0", " %f * 60.0")
    unit_database.AddUnit("time", "hours", "h", "%f * 3600.0", " %f * 3600.0")
    unit_database.AddUnit("time", "days", "d", "%f * 86400.0", " %f * 86400.0")

    unit_database.AddCategory(
        category="length", quantity_type="length", valid_units=["cm", "m", "km"]
    )
    unit_database.AddCategory(
        category="time", quantity_type="time", valid_units=["s", "min", "h", "d"]
    )

    UnitDatabase.PushSingleton(unit_database)
    yield unit_database

    UnitDatabase.PopSingleton()


def testCurves(unit_database) -> None:
    import numpy

    r = ObtainQuantity("m", "length")

    values10 = Array(r, values=numpy.array(list(range(10)), dtype=numpy.int32))
    values9 = Array(r, values=numpy.array(list(range(9)), dtype=numpy.int32))

    domain9 = Array("time", values=numpy.array(list(range(9)), dtype=numpy.int32), unit="s")
    domain10 = Array("time", values=numpy.array(list(range(10)), dtype=numpy.int32), unit="s")

    with pytest.raises(ValueError):
        Curve(values10, domain9)  # type:ignore[arg-type]

    c = Curve(values10, domain10)  # type:ignore[arg-type]

    with pytest.raises(ValueError):
        c.SetDomain(domain9)  # type:ignore[arg-type]
    with pytest.raises(ValueError):
        c.SetImage(values9)  # type:ignore[arg-type]


def testSlice(unit_database) -> None:
    quantity = ObtainQuantity("m", "length")

    def MakeArray(values):
        return Array(quantity, values=values)

    domain = MakeArray([5, 10, 20, 30, 40, 50])
    image = MakeArray([0, 1, 2, 3, 4, 5])

    curve = Curve(image, domain)

    assert curve[0] == (5, 0)
    assert curve[:3] == ([5, 10, 20], [0, 1, 2])
    assert curve[:] == ([5, 10, 20, 30, 40, 50], [0, 1, 2, 3, 4, 5])


def testCurveRepr(unit_database) -> None:
    q1 = ObtainQuantity("m", "length")
    q2 = ObtainQuantity("d", "time")
    curve = Curve(Array(q1, []), Array(q2, []))  # type:ignore[arg-type]
    assert "Curve(m, d)[]" == repr(curve)

    curve = Curve(Array(q1, list(range(3))), Array(q2, list(range(3))))  # type:ignore[arg-type]
    assert "Curve(m, d)[(0, 0) (1, 1) (2, 2)]" == repr(curve)

    curve = Curve(Array(q1, list(range(100))), Array(q2, list(range(100))))  # type:ignore[arg-type]
    expected = (
        "Curve(m, d)[(0, 0) (1, 1) (2, 2) (3, 3) (4, 4) (5, 5) "
        "(6, 6) (7, 7) (8, 8) (9, 9) (10, 10) (11, 11) "
        "(12, 12) (13, 13) (14, 14) (15, 15) (16, 16) "
        "(17, 17) (18, 18) (19, 19) (20, 20)  ... ]"
    )
    assert repr(curve) == expected
