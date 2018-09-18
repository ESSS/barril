from __future__ import absolute_import, unicode_literals

import six
import pytest
from pytest import approx

from barril._foundation.odict import odict
from barril import units
from barril.units import InvalidUnitError, ObtainQuantity, Quantity


def testFormatting(unit_database_start_units):
    point = units.FixedArray(2, 'length', [(100, 150), (50, 50)], 'm')
    assert '(100, 150) (50, 50) [m]' == six.text_type(point)

def testValues(unit_database_start_units):
    with pytest.raises(ValueError):
        units.FixedArray(1, 'length', [100], 'm')
    point = units.FixedArray(3, 'length', [100, 150, 200], 'm')
    assert point.unit == 'm'
    assert point.values == [100, 150, 200]
    assert point.dimension == 3

    # check dimension read-only
    def SetDimensions():
        point.dimension = 4

    with pytest.raises(AttributeError):
        SetDimensions()

    # check number of values
    with pytest.raises(ValueError):
        point.CreateCopy(values=[0, 0])
    with pytest.raises(ValueError):
        point.CreateCopy(values=[0, 0, 0, 0])
    point = point.CreateCopy(values=[50, 80, 90])  # OK

    # check conversion
    assert point.GetValues('m') == [50, 80, 90]

    assert approx(point.GetValues('km')) == [0.050, 0.080, 0.090]

    assert '50 80 90 [m]' == six.text_type(point)

    with pytest.raises(AttributeError):
        setattr(point, 'values', [50, 80, 90])

def testInvalidUnits(unit_database_start_units):
    point = units.FixedArray(2, 'length', [(100, 150), (50, 50)], 'm')
    try:
        point = point.CreateCopy(values=[(20, 30), (40, 50)], unit='foo')
    except InvalidUnitError:
        pass

    assert point.values == [(100, 150), (50, 50)]
    assert point.unit == 'm'

def testCreateWithQuantity(unit_database_start_units):
    units.FixedArray.CreateWithQuantity(Quantity.CreateDerived(odict()), [100, 150, 200], dimension=3)

    quantity = ObtainQuantity('m', 'length')
    a1 = units.FixedArray(3, quantity, values=[1, 2, 3])
    a2 = units.FixedArray(3, quantity, values=[1, 2, 3])

    assert a1.GetValues('km') == [0.001, 0.002, 0.003]
    assert a2.GetValues() == [1, 2, 3]

def testCopy(unit_database_start_units):
    point = units.FixedArray(3, 'length', [100, 150, 200], 'm')
    assert point.Copy() == point

#         other = units.FixedArray(3, 'length', [1, 2, 3], 'km')
    other = point.CreateCopy()
    assert other == point

    # test copy with subclasses
    class MyFixedArray(units.FixedArray):
        pass

    point = MyFixedArray(3, 'length', [100, 150, 200], 'm')
    assert isinstance(point.Copy(), MyFixedArray)

    point = units.FixedArray(3, 'length', [100, 150, 200], 'm')

def testEmptyArray(unit_database_start_units):
    arr = units.FixedArray.CreateEmptyArray(3)
    assert not arr.HasCategory()
    assert arr.category == ''
    assert arr.unit == ''

    arr = arr.CreateCopy(category='length', unit='m')
    assert arr.HasCategory()
    assert arr.category == 'length'
    assert arr.unit == 'm'

def testReadOnlyQuantity(unit_database_start_units):
    quantity = ObtainQuantity('m', 'length')
    array = units.FixedArray(3, quantity, values=[1, 2, 3])
    assert approx(array.GetValues('km')) == [0.001, 0.002, 0.003]

def testDefaultValues(unit_database_start_units):
    # Not raises exception because by default validation is False on the copy operation
    array = units.FixedArray(3, 'length')
    assert array.values == [0.0, 0.0, 0.0]

    array = units.FixedArray(3, ObtainQuantity('m'))
    assert array.values == [0.0, 0.0, 0.0]

    with pytest.raises(AssertionError):
        units.FixedArray(3, ObtainQuantity('m'), unit='m')

def testTupleCreation(unit_database_start_units):
    """
    Make sure we can use tuples as values.
    """
    array = units.FixedArray(3, (0.0, 200.0, 300.0), 'm')
    assert units.FixedArray(3, 'length', (0.0, 200.0, 300.0), 'm') == array

def testFixedArrayPickle(unit_database_start_units):
    import pickle
    fixed_array_1 = units.FixedArray(3, 'length', values=[1, 2, 3], unit='m')
    fixed_array_2 = pickle.loads(pickle.dumps(fixed_array_1))

    assert fixed_array_1 == fixed_array_2


def testNumberInteractions():
    # Operations on FixedArrays used to return Array instances.
    a = units.FixedArray(3, [1, 2, 3], 'm')
    b = units.FixedArray(3, [0.5] * 3, 'm')

    s = a + b
    assert isinstance(s, units.FixedArray)
    assert s.GetDimension() == 3

    m = a + b
    assert isinstance(m, units.FixedArray)
    assert m.GetDimension() == 3


def testFixedArrayChangingIndex():
    fixed_array = units.FixedArray(3, [1, 2, 3], 'm')
    assert fixed_array.ChangingIndex(0, 5) == units.FixedArray(3, [5, 2, 3], 'm')
    assert fixed_array.ChangingIndex(0, units.Scalar(5, 'm')) == units.FixedArray(3, [5, 2, 3], 'm')
    assert fixed_array.ChangingIndex(0, (5,)) == units.FixedArray(3, [5, 2, 3], 'm')

    # Different unit
    assert fixed_array.ChangingIndex(0, (5, 'cm')) == units.FixedArray(3, [5, 200, 300], 'cm')
    assert fixed_array.ChangingIndex(0, units.Scalar(5, 'cm')) == units.FixedArray(3, [5, 200, 300], 'cm')

    # Keeping fixed array unit
    assert fixed_array.ChangingIndex(0, units.Scalar(5, 'cm'), use_value_unit=False) == units.FixedArray(3, [0.05, 2, 3], 'm')

    # Other indexes
    assert fixed_array.ChangingIndex(1, units.Scalar(5, 'cm')) == units.FixedArray(3, [100, 5, 300], 'cm')
    assert fixed_array.ChangingIndex(2, units.Scalar(5, 'cm')) == units.FixedArray(3, [100, 200, 5], 'cm')


def testFixedArrayIndexAsScalar():
    from barril.units import Scalar
    fixed_array = units.FixedArray(3, 'length of path', [1, 2, 3], 'm')
    assert fixed_array.IndexAsScalar(0).GetCategory() == 'length of path'
    assert fixed_array.IndexAsScalar(0) == Scalar('length of path', 1, 'm')
    assert fixed_array.IndexAsScalar(1) == Scalar('length of path', 2, 'm')
