import weakref
from typing import Dict

import pytest

from barril.units import Array
from barril.units import FixedArray
from barril.units import FractionScalar
from barril.units import ObtainQuantity
from barril.units import Scalar
from barril.units.unit_system import UnitSystem
from barril.units.unit_system_manager import InvalidTemplateError
from barril.units.unit_system_manager import UnitSystemCategoriesError
from barril.units.unit_system_manager import UnitSystemIDError
from barril.units.unit_system_manager import UnitSystemManager


@pytest.fixture
def unit_manager():
    manager = UnitSystemManager()
    UnitSystemManager.PushSingleton(manager)

    yield manager

    UnitSystemManager.PopSingleton()


@pytest.fixture
def units_mapping_1():
    units_mapping = {"length": "m"}
    return units_mapping


@pytest.fixture
def units_mapping_2():
    units_mapping = {"length": "km"}
    return units_mapping


@pytest.fixture
def units_mapping_3():
    units_mapping: Dict[str, str] = {}
    return units_mapping


def CreateUnitSystemTemplate(manager):
    units_mapping_template = {"length": "m"}
    manager.SetTemplateUnitSystemByUnitsMapping(units_mapping_template)


def testUnitSystemManager(unit_manager, units_mapping_1, units_mapping_2, units_mapping_3) -> None:
    CreateUnitSystemTemplate(unit_manager)
    unit_manager.AddUnitSystem("system1", "system1", units_mapping_1, False)
    unit_manager.AddUnitSystem("system2", "system2", units_mapping_2, False)

    with pytest.raises(UnitSystemIDError):
        unit_manager.AddUnitSystem("system1", "system3", units_mapping_3, False)

    with pytest.raises(UnitSystemCategoriesError):
        unit_manager.AddUnitSystem("system3", "system3", units_mapping_3, False)

    scalar = Scalar("length", unit="cm")
    array = Array("length", unit="cm")
    fixed_array = FixedArray(3, "length", unit="cm")
    fraction_scalar = FractionScalar("length")

    unit_systems = unit_manager.GetUnitSystems()
    system1 = unit_systems["system1"]
    system2 = unit_systems["system2"]

    unit_manager.current = system1
    assert unit_manager.GetUnitSystemById("system1") is system1
    assert unit_manager.GetUnitSystemById("system2") is system2

    # make sure the unit system manager is not holding a strong ref to its objects
    scalar_ref = weakref.ref(scalar)
    array_ref = weakref.ref(array)
    fixed_array_ref = weakref.ref(fixed_array)
    fraction_scalar_ref = weakref.ref(fraction_scalar)

    del scalar
    del array
    del fixed_array
    del fraction_scalar

    assert scalar_ref() is None
    assert array_ref() is None
    assert fixed_array_ref() is None
    assert fraction_scalar_ref() is None


def testGetNewId(unit_manager, units_mapping_1) -> None:
    CreateUnitSystemTemplate(unit_manager)

    new_id = unit_manager.GetNewId()
    assert new_id == "system 1"
    unit_manager.AddUnitSystem(new_id, "system 1", units_mapping_1, False)

    assert unit_manager.GetNewId() == "system 2"
    unit_manager.RemoveUnitSystem("system 1")
    assert unit_manager.GetNewId() == "system 1"


def testCurrentUnitSystemUpdate(unit_manager, units_mapping_1) -> None:
    """
    If the current unit system is removed, another should be set
    """
    CreateUnitSystemTemplate(unit_manager)

    current = unit_manager.GetCurrent()
    assert current.GetId() is None

    # Adding
    unit_manager.AddUnitSystem("system 1", "system 1", units_mapping_1, False)

    # Since this is the first valid unit system we expect it to be set as current
    current_id = unit_manager.current.GetId()
    assert current_id == "system 1"

    # Adding another system, the current is not expected to change
    unit_manager.AddUnitSystem("system 2", "system 2", units_mapping_1, False)
    current_id = unit_manager.current.GetId()
    assert current_id == "system 1"

    # Removing the unit system set as current
    unit_manager.RemoveUnitSystem("system 1")

    # The second system should be set as default
    current_id = unit_manager.current.GetId()
    assert current_id == "system 2"

    # Also removing the second unit system
    unit_manager.RemoveUnitSystem("system 2")
    current_id = unit_manager.current.GetId()
    assert current_id is None


def testConvertToCurrent(unit_manager, units_mapping_1, units_mapping_2) -> None:
    CreateUnitSystemTemplate(unit_manager)

    units_mapping_3 = {"length": "cm"}

    system1 = unit_manager.AddUnitSystem("system1", "", units_mapping_1)
    system2 = unit_manager.AddUnitSystem("system2", "", units_mapping_2)
    system3 = unit_manager.AddUnitSystem("system3", "", units_mapping_3)

    def Convert(value, unit):
        return unit_manager.ConvertToCurrent("length", unit, value)

    def assertConversion(v1, v2):
        assert Convert(*v1) == v2
        prev_scalar = Scalar(v1)
        expected_scalar = Scalar(v2)
        obtained_scalar = unit_manager.ConvertScalarToCurrent(prev_scalar)
        assert obtained_scalar == expected_scalar

    # no current unit system: no conversion performed
    unit_manager.current = None
    assertConversion((100.0, "m"), (100.0, "m"))

    # unit system available: convert to current unit
    unit_manager.current = system1  # m
    assertConversion((100.0, "m"), (100.0, "m"))

    unit_manager.current = system2  # km
    assertConversion((100.0, "m"), (0.1, "km"))

    unit_manager.current = system3  # cm
    assertConversion((100.0, "m"), (10000.0, "cm"))


def testCreateUnitSystemWithoutTemplate(unit_manager, units_mapping_1) -> None:
    """
    It should be possible to create unit systems without a units template.
    """
    system1 = unit_manager.AddUnitSystem("system1", "", units_mapping_1)
    assert unit_manager.GetUnitSystemTemplate() is None

    unit_manager.GetCurrent()
    assert system1.GetId() == "system1"

    # However if a template is set then existing unit systems should respect it, and if any category
    # specified in the template is missing, then an error should be raised.
    units_mapping_template = {"pressure": "psi"}
    with pytest.raises(InvalidTemplateError):
        unit_manager.SetTemplateUnitSystemByUnitsMapping(units_mapping_template)


def testGetQuantityDefaultUnit(unit_manager, units_mapping_1) -> None:
    system1 = unit_manager.AddUnitSystem("system1", "", units_mapping_1)

    system1.SetDefaultUnit("length", "cm")
    quantity = ObtainQuantity(category="length", unit="m")

    default_unit = unit_manager.GetQuantityDefaultUnit(quantity)
    assert default_unit == "cm"


def testEmptyUnitSystemManager() -> None:
    """
    When no current unit system is selected the method GetCurrent should return an empty unit
    system.
    """
    unit_manager = UnitSystemManager()
    current = unit_manager.current

    assert current is not None
    assert isinstance(current, UnitSystem)

    assert current.GetId() is None
    assert current.GetCaption() == "Null"
    assert current.IsReadOnly()

    current_mapping = current.GetUnitsMapping()
    assert len(current_mapping) == 0
