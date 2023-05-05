import pytest
from pytest import approx
from pytest import raises

from barril.units import Scalar
from barril.units.unit_database import _LEGACY_TO_CURRENT


def testCubicFeetPerDayLegacyUnits() -> None:
    # test creating scalar using legacy representation and default category
    q = Scalar(1.0, "1000ft3/d")
    assert q.GetUnit() == "Mcf/d"

    # test creating scalar using legacy representation
    q = Scalar(category="volume flow rate", value=1.0, unit="1000ft3/d")
    assert q.GetUnit() == "Mcf/d"

    # test getting value using legacy representation
    assert approx(q.GetValue("M(ft3)/d")) == q.GetValue("MMcf/d")

    q = Scalar(category="volume flow rate", value=1.0, unit="M(ft3)/d")
    assert q.GetUnit() == "MMcf/d"
    assert approx(q.GetValue("M(ft3)/d")) == q.GetValue("MMcf/d")
    assert q.GetUnitName() == "million cubic feet per day"


@pytest.mark.parametrize("legacy, current", _LEGACY_TO_CURRENT)
@pytest.mark.parametrize("value", [1.0, 3.1415, 123.567])
def testAllLegacyUnits(legacy: str, current: str, value: float) -> None:
    test_scalar = Scalar(value, legacy)
    assert test_scalar.GetUnit() == current
    assert approx(test_scalar.GetValue(legacy)) == value
    assert approx(test_scalar.GetValue(current)) == value


def testCreateScalarUnitsError() -> None:
    from barril.units.unit_database import UnitsError

    with raises(UnitsError, match="Unable to get default category for: foo/d"):
        _ = Scalar(1.0, "foo/d")


def testGetValueInvalidUnitError() -> None:
    from barril.units.unit_database import InvalidUnitError

    with raises(
        InvalidUnitError, match="Invalid unit for quantity_type volume flow rate: 1000ft3/foo"
    ):
        q = Scalar(1.0, "1000ft3/d")
        q.GetValue("1000ft3/foo")


def testFixUnitIfIsLegacyExcept() -> None:
    from barril.units.unit_database import FixUnitIfIsLegacy

    class SomeNonExpectedObject:
        pass

    unknown = SomeNonExpectedObject()
    is_legacy, unit = FixUnitIfIsLegacy(unknown)  # type:ignore[arg-type]
    assert not is_legacy
    assert unit is unknown  # type:ignore[comparison-overlap]


def testUnitDatabaseConvert(unit_database_posc) -> None:
    import numpy as np

    # Test against float
    converted = unit_database_posc.Convert("volume flow rate", "1000ft3/d", "m3/d", 1.0)
    assert approx(converted) == 28.31685

    converted = unit_database_posc.Convert("volume flow rate", "M(ft3)/d", "m3/d", 1.0)
    assert approx(converted) == 28316.85

    # Test against numpy arrays
    converted = unit_database_posc.Convert("volume flow rate", "1000ft3/d", "m3/d", np.ones(2))
    assert approx(converted) == 28.31685
    converted = unit_database_posc.Convert("volume flow rate", "M(ft3)/d", "m3/d", np.ones(2))
    assert approx(converted) == 28316.85


def testUnitDatabaseGetUnitNameLegacy(unit_database_posc) -> None:
    assert (
        unit_database_posc.GetUnitName(quantity_type="volume flow rate", unit="M(ft3)/d")
        == "million cubic feet per day"
    )


def testUnitDatabaseCheckQuantityTypeUnitLegacy(unit_database_posc) -> None:
    from barril.units.unit_database import InvalidUnitError

    with raises(InvalidUnitError, match="Invalid unit for quantity_type volume flow rate"):
        unit_database_posc.CheckQuantityTypeUnit(quantity_type="volume flow rate", unit="M(ft3)/d")


def testUnitDatabaseGetDefaultCategory(unit_database_posc) -> None:
    category = unit_database_posc.GetDefaultCategory("1000ft3/d")
    assert category == "volume flow rate"

    class SomeNonExpectedObject:
        pass

    category = unit_database_posc.GetDefaultCategory(SomeNonExpectedObject())
    assert category is None


def testAddCategoryWithLegacyUnit(unit_database_posc) -> None:
    """Try creating a category with legacy unit"""
    unit_database_posc.AddCategory(
        category="molar-mass",
        quantity_type="mass per mol",
        valid_units=["g/mol", "kg/mol", "lb/lbmole"],
        default_value=100,
        min_value=0,
        is_min_exclusive=True,
        caption="Molar Mass",
    )
    valid_units = unit_database_posc.GetValidUnits("molar-mass")
    assert sorted(valid_units) == sorted(["g/mol", "kg/mol", "lb/lbmol"])


def testAddCategoryWithLegacyDefaultUnit(unit_database_posc) -> None:
    """Try creating a category with legacy default unit"""
    unit_database_posc.AddCategory(
        category="molar-mass",
        quantity_type="mass per mol",
        default_unit="lb/lbmole",
        default_value=100,
        min_value=0,
        is_min_exclusive=True,
        caption="Molar Mass",
    )
    valid_units = unit_database_posc.GetValidUnits("molar-mass")
    assert sorted(valid_units) == sorted(["g/mol", "kg/mol", "lb/lbmol"])
