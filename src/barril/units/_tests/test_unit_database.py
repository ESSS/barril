# coding: UTF-8
from __future__ import absolute_import, division, unicode_literals

import pytest
from pytest import approx

from six.moves import range

from barril import units
from barril.basic.format_float import FormatFloat
from barril.basic.fraction import FractionValue
from barril.units import (
    UNKNOWN_QUANTITY_TYPE, UNKNOWN_UNIT, Array, FixedArray, InvalidQuantityTypeError,
    InvalidUnitError, ObtainQuantity, Quantity, UnitsError)
from barril.units.unit_database import UnitDatabase


def testNotDefaultUnitDatabase():
    unit_database = units.UnitDatabase()
    with pytest.raises(AssertionError):
        unit_database.CheckDefaultUnitDatabase()

def testDefaultUnitDatabase(unit_database):
    unit_database.CheckDefaultUnitDatabase()

def testConv(unit_database_empty):
    unit_database = unit_database_empty

    # add some units for testing
    unit_database.AddUnitBase('temperature', 'Celcius', 'ºC')
    unit_database.AddUnit('temperature', 'Fahrenheit', 'F', '%f * 1.8 + 32.0', ' (%f - 32.0) / 1.8')
    unit_database.AddUnit('temperature', 'Kelvin', 'K', '%f + 273.15', '%f - 273.15')
    unit_database.AddUnit('temperature', 'Rakini', 'R', '%f * 1.8 + 32 + 459.67', '(%f - 32 - 459.67) / 1.8')

    assert 50 == unit_database.Convert('temperature', 'ºC', 'F', 10)
    assert 10 == unit_database.Convert('temperature', 'F', 'ºC', 50)
    assert approx(abs(-245.372222-unit_database.Convert('temperature', 'R', 'ºC', 50)), 5) == 0
    assert approx(abs(581.67-unit_database.Convert('temperature', 'ºC', 'R', 50)), 7) == 0

    assert [50, 50, 50] == unit_database.Convert('temperature', 'ºC', 'F', [10, 10, 10])
    assert [10, 10, 10] == unit_database.Convert('temperature', 'F', 'ºC', [50, 50, 50])
    assert (10, 10, 10) == unit_database.Convert('temperature', 'F', 'ºC', (50, 50, 50))

def testPrecision():
    unit_database = units.UnitDatabase()
    unit_database.AddUnitBase('Compressibility', '1/Bars', '1/Bars')
    unit_database.AddUnit    ('Compressibility', '1/Psi', '1/Psi', frombase='%f / 14.50377', tobase='%f * 14.50377')
    unit_database.AddUnit    ('Compressibility', '1/Atm', '1/Atm', frombase='%f / 0.986923', tobase='%f * 0.986923')

    assert approx(abs(14.50377 * 10e-6-unit_database.Convert('Compressibility', '1/Psi', '1/Bars', 1 * 10e-6)), 5) == 0
    assert approx(abs(0.000063816588-unit_database.Convert('Compressibility', '1/Psi', '1/Bars', 4.4e-006)), 5) == 0

def testQuantityTypes(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion
    real = unit_database.GetQuantityTypes()
    real.sort()
    assert real == [UNKNOWN_QUANTITY_TYPE, 'length', 'temperature']

def testUnitQuantityType(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion
    assert 'length' == unit_database.GetQuantityType('m')

def testDistanceUnits(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion
    available_units = ['m', 'mm', 'cm', 'km', 'mi', 'in', 'µm']
    real = unit_database.GetUnits('length')
    assert available_units == real

def testFindCase(unit_database_custom_conversion):
    unit_database = units.UnitDatabase()
    # add some units for testing
    unit_database.AddUnitBase('temperature', 'mang1', 'mA')
    unit_database.AddUnit('temperature', 'mang2', 'Ma', frombase='%f', tobase='%f')
    unit_database.AddUnit('temperature', 'Celsius', 'C', frombase='%f', tobase='%f')
    unit_database.AddUnit('temperature', 'mang3', 'MA', frombase='%f', tobase='%f')

    unit_database.AddCategory('my', 'temperature')
    with pytest.raises(AssertionError):
        unit_database.FindUnitCase('my', 'ma')
    assert 'C' == unit_database.FindUnitCase('my', 'c')
    assert 'C' == unit_database.FindUnitCase('my', 'C')

def testUnits(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion
    real = unit_database.GetUnits()
    real.sort()
    available_units = [UNKNOWN_UNIT, 'm', 'mm', 'cm', 'km', 'mi', 'in', 'µm', 'ºC', 'F', 'K']
    available_units.sort()
    assert available_units == real

def testBaseUnit(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion
    assert 'm' == unit_database.GetBaseUnit('length')

def testUnitNames(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion
    names = set(['meters', 'milimeters', 'centimeters', 'kilometers', 'miles', 'inches', 'micrometers'])
    onames = set(unit_database.GetUnitNames('length'))
    assert names == onames

def testClear(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion
    unit_database.Clear()
    with pytest.raises(units.InvalidQuantityTypeError):
        unit_database.CheckQuantityType('length')

def testCategory(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion
    unit_database.AddCategory('my length', 'length', ['mm', 'm'],
                                   default_unit='m', default_value=15.5,
                                   min_value=-6e-10, max_value=2e5,
                                   is_min_exclusive=True, is_max_exclusive=False,
                                   caption='My Length')

    assert unit_database.GetDefaultValue('my length') == 15.5
    assert unit_database.GetDefaultUnit('my length') == 'm'
    assert sorted(list(unit_database.IterCategories())) == ['length', 'my length']

    quantity = ObtainQuantity('m', 'my length')
    formatted_value = FormatFloat('%g', -6e-010)
    with pytest.raises(ValueError, match="Invalid value for My Length: %s. Must be > %s." % (formatted_value, formatted_value)):
        quantity.CheckValue(-6e-10)

    quantity.CheckValue(0)  # without specifying unit
    mm_quantity = ObtainQuantity('mm', 'my length')
    mm_quantity.CheckValue(2e5)

    with pytest.raises(ValueError, match="Invalid value for My Length: 200000. Must be <= 200000.0."):
        mm_quantity.CheckValue(2e8 + 1,)

    # Check the unit info using a category instead a quantity_type
    with pytest.raises(InvalidQuantityTypeError):
        unit_database.GetInfo('unknown length', 'mm')

    unit_database.GetInfo('my length', 'mm')
    unit_database.GetInfo(UNKNOWN_QUANTITY_TYPE, 'I know it is m3', fix_unknown=True)

def testUniqueness(unit_database_custom_conversion):
    # trying to re-register milimeters (mm)
    unit_database = unit_database_custom_conversion
    with pytest.raises(RuntimeError):
        unit_database.AddUnit('length', 'milimeters', 'mm', '%f * 1000.0', '%f / 1000.0')

def testDefaultUnitWhenNoneIsPassed(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion
    unit_database.AddCategory('my category', 'length', ['mm'], default_unit='mm')
    # Quantity without specifying unit, must use category's default unit and not raise
    default_when_none = ObtainQuantity(None, 'my category')
    assert ObtainQuantity('mm', 'my category') == default_when_none

def testDefaultUnitValid(unit_database_custom_conversion):
    '''
    Test the situation where a category does not have the base unit among its valid units
    '''
    unit_database = unit_database_custom_conversion
    unit_database.AddCategory('my category', 'length', ['mm'])
    assert unit_database.GetCategoryInfo('my category').default_unit == 'mm'

def testConvertionWithExponent(unit_database_custom_conversion):
    '''
    Test conversions with different exponents.
    '''
    unit_database = unit_database_custom_conversion
    assert approx(abs(100-unit_database.Convert('length', [('m', 1)], [('cm', 1)], 1)), 5) == 0
    assert approx(abs(10000-unit_database.Convert('length', [('m', 2)], [('cm', 2)], 1)), 5) == 0

    # Doesn't make sense changing the exponent in the from and to
    with pytest.raises(ValueError):
        unit_database.Convert('length', [('m', 2)], [('m', 1)], 1)

def testAddCategory(unit_database_custom_conversion):
    '''
    Testing if AddCategory gives an error if trying to register twice.
    '''
    unit_database = unit_database_custom_conversion
    unit_database.AddCategory(
        'my category',
        'length',
        valid_units=['mm', 'm', 'cm'],
        default_unit='mm'
    )
    with pytest.raises(
        UnitsError):
        unit_database.AddCategory('my category',
        'length',
        ['mm'],
        default_unit='mm')

    unit_database.AddCategory(
        'derived category',
        'length',
    )

    # Create a preferred unit set for categories
    assert unit_database.GetValidUnits('my category') == ['mm', 'm', 'cm']
    assert unit_database.GetValidUnits('derived category') == ['m', 'mm', 'cm', 'km']

def testValidUnits(unit_database_custom_conversion):
    '''
    Test while registering a category that passing None as valid_units returns the
    units of the quantity type.
    '''
    unit_database = unit_database_custom_conversion
    unit_database.AddCategory('length', 'length', override=True)
    info = unit_database.AddCategory('my category', 'length', default_unit='mm')
    length_units = unit_database.GetUnits('length')
    assert info.valid_units == None
    assert unit_database.GetValidUnits('my category') == length_units

def testConvertQuantityTypeCheck(unit_database_custom_conversion):
    '''
    Check for bug when trying to convert a unit to the same unit, but passing
    an invalid quantity type as argument.
    '''
    unit_database = unit_database_custom_conversion
    with pytest.raises(InvalidQuantityTypeError):
        unit_database.Convert('XXX', 'm', 'mm', 100)
    with pytest.raises(InvalidUnitError):
        unit_database.Convert('length', 'XXX', 'm', 100)
    with pytest.raises(InvalidUnitError):
        unit_database.Convert('length', 'm', 'XXX', 100)

def testCheckValidUnits(unit_database_custom_conversion):
    '''
    Make sure we check if the given valid_units are actually valid for that quantity_type
    '''
    unit_database = unit_database_custom_conversion
    with pytest.raises(ValueError):
        unit_database.AddCategory('my category', 'length', default_unit='mm', valid_units='foooo')

def testDiscoverCloseUnitMatches():
    unit_database = UnitDatabase.CreateDefaultSingleton()
    assert unit_database.FindSimilarUnitMatches('kg/day') == ['kg/d']
    assert unit_database.FindSimilarUnitMatches('bbls/d') == ['bbl/d', 'bbl/d2']
    assert unit_database.FindSimilarUnitMatches('mg/l') == ['mg/L']

def testDefaultCaption():
    unit_database = UnitDatabase.CreateDefaultSingleton()
    category_info = unit_database.GetCategoryInfo('angle per volume')
    assert category_info.caption == 'Angle per Volume'

def testAddCategoryBasedOnCategory(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion
    unit_database.AddCategory('my category', 'length', valid_units=['mm', 'm'], default_unit='mm', default_value=0.5)

    unit_database.AddCategory('my category 2', from_category='my category', valid_units=['mm'])
    assert unit_database.GetValidUnits('my category 2') == ['mm']

    unit_database.AddCategory('my category 3', from_category='my category', default_unit='m')
    assert unit_database.GetDefaultUnit('my category 3') == 'm'

    unit_database.AddCategory('my category 4', from_category='my category', default_value=0.8)
    assert unit_database.GetDefaultValue('my category 4') == 0.8
    assert unit_database.GetValidUnits('my category 4') == ['mm', 'm']

def testConvertFractionValues(unit_database_custom_conversion):
    '''
    Test unit database handling fraction values.
    '''
    db = unit_database_custom_conversion

    # Converting half meter to cm
    value = FractionValue(0, (1, 2))

    value = db.Convert('length', 'm', 'cm', value)
    assert float(value) == 50

def testRegisterTwoFunctionsForTheSameClass(unit_database_custom_conversion):
    '''
    Test the behavior when we attempt to register two convert functions for the same class
    '''
    def ConvertFunction1(*args, **kwargs):
        return 0

    db = unit_database_custom_conversion
    # There is a function specialized in convert fraction values. Attempting to register another
    # function should raise an error

    value = FractionValue(0, (1, 2))
    db.Convert('length', 'm', 'cm', value)

    with pytest.raises(
        AssertionError):
        db.RegisterAdditionalConversionType(FractionValue, ConvertFunction1)

def testNumpyConversion(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion

    from barril.units.posc import MakeBaseToCustomary, MakeCustomaryToBase
    f_unit_to_base = MakeCustomaryToBase(273.15, 1, 1, 0)
    f_base_to_unit = MakeBaseToCustomary(273.15, 1, 1, 0)
    unit_database.AddUnit('My Temperature', 'degrees Celsius', 'degC', f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(2298.35, 5, 9, 0)
    f_base_to_unit = MakeBaseToCustomary(2298.35, 5, 9, 0)
    unit_database.AddUnit('My Temperature', 'degree Fahrenheit', 'degF', f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0, 1, 1, 0)
    f_base_to_unit = MakeBaseToCustomary(0, 1, 1, 0)
    unit_database.AddUnit('My Temperature', 'my Kelvin', 'myK', f_base_to_unit, f_unit_to_base, default_category=None)

    unit_database.AddCategory(
        'My Temperature',
        quantity_type='My Temperature',
        valid_units=['myK', 'degC', 'degF'],
        default_unit='myK',
        default_value=2,
        min_value=0,
        max_value=15,
        is_min_exclusive=False,
        is_max_exclusive=False,
        caption='My Temperature',
    )

    import numpy
    values = numpy.array(list(range(10, 13)), numpy.float32)
    arr = Array('My Temperature', values, 'degC')
    obtained = arr.GetValues('degF')

    expected = [49.99995041, 51.79994965, 53.5999527]
    assert approx(obtained) == expected

def testNumpyWithMinMax(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion
    unit_database.AddCategory(
        'my length',
        'length',
        ['mm', 'm'],
        default_unit='m',
        default_value=2,
        min_value=0,
        max_value=15,
        is_min_exclusive=False,
        is_max_exclusive=False,
        caption='My Length',
    )
    import numpy
    values = numpy.array(list(range(10)), numpy.float32)
    Array('my length', values, 'mm')

    values = numpy.array(list(range(20000, 20010)), numpy.float32)
    # Raise validation error
    another = Array('my length', values, 'mm')
    assert not another.IsValid()
    with pytest.raises(ValueError):
        another.CheckValidity()

    # Don't raise validation error if validate = False.
    arr = Array('my length', values, 'mm')
    assert not arr.IsValid()

    another = arr.CreateCopy(values=values, unit='mm')
    assert not another.IsValid()

    # Same checks on FixedArray.
    values = numpy.array(list(range(10)), numpy.float32)
    FixedArray(len(values), 'my length', values, 'mm')

    values = numpy.array(list(range(20000, 20010)), numpy.float32)
    # Raise validation error
    another = FixedArray(len(values), 'my length', values, 'mm')
    assert not another.IsValid()

    # Don't raise validation error if validate = False.
    arr = FixedArray(len(values), 'my length', values, 'mm')
    assert not arr.IsValid()

    another = arr.CreateCopy(values=values, unit='mm')
    assert not another.IsValid()

def testInvalidUnitCategoryDoesntGenerateError(unit_database_custom_conversion):
    unit_database = unit_database_custom_conversion
    with pytest.raises(
        ValueError):
        unit_database.AddCategory('my invalid length',
        'length',
        caption='Invalid length',

        # This is not a valid unit
        default_unit='Mm',

        min_value=0,
        max_value=99999.0,
        is_min_exclusive=False,
        is_max_exclusive=False,
        valid_units=['mm', 'm'],)

def testGetValidUnitsEmptyQuantity(unit_database_custom_conversion):
    '''
    Test that retrieving the valid units for the category of the empty quantity (as created
    by Quantity.CreateEmpty() correctly returns an empty list.
    '''
    unit_database = unit_database_custom_conversion
    quantity = Quantity.CreateEmpty()
    assert unit_database.GetValidUnits(quantity.GetCategory()) == []

