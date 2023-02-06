import pickle
from collections import OrderedDict

import pytest

from barril.units import GetUnknownQuantity
from barril.units import ObtainQuantity
from barril.units import Quantity
from barril.units import UNKNOWN_QUANTITY
from barril.units import UNKNOWN_QUANTITY_TYPE
from barril.units import UNKNOWN_UNIT
from barril.units.unit_database import InvalidUnitError
from barril.units.unit_database import UnitDatabase


def testQuantityInit(mocker) -> None:
    # 1: cache it
    ObtainQuantity("m", "length")

    # 2: check
    calls = [0]
    original = UnitDatabase.GetSingleton

    def _New(*args, **kwargs):
        calls[0] += 1
        return original()

    m = mocker.patch.object(UnitDatabase, "GetSingleton")
    m.return_value = _New()

    ObtainQuantity("m", "length")
    assert calls[0] == 1


def testQuantitySharedInstances() -> None:
    quantity = ObtainQuantity("m", "length")
    assert quantity is ObtainQuantity("m", "length")


def testQuantityCaption(unit_database_posc_len) -> None:
    unit_database = unit_database_posc_len
    unit_database.AddUnitBase(UNKNOWN_QUANTITY_TYPE, UNKNOWN_QUANTITY_TYPE, UNKNOWN_UNIT)
    unit_database.AddCategory(UNKNOWN_QUANTITY_TYPE, UNKNOWN_QUANTITY_TYPE)

    q0 = ObtainQuantity(unit=UNKNOWN_UNIT, category=UNKNOWN_QUANTITY_TYPE)
    assert "" == q0.GetUnknownCaption()

    q = ObtainQuantity(
        unit=UNKNOWN_UNIT, unknown_unit_caption="Feeeet", category=UNKNOWN_QUANTITY_TYPE
    )
    assert "Feeeet" == q.GetUnknownCaption()
    assert "Feeeet <unknown>" == q.GetUnitCaption()

    q = Quantity.CreateDerived(OrderedDict([("length", ("m", 1))]), unknown_unit_caption="Feeeet")
    assert "m" == q.GetUnitCaption()


def testUnknownQuantity() -> None:
    global_unknown = UNKNOWN_QUANTITY

    # Global
    assert global_unknown is GetUnknownQuantity()

    # Cache
    my_unknown = GetUnknownQuantity("my_unknown")
    assert my_unknown is GetUnknownQuantity("my_unknown")


def testHash() -> None:
    quantity1 = ObtainQuantity("m")
    quantity2 = ObtainQuantity("m", "length")
    assert hash(quantity1) == hash(quantity2)
    assert quantity1 == quantity2

    unknown1 = ObtainQuantity(UNKNOWN_UNIT, unknown_unit_caption="foo")
    unknown2 = ObtainQuantity(UNKNOWN_UNIT, unknown_unit_caption="foo_bar")
    unknown3 = ObtainQuantity(UNKNOWN_UNIT, unknown_unit_caption="foo")
    assert hash(unknown1) == hash(unknown3)
    assert unknown1 == unknown3

    assert unknown1 != unknown2


def testPickle() -> None:
    quantity1 = ObtainQuantity("m")
    quantity2 = quantity1.__reduce__()
    assert quantity1 is quantity2[0](*quantity2[1])  # type:ignore[operator]
    obtained = pickle.loads(pickle.dumps(quantity1))
    assert obtained is quantity1, f"{obtained} != {quantity1}"


def testConvert() -> None:
    assert [1000.0, 3000.0] == ObtainQuantity("m").Convert([10, 30], "cm")


def testUnknown() -> None:
    with pytest.raises(InvalidUnitError):
        ObtainQuantity("m3", UNKNOWN_QUANTITY_TYPE)


def testDivision() -> None:
    meters = ObtainQuantity("m")
    seconds = ObtainQuantity("s")
    speed = meters / seconds
    no_unit = meters / meters
    assert speed.GetUnit() == "m/s"
    assert speed.unit == "m/s"
    assert no_unit.GetUnit() == ""
