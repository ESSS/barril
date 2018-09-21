from __future__ import absolute_import, division, unicode_literals

import pytest
from pytest import approx
import six
from six.moves import range, zip

from barril._foundation.odict import odict
from barril import units
from barril.units import Array, InvalidUnitError, ObtainQuantity, Quantity


def testEmptyArray():
    arr = Array.CreateEmptyArray()
    assert not arr.HasCategory()

    arr = arr.CreateCopy(category='temperature', unit='degC')
    assert arr.HasCategory()


def testValues():
    array = units.Array('length', values=[100, 150, 200], unit='m')
    assert array.unit == 'm'
    assert array.values == [100, 150, 200]

    array = array.CreateCopy(values=list(range(100)))
    array = array.CreateCopy(unit='km')
    assert array.values == [x / 1000.0 for x in range(100)]
    assert 3.0 / 1000.0 == array[3]

    with pytest.raises(AttributeError):
        array.values = 10


def testArrayWithNaNs(unit_database_len):
    import numpy
    TEST_VALUES = [
        [numpy.nan, 0, 15, numpy.nan],
        [numpy.nan] * 5,
    ]
    for values in TEST_VALUES:
        units.Array('flow rate', values=values, unit='m3/s')  # check that this does not raise exceptions


def testStr():
    array = units.Array('length', values=[100, 150, 200], unit='m')
    assert six.text_type(array) == '100 150 200 [m]'


def testConvertValuesFromArray():

    def CheckConversion(values):
        _array = units.Array('length', values=values, unit='m')
        for converted, original in zip(_array.GetValues('km'), values):
            assert converted == original / 1000

    from numpy import array
    CheckConversion(array([0.0, 1.123, 2.456, 3.789]))
    CheckConversion(array([0.0, 0.0]))


def testValues2():
    array = units.Array('length', values=[100, 150, 200], unit='m')
    array2 = units.Array('length', values=(100, 150, 200), unit='m')
    assert array == array2


def testEquality():
    a1 = units.Array('length', values=list(range(100)), unit='m')

    assert a1 == units.Array('length', values=list(range(100)), unit='m')
    assert a1 != units.Array('temperature', values=list(range(100)), unit='degC')
    assert a1 != units.Array('length', values=[], unit='m')
    assert a1 != units.Array('length', values=list(range(100)), unit='km')


def testMultiDimensional():
    a1 = units.Array('length', values=[(1000, 1000), (300, 300)], unit='m')
    assert a1.GetValues('km') == [(1, 1), (0.3, 0.3)]

    assert (1000, 1000) == a1[0]
    assert (300, 300) == a1[1]

    a1 = a1.CreateCopy(unit='km')
    assert (1, 1) == a1[0]
    assert (0.3, 0.3) == a1[1]


def testCreateWithQuantity():
    q = ObtainQuantity('m', 'length')
    a1 = units.Array(q, values=[(1000, 1000), (300, 300)])
    a2 = a1.CreateCopy(unit='km')

    assert a1.values == [(1000, 1000), (300, 300)]
    assert a2.values == [(1, 1), (0.3, 0.3)]


def testCategoryParameters(unit_database_len, mocker):
    unit_database = unit_database_len
    unit_database.AddUnit('temperature', 'Kelvin Degrees', 'degK', '%f - 273.5', '%f + 273.5')
    unit_database.AddCategory(
        'my temperature',
        'temperature',
        ['degC', 'degK'],
        default_unit='degC',
        default_value=22.3,
        min_value=-10.0,
        max_value=213.4,
        is_min_exclusive=False,
        is_max_exclusive=True,
    )

    a1 = units.Array('my temperature', values=[0, 100], unit='degC')
    assert a1.IsValid()

    a2 = a1.CreateCopy(values=[0, 220])
    assert a2._is_valid is None
    assert a2._validity_exception is None

    mocker.patch.object(a2, '_DoValidateValues', autospec=True)
    a2._DoValidateValues.side_effect = ValueError('my value error')

    assert not a2.IsValid()
    assert a2._is_valid is False
    assert six.text_type(a2._validity_exception) == 'my value error'
    assert a2._DoValidateValues.call_count == 1

    with pytest.raises(ValueError):
        a2.CheckValidity()

        # As result is already cached the "_DoValidateValues" will not be invoked.
        assert a2._DoValidateValues.call_count == 1

    a3 = units.Array('my temperature', values=[(-100, 50), (0, 2)], unit='degC')
    assert not a3.IsValid()


def testInvalidUnit():
    a1 = units.Array('length', values=[(1000, 1000), (300, 300)], unit='m')
    try:
        a1 = a1.CreateCopy(values=[(100, 200)], unit='foo')
    except InvalidUnitError:
        pass
    assert a1.values == [(1000, 1000), (300, 300)]
    assert a1.unit == 'm'


def testGetValues():
    '''
        Tests GetValues method return type when passing a 'unit'
    '''
    array = units.Array('temperature', values=[0, 100], unit='degC')
    assert isinstance(array.GetValues(), list)
    assert isinstance(array.GetValues('degC'), list)

    array = units.Array('temperature', values=(0, 100), unit='degC')
    assert isinstance(array.GetValues(), tuple)
    assert isinstance(array.GetValues('degC'), tuple)
    assert array[1] == 100

    array = units.Array('temperature', values=[], unit='degC')
    assert isinstance(array.GetValues('degC'), list)


def testCopy():
    array = units.Array('length', values=[0, 100], unit='m')
    copy = array.Copy()
    assert copy is array

    # test copy of subclasses
    class MyArray(units.Array):
        pass

    array = MyArray('length', values=[0, 100], unit='m')
    copy = array.Copy()
    assert isinstance(copy, MyArray)


def testArrayOperations(unit_database_len_time):
    unit_database = unit_database_len_time

    m = Quantity.CreateDerived(odict([('Table size', ['m', 1])]))
    km_city = Quantity.CreateDerived(odict([('City size', ['km', 1])]))

    s1 = Array.CreateWithQuantity(m, [1])
    s2 = Array.CreateWithQuantity(km_city, [0.01])
    initial1 = s1.GetQuantity().GetComposingUnits()
    initial2 = s2.GetQuantity().GetComposingUnits()
    # Check that they doesn't raise ComposedUnitError
    s1.GetValues()
    s2.GetValues()

    quantity, value = unit_database.Multiply(m, km_city, 1, 0.01)
    assert initial1 == s1.GetQuantity().GetComposingUnits()
    assert initial2 == s2.GetQuantity().GetComposingUnits()
    calculated1 = Array.CreateWithQuantity(quantity, [value])

    array = s1 * s2
    six.text_type(array)  # just to see if it works...
    assert calculated1 == s1 * s2

    quantity, value = unit_database.Sum(m, km_city, 1, 0.01)
    assert Array.CreateWithQuantity(quantity, [value]) == s1 + s2

    quantity, value = unit_database.Subtract(m, km_city, 1, 0.01)
    assert Array.CreateWithQuantity(quantity, [value]) == s1 - s2


def testDivision(unit_database_len_time):
    unit_database = unit_database_len_time
    m = Quantity.CreateDerived(odict([('Table size', ['m', 1])]))
    km_city = Quantity.CreateDerived(odict([('City size', ['km', 1])]))
    quantity, value = unit_database.Divide(m, km_city, 1, 0.01)
    calculated1 = Array.CreateWithQuantity(quantity, [value])
    s1 = Array.CreateWithQuantity(m, [1])
    s2 = Array.CreateWithQuantity(km_city, [0.01])
    assert calculated1 == s1 / s2


def testNumberInteractions(unit_database_len_time):
    import numpy

    m = Quantity.CreateDerived(odict([('Table size', ['m', 1])]))
    s1 = Array.CreateWithQuantity(m, list(range(10)))
    s2 = Array.CreateWithQuantity(m, [x + x for x in range(10)])
    assert s1 == 0 + s1
    assert s1 == s1 + 0
    assert s2 == s1 + s1

    num_arr = Array.CreateWithQuantity(m, numpy.array([x for x in range(10)]))
    sum_array = num_arr + s1
    assert isinstance(sum_array.values, numpy.ndarray)

    sum_array2 = num_arr + numpy.array([x for x in range(10)])
    assert isinstance(sum_array2.values, numpy.ndarray)

    tup_arr = Array.CreateWithQuantity(m, tuple([x for x in range(10)]))
    tup_arr = tup_arr + 1
    assert isinstance(tup_arr.values, tuple)


def testNumpyConversion():
    import numpy

    values = numpy.array([100, 200, 300])
    array = units.Array('length', values=values, unit='m')

    converted_values = array.GetValues('km')
    assert isinstance(converted_values, numpy.ndarray)
    assert list(numpy.array([0.1, 0.2, 0.3])) == list(converted_values)


def testNumpyMultiplicationOperation():
    import numpy

    units_array = units.Array('length', values=[100, 200, 300], unit='m')
    raw_array = [100, 200, 300]
    numpy_array = numpy.array([2.0, 0.5, 0.25])

    units_result = units_array * numpy_array
    raw_result = raw_array * numpy_array

    assert list(raw_result) == [200, 100, 75]
    assert list(units_result.GetValues('m')) == list(raw_result)


def testNoConversion():
    values = [100, 150, 200]
    array = units.Array('length', values=values, unit='m')
    assert array.GetValues() is values


def testNoConversionWhenUsingSameUnit():
    import numpy
    values = numpy.array([100, 150, 200])
    array = units.Array(values, 'm')
    assert array.GetValues('m') is values


def testZeroDimensionalNumpyArray():
    import numpy
    values = numpy.array(1000.0)
    array = units.Array(values, 'm')
    assert array.GetValues('m') == numpy.array(1000.0)
    assert array.GetValues('km') == numpy.array(1.0)


def testReadOnlyQuantity():
    quantity = ObtainQuantity('m', 'length')
    array = units.Array(quantity, values=[1, 2, 3])

    array = array.CreateCopy(unit='km')
    assert array.unit == 'km'
    assert approx(array.GetValues()) == [0.001, 0.002, 0.003]


def testCopyPropertiesAndValidation(unit_database_len):
    # Not raises exception because by default validation is False on the copy operation
    array_source = Array('flow rate', values=[-1, -2, -3], unit='m3/s')
    assert not array_source.IsValid()

    array_dest = array_source.CreateCopy()
    assert array_dest.values == [-1, -2, -3]


def testDefaultValues(unit_database_len):
    # Not raises exception because by default validation is False on the copy operation
    array = Array('flow rate')
    assert array.values == []

    array = Array(ObtainQuantity('m'))
    assert array.values == []

    with pytest.raises(AssertionError):
        Array(ObtainQuantity('m'), unit='m')
