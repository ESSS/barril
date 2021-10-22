from typing import Any

import pytest

from barril.units.unit_system import UnitSystem


@pytest.fixture
def units_mapping_1():
    units_mapping = {"length": "m", "viscosity": "cP"}
    return units_mapping


@pytest.fixture
def units_mapping_2():
    units_mapping = {"length": "km", "viscosity": "cP"}
    return units_mapping


def testUnitSystemManager(units_mapping_1) -> None:
    system1 = UnitSystem("system1", "My System", units_mapping_1)
    system1.SetReadOnly(True)
    assert system1.GetId() == "system1"
    assert system1.GetCaption() == "My System"
    assert system1.IsReadOnly()
    assert system1.GetDefaultUnit("length") == "m"
    assert system1.GetDefaultUnit("viscosity") == "cP"
    assert system1.GetDefaultUnit("pressure") is None
    assert system1.GetDefaultUnit("") is None


def testEquality(units_mapping_1, units_mapping_2) -> None:
    system1 = UnitSystem("system1", "My System", units_mapping_1, True)
    system2 = UnitSystem("system1", "My System", units_mapping_1, True)
    system3 = UnitSystem("system3", "My System 3", units_mapping_2, False)

    assert system1 == system2
    assert not system1 != system2

    assert system2 != system3
    assert not system1 == system3

    assert system1 is not None


def testSetDefaultUnitCallback(units_mapping_1) -> None:
    """
    Implements on_default_unit on unit system, called when the default unit changes.
    """

    class MockClass:
        callback_params: Any = None

        def OnDefaultUnit(self, category, unit):
            self.callback_params = (category, unit)

    obj = MockClass()
    system1 = UnitSystem("system1", "My System", units_mapping_1)
    system1.on_default_unit.Register(obj.OnDefaultUnit)

    system1.SetDefaultUnit("length", "km")
    assert obj.callback_params == ("length", "km")

    system1.SetDefaultUnit("viscosity", "P")
    assert obj.callback_params == ("viscosity", "P")


def testRemoveCategory(units_mapping_1) -> None:
    class MockClass:
        update_notified: Any = None

        def CallbackUnit(self, category, new_unit):
            if category == "length":
                self.update_notified = True

    system_1 = UnitSystem("system1", "My System", units_mapping_1)

    obj = MockClass()
    system_1.on_default_unit.Register(obj.CallbackUnit)
    assert system_1.GetDefaultUnit("length") == "m"

    # Removing the given quantity
    obj.update_notified = False
    system_1.RemoveCategory("length")
    assert system_1.GetDefaultUnit("length") is None

    assert obj.update_notified
