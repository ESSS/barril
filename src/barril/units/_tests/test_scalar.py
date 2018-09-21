'''
    REMARKS: Unicode
        The "unit" must not containt unicode character. All unit name and representation must use
        the standard ascii representation.
'''
from __future__ import absolute_import, division, unicode_literals

import pytest
from pytest import approx

import six

from barril._foundation.odict import odict
from barril import units
from barril.units import InvalidOperationError, InvalidUnitError, ObtainQuantity, Quantity, Scalar


def testScalarInterface(unit_database_well_length):
    s = Scalar('well-length')
    assert 0 == s.value
    assert 'm' == s.unit

def testQuantity(unit_database_well_length):
    Quantity('well-length', 'm')
    with pytest.raises(units.InvalidQuantityTypeError):
        Quantity('foo', 'm')

def testQuantityEq(unit_database_well_length):
    q0 = ObtainQuantity('m', 'well-length')
    q1 = ObtainQuantity('m', 'well-length')
    assert q0 == q1

def testReadOnlyQuantityCopy(unit_database_well_length):
    q0 = ObtainQuantity('m', 'well-length')
    q1 = q0.Copy()
    assert q0 == q1

def testScalar(unit_database_well_length):
    q = ObtainQuantity('m', 'well-length')
    s = Scalar.CreateWithQuantity(q, 10)

    assert 10 == s.value
    assert approx(abs(393.700787402-s.GetValue(unit='in')), 7) == 0

    s = s.CreateCopy(value=0.254, unit='in')
    assert 0.254 == s.value
    assert 'in' == s.unit
    assert 'well-length' == s.category

    with pytest.raises(AttributeError):
        setattr(s, 'value', 10)

def GetQuantity(unit='cm'):
    return units.ObtainQuantity(unit, 'well-length')

def testBadUnit(unit_database_well_length):
    x = units.Scalar.CreateWithQuantity(GetQuantity(), 500)
    with pytest.raises(units.InvalidUnitError):
        x.CreateCopy(unit='invalidUnit')

def testOperations(unit_database_well_length):
    x = units.Scalar.CreateWithQuantity(GetQuantity(), 500)
    assert x.value == 500
    assert x.unit == 'cm'

    assert x.GetValue('m') == 5
    assert x.unit == 'cm'
    assert x.GetValue('cm') == 500
    assert x.unit == 'cm'
    assert x.GetValue('km') == 0.005

def unit(value, unit='m'):
    return units.Scalar.CreateWithQuantity(GetQuantity(unit), value)

def testEq(unit_database_well_length):
    u1 = units.Scalar.CreateWithQuantity(GetQuantity(), 1.0)
    u2 = units.Scalar.CreateWithQuantity(GetQuantity(), 1.0)
    assert u1 == u2
    assert u1.unit == u2.unit
    assert 'cm' == u2.unit


def testAddUnit(unit_database_empty):
    unit_database = unit_database_empty
    unit_database.AddUnitBase('length', 'metre', 'm')
    RATIO = 0.0254
    unit_database.AddUnit(
        'length',
        'inch',
        'in',
        lambda x: 0.0254 * RATIO,
        lambda y: y / RATIO,
        default_category=None,
    )
    unit_database.AddCategory('length', 'length', override=True, valid_units=['m', 'in'])
    unit_database.AddCategory('depth', 'length', override=True, valid_units=['m', 'in'])

    a = units.Scalar('length', value=1.0, unit='m')
    b = units.Scalar('length', value=2.0, unit='m')
    c = units.Scalar('length', value=1.0, unit='in')
    d = units.Scalar('depth', value=1.0, unit='m')
    e = None
    f = units.Scalar('length', value=1.0, unit='m')

    assert a != b
    assert a != c
    assert a != e
    assert a != d

    assert a == f

def testValidUnits(unit_database_empty):
    # let'scalar clear up the unit manager
    unit_database = unit_database_empty

    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddUnit('length', 'centimeters', 'cm', '%f * 100.0', '%f / 100.0')
    unit_database.AddUnit('length', 'milimeters', 'mm', '%f * 1000.0', '%f / 1000.0')
    unit_database.AddUnit('length', 'kilometers', 'km', '%f / 1000.0', '%f * 1000.0')
    unit_database.AddUnit('length', 'miles', 'mi', '%f / 1609.347', '%f * 1609.347')
    unit_database.AddUnit('length', 'inches', 'in', '%f / 0.0254', '%f * 0.0254')

    valid_units = ['m', 'cm', 'mm']
    unit_database.AddCategory('length', 'length')
    unit_database.AddCategory('well-length', 'length', valid_units=valid_units)
    unit_database.AddCategory('well-diameter', 'length')

    Quantity('well-length', 'km')

    scalar = units.Scalar('well-length', 1, 'm')
    assert valid_units == scalar.GetValidUnits()

    scalar = units.Scalar('well-diameter', 1, 'm')
    assert ['m', 'cm', 'mm', 'km', 'mi', 'in'] == scalar.GetValidUnits()

    # Creating a scalar in a unit that isn't valid shouldn't raise an error and the unit
    # will be added to valid units
    scalar = units.Scalar('well-length', 1, 'mi')
    assert scalar.GetValidUnits() == ['m', 'cm', 'mm', 'mi']

def testScalarCopyAndRepresentation(unit_database_empty):
    unit_database = unit_database_empty

    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddUnit('length', 'milimeters', 'mm', 'x * 1000.0', 'x / 1000.0')
    unit_database.AddUnit('length', 'centimeters', 'cm', 'x * 100.0', 'x / 100.0')
    unit_database.AddCategory('well-diameter', 'length')
    s = Scalar('well-diameter', 10, 'm')

    assert "Scalar(10.0, 'm', 'well-diameter')" == repr(s)
    assert '10.0' == six.text_type(s.value)
    assert 'm' == s.unit
    assert 'well-diameter' == s.GetCategory()
    assert 'length' == s.GetQuantityType()

    s = s.CreateCopy(unit='cm')
    assert "Scalar(1000.0, 'cm', 'well-diameter')" == repr(s)
    assert "1000 [cm]" == six.text_type(s)

def testSort(unit_database_empty):
    db = unit_database_empty

    db.AddUnitBase('length', 'meters', 'm')
    db.AddUnit('length', 'centimeters', 'cm', 'x * 100.0', 'x / 100.0')
    db.AddCategory('length', 'length')

    s1 = Scalar('length', 10.0, 'cm')
    s2 = Scalar('length', 1.0, 'm')
    s3 = Scalar('length', 500.0, 'cm')
    s4 = Scalar('length', 10.0, 'm')

    x = [s2, s1, s4, s3]
    x.sort()
    assert x == [s1, s2, s3, s4]

def testCategoryParameters(unit_database_empty):
    db = unit_database_empty

    db.AddUnitBase('length', 'meters', 'm')
    db.AddUnit('length', 'centimeters', 'cm', 'x * 100.0', 'x / 100.0')

    db.AddCategory('my length', 'length', ['cm', 'm'], default_unit='m', default_value=18.5,
                   min_value=-30.0, max_value=100.0, is_min_exclusive=True, is_max_exclusive=False)

    s1 = Scalar('my length')
    assert s1.value == 18.5
    assert s1.unit == 'm'

    # test maximum boundary
    s2 = Scalar('my length', 100.0, 'm')
    assert s2.value == 100.0
    assert s2.unit == 'm'

    s3 = Scalar('my length', 500.0, 'cm')
    assert s3.value == 500.0
    assert s3.unit == 'cm'

    # higher than maximum value
    another = Scalar('my length', 120.0, 'm')
    assert not another.IsValid()
    with pytest.raises(ValueError):
        another.CheckValidity()

    another = Scalar('my length', -30.0, 'm')
    assert not another.IsValid()

    s4 = Scalar('my length', unit='cm')
    assert s4.value == 1850.0
    assert s4.unit == 'cm'

    another = s4.CreateCopy(12500.00, 'cm')
    assert not another.IsValid()

def testInvalidUnit(unit_database_empty):
    unit_database = unit_database_empty

    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddUnit('length', 'milimeters', 'mm', 'x * 1000.0', 'x / 1000.0')
    unit_database.AddUnit('length', 'centimeters', 'cm', 'x * 100.0', 'x / 100.0')
    unit_database.AddCategory('well-diameter', 'length')
    try:
        s = Scalar('well-diameter', 10, 'days')
        raise RuntimeError('Expecting error')
    except InvalidUnitError:
        pass

def testDerivedUnits(unit_database_empty):
    unit_database = unit_database_empty

    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddUnit('length', 'milimeters', 'mm', 'x * 1000.0', 'x / 1000.0')
    unit_database.AddUnit('length', 'centimeters', 'cm', 'x * 100.0', 'x / 100.0')
    unit_database.AddCategory('well-diameter', 'length')
    unit_database.AddUnitBase('time', 'seconds', 's')
    unit_database.AddCategory(category='Time', quantity_type='time')

    s1 = Scalar('well-diameter', 10, 'm')
    s2 = Scalar('well-diameter', 10, 'cm')
    s3 = Scalar('Time', 10, 's')

    assert Scalar('well-diameter', 10.10, 'm') == s1 + s2
    assert Scalar('well-diameter', 9.90, 'm') == s1 - s2

    quantity = Quantity.CreateDerived(odict())
    assert Scalar.CreateWithQuantity(quantity, 100) == s1 / s2
    assert Scalar('well-diameter', 9.90, 'm') == s1 - s2
    with pytest.raises(InvalidOperationError):
        s1.__sub__(s3)

def testCreationWithDerivedQuantity(unit_database_len_time):
    unit_database = unit_database_len_time

    m = Quantity.CreateDerived(odict([('Table size', ['m', 1])]))
    km_city = Quantity.CreateDerived(odict([('City size', ['km', 1])]))

    quantity, value = unit_database.Multiply(m, km_city, 1, 0.01)
    calculated1 = Scalar.CreateWithQuantity(quantity, value)
    assert six.text_type(calculated1)

    s1 = Scalar.CreateWithQuantity(m, 1)
    s2 = Scalar.CreateWithQuantity(km_city, 0.01)
    assert calculated1 == s1 * s2

def testNumberInteractions(unit_database_len_time):
    scalar = Scalar('Table size', 1, 'm')
    scalar2 = Scalar.CreateWithQuantity(Quantity.CreateDerived(odict()), 0)

    assert scalar == scalar + scalar2

    assert scalar == scalar + 0
    assert scalar == 0 + scalar

    assert 9 == (10 - scalar).value
    assert -9 == (scalar - 10).value

    assert 10 == (10 * scalar).value
    assert 10 == (scalar * 10).value

    assert 10 == (10.0 / scalar).value
    assert 1 / 10.0 == (scalar / 10.0).value

def testDivision(unit_database_len_time):
    unit_database = unit_database_len_time

    m = Quantity.CreateDerived(odict([('Table size', ['m', 1])]))
    km_city = Quantity.CreateDerived(odict([('City size', ['km', 1])]))
    quantity, value = unit_database.Divide(m, km_city, 1, 0.01)
    calculated1 = Scalar.CreateWithQuantity(quantity, value)
    s1 = Scalar.CreateWithQuantity(m, 1)
    s2 = Scalar.CreateWithQuantity(km_city, 0.01)
    assert calculated1 == s1 / s2

def testPow(unit_database_len_time):
    s = Scalar(2, 's', 'Time')
    spow = s ** 3
    assert spow.unit == 's3'
    assert spow.value == 8

def testFormatedUnitsOnScalar(unit_database_empty):
    '''
        Allow present units on get formatted Scalar
    '''
    unit_database = unit_database_empty
    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddCategory(category='length', quantity_type='length')

    class MyScalar(units.Scalar):
        pass

    scalar = MyScalar('length', 1.18, 'm')
    assert scalar.GetFormatted() == '1.18 [m]'

    MyScalar.SetFormattedValueFormat('%0.4f')
    MyScalar.SetFormattedSuffixFormat(' (%s)')

    # Tests the GET methods
    assert MyScalar.GetFormattedValueFormat() == '%0.4f'
    assert MyScalar.GetFormattedSuffixFormat() == ' (%s)'

    # Tests the Formatted method
    assert scalar.GetFormatted() == '1.1800 (m)'

    # Check for invalid format strings
    with pytest.raises(TypeError):
        MyScalar.SetFormattedValueFormat('%d [%s]')
    with pytest.raises(TypeError):
        MyScalar.SetFormattedSuffixFormat('%s %s')
    with pytest.raises(TypeError):
        MyScalar.SetFormattedSuffixFormat('%f')

    # When invalid format are set, the formats are not changed
    assert MyScalar.GetFormattedValueFormat() == '%0.4f'
    assert MyScalar.GetFormattedSuffixFormat() == ' (%s)'

    # Make sure we didn't affect the Scalar class, only the local MyScalar
    MyScalar.SetFormattedValueFormat('<<< %f')
    MyScalar.SetFormattedSuffixFormat(' [%s] >>>')
    scalar = Scalar('length', 1.18, 'm')
    assert scalar.GetFormatted() == '1.18 [m]'

def testEmptyScalar():
    '''
        ScalarMultiData exception when some of its scalars don't have a quantity_type
    '''
    # An empty scalar doesn't have a category defined
    scalar_1 = Scalar.CreateEmptyScalar(20.0)

    # When try to retrieve scalar value or unit a  exception was being raised
    assert scalar_1.GetValue('m') == 20.
    assert scalar_1.GetUnit() == ''

def testCopyProperties(unit_database_well_length):
    '''
        Test if the mehod SetValue is not called when copying the Scalar's properties.
    '''
    category = 'well-length'
    unit = 'm'
    value = 10.0

    scalar_source = Scalar(category, value, unit)
    scalar_dest = scalar_source.CreateCopyInstance()

    assert scalar_dest.GetCategory() == category
    assert scalar_dest.GetUnit() == unit
    assert scalar_dest.GetValue() == value

def testCopyPropertiesAndValidation(unit_database_well_length):
    category = 'well-length-with-min-and-max'  # the minimum value is zero
    unit = 'm'
    value = -1

    # Not raises exception because validation is False on the copy operation
    scalar_source = Scalar(category, value, unit)
    assert not scalar_source.IsValid()

    # Raises exception because validation is True and the value -1 is invalid accordingly to
    # the category 'well-length-with-min-and-max'
    another = scalar_source.CreateCopy()
    assert not another.IsValid()

def testDefaultValue(unit_database_len_pressure):
    '''
        Scalar constructor considers the minimum and maximum values
        when default_value is not defined
    '''
    db = unit_database_len_pressure

    db.AddCategory(
        category='my length',
        quantity_type='length',
        min_value=100.0,
        max_value=200.0,
    )

    # if the default value is not defined, the scalar should not try to set the initial/first
    # value of the new instance to 0.0, but it should assume the minimum allowed value.
    # should not raise ValueError
    length = Scalar('my length')
    assert length.GetValue() == 100.0

    length = Scalar(ObtainQuantity('m', 'my length'))
    assert length.GetValue() == 100.0

    length = Scalar(ObtainQuantity('m'))
    assert length.GetValue() == 0.0

    # invalid default value (< min)
    with pytest.raises(AssertionError):
        db.AddCategory(category='my pressure',
        quantity_type='pressure', default_value=50.0, min_value=100.0, max_value=200.0)

    # invalid default value (> max)
    with pytest.raises(AssertionError):
        db.AddCategory(category='my pressure',
        quantity_type='pressure', default_value=300.0, min_value=100.0, max_value=200.0)

    # invalid default value (<= min)
    with pytest.raises(AssertionError):
        db.AddCategory(category='my pressure',
        quantity_type='pressure', default_value=100.0, min_value=100.0, max_value=200.0,
        is_min_exclusive=True)

    # invalid default value (>= min)
    with pytest.raises(AssertionError):
        db.AddCategory(category='my pressure',
        quantity_type='pressure', default_value=200.0, min_value=100.0, max_value=200.0,
        is_max_exclusive=True)

    db.AddCategory(
        category='my pressure',
        quantity_type='pressure',
        min_value=100.0,
        max_value=200.0,
        default_value=150.0,
        is_min_exclusive=True,
        is_max_exclusive=False,
    )

    pressure = Scalar('my pressure')
    assert pressure.GetValue() == 150.0

    # default_value not informed. checking if the interval limits are respected
    # when is_min_exclusive or is_max_exclusive have been informed, so the default_value
    # must be
    with pytest.raises(RuntimeError):
        db.AddCategory(category='my pressure 2',
        quantity_type='pressure', min_value=100.0, max_value=200.0, is_max_exclusive=True)

def testScalarInvalidValue(unit_database_len_time):
    db = unit_database_len_time

    db.AddCategory('another-length', 'length', min_value=0, max_value=15)

    scalar = Scalar('another-length', value=15, unit='m')
    assert scalar.IsValid()

    scalar = Scalar('another-length', value=-5, unit='m')
    assert not scalar.IsValid()

    # By default the validation will be performed. 15 is a valid value.
    scalar = Scalar('another-length', value=15, unit='m')
    assert scalar.IsValid()

    # Even invalid ,the scalar returns the value, unit and a formatted text.
    another = Scalar('another-length', value=3000, unit='m')
    assert not another.IsValid()
    assert another.GetValue('m') == 3000
    assert another.GetUnit() == 'm'
    assert another.GetFormatted() == '3000 [m]'

    # By default the validation will be performed, and in this cases will raise ValueError.
    another_2 = Scalar('another-length', unit='m', value=5000)
    assert not another_2.IsValid()

    # Performing copy between invalid scalars. The validation is not performed on copy.
    copied = another.CreateCopy(unit='cm')
    assert not copied.IsValid()
    assert copied.GetValue('m') == 3000
    assert copied.GetUnit() == 'cm'
    assert copied.GetFormatted() == '300000 [cm]'


def testScalarValidUnits(unit_database_empty):
    db = unit_database_empty
    db.AddUnit('length', 'milimeters', 'mm', '%f * 1000.0', '%f / 1000.0')
    db.AddUnitBase('length', 'meters', 'm')
    db.AddUnit('length', 'centimeters', 'cm', '%f * 100.0', '%f / 100.0')
    db.AddUnit('length', 'kilometers', 'km', '%f / 1000.0', '%f * 1000.0')
    db.AddCategory('len1', 'length', valid_units=['mm', 'cm'])
    db.AddCategory('len2', 'length', valid_units=['m', 'km'])

    s1 = Scalar('len1', 1, 'mm')
    assert s1 is not None

    s2 = Scalar('len2', 1, 'mm')
    assert s2 is not None

def testScalarRepresentation(unit_database_posc):
    s1 = Scalar(0.5, 'kg/kg', 'dimensionless')
    s2 = Scalar(0.125, 'g/g', 'mass concentration')

    assert s1.GetCategory() == 'dimensionless'
    assert s2.GetCategory() == 'mass concentration'

    assert repr(s1) == "Scalar(0.5, 'kg/kg', 'dimensionless')"
    assert repr(s2) == "Scalar(0.125, 'g/g', 'mass concentration')"

def testScalarCreationModes():
    base = Scalar(10, 'm')

    assert Scalar('length', 10, 'm') == base
    assert Scalar((10.0, 'm')) == base

    with pytest.raises(AssertionError):
        Scalar('length', 1.0)  # missing unit

def testScalarPickle(unit_database_posc):

    import pickle
    simple_scalar = Scalar('length', 10, 'm')
    simple_scalar2 = pickle.loads(pickle.dumps(simple_scalar))
    assert simple_scalar == simple_scalar2

    complex_scalar = Scalar('length', 10, 'm') * Scalar('time', 5, 's')
    complex_scalar2 = pickle.loads(pickle.dumps(complex_scalar))
    assert complex_scalar == complex_scalar2

def testScalarHashEq():
    scalar1 = Scalar('length', 10, 'm')
    scalar2 = Scalar('length', 10, 'm')
    scalar3 = Scalar('length', 10, 'cm')
    scalar4 = Scalar('length', scalar2.GetValue('cm'), 'cm')

    assert scalar1 == scalar2
    assert hash(scalar1) == hash(scalar2)
    assert hash(scalar1) == hash(scalar1)
    assert scalar2 != scalar3
    assert hash(scalar2) != hash(scalar3)
    assert scalar3 != scalar4
    assert hash(scalar4) != hash(scalar3)

