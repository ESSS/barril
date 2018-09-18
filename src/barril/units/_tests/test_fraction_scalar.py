from __future__ import absolute_import, division, unicode_literals

import copy

import pytest

from barril import units
from barril.basic.fraction import FractionValue

def testFractionScalar():
    # create our scalar
    f = units.FractionScalar('length', value=FractionValue(250, (3, 4)), unit='m')

    # check formatting
    assert f.GetFormatted() == '250 3/4 [m]'

    # check conversion
    # f.unit = 'km'
    assert f.GetValue('km') == FractionValue(0.25, (3 / 1000.0, 4))
    assert f.GetValue('m') == FractionValue(250.0, (3, 4))

    # test no fraction part
    f = f.CreateCopy(value=FractionValue(0.25), unit='km')
    assert f.value == FractionValue(0.25)
    assert f.GetFormatted() == '0.25 [km]'

    # set fraction again
    f = f.CreateCopy(value=FractionValue(250, (3, 4)), unit='m')
    assert f.GetValue('km') == FractionValue(0.25, (3 / 1000.0, 4))
    assert f.GetFormatted() == '250 3/4 [m]'
    assert f.GetValue('m') == FractionValue(250, (3, 4))

    f = f.CreateCopy(value=FractionValue(0.25, (3, 4)), unit='km')
    assert f.value == FractionValue(0.25, (3, 4))
    assert f.GetFormatted() == '0.25 3/4 [km]'
    assert f.GetValue('m') == FractionValue(250.0, (3000, 4))

    with pytest.raises(AttributeError):
        setattr(f, 'value', 10)


def testCopy():
    f = units.FractionScalar('length', value=FractionValue(250.0, (3, 4)), unit='m')
    c = copy.copy(f)
    assert c.value == FractionValue(250.0, (3, 4))

def testEquality():

    def Create(number, fraction):
        return units.FractionScalar('length', value=FractionValue(number, fraction), unit='m')

    assert Create(250, (3, 4)) == Create(250, (3, 4))
    assert not Create(250, (3, 4)) != Create(250, (3, 4))

    assert Create(100, (3, 4)) != Create(250, (3, 4))
    assert not Create(100, (3, 4)) == Create(250, (3, 4))

    a = units.FractionScalar('length', value=1.0, unit='m')
    b = units.FractionScalar('length', value=2.0, unit='m')
    c = units.FractionScalar('length', value=1.0, unit='in')
    d = units.FractionScalar('depth', value=1.0, unit='m')
    e = None
    f = units.FractionScalar('length', value=1.0, unit='m')

    assert a != b
    assert a != c
    assert a != e
    assert a != d

    assert a == f

def testRepr():
    assert repr(FractionValue(250, (3, 4))) == 'FractionValue(250, 3/4)'

def testFormatValue():
    f = units.FractionScalar('length', value=FractionValue(250.0, (3, 4)), unit='m')
    assert f.GetFormattedValue() == "250 3/4"

def testComparison():

    f1 = units.FractionScalar('length', value=FractionValue(10), unit='in')
    f3 = units.FractionScalar('volume', value=FractionValue(4), unit='m3')
    with pytest.raises(TypeError):
        f1 < f3

    f2 = units.FractionScalar('length', unit='in')
    f1 = f1.CreateCopy(value=FractionValue(250, (1, 2)), unit='m')
    f2 = f2.CreateCopy(value=FractionValue(220, (3, 4)), unit='m')

    assert f1 > f2
    assert f2 < f1

def testFractionScalarConversion():
    db = units.UnitDatabase()
    db.AddUnit('length', 'milimeters', 'mm', '%f * 1000.0', '%f / 1000.0')
    db.AddUnitBase('length', 'meters', 'm')

    f = units.FractionScalar('length', value=FractionValue(3, (1, 2)), unit='m')

    converted = db.Convert('length', 'm', 'mm', f.value)
    assert converted == FractionValue(3500)

def testFractionScalarInvalidValue(unit_database_len):
    db = unit_database_len

    db.AddCategory('another-length', 'length', min_value=5, max_value=15)

    scalar = units.FractionScalar('another-length', value=FractionValue(1, (1, 5)), unit='m')
    assert not scalar.IsValid()
    with pytest.raises(ValueError):
        scalar.CheckValidity()

    # By default the validation will be performed, 10 is a valid value
    scalar = scalar.CreateCopy(value=FractionValue(10))
    assert scalar.IsValid()

    # Even invalid ,the scalar returns the value, unit and a formatted text.
    another = units.FractionScalar('another-length', value=FractionValue(3000), unit='m')
    assert not another.IsValid()
    assert another.GetValue('m') == FractionValue(3000)
    assert another.GetUnit() == 'm'
    assert another.GetFormatted() == '3000 [m]'

    # By default the validation will be performed, and in this cases will raise ValueError.
    another_2 = scalar.CreateCopy(value=FractionValue(5000))
    assert not another_2.IsValid()

    another_3 = units.FractionScalar('another-length', unit='m', value=FractionValue(5000))
    assert not another_3.IsValid()

    # Performing copy between invalid fraction scalars. The validation is not performed on copy.
    copied = another.Copy()
    assert not copied.IsValid()
    assert copied.GetValue('m') == FractionValue(3000)
    assert copied.GetUnit() == 'm'
    assert copied.GetFormatted() == '3000 [m]'

def testSetFloatValue():
    '''
    The fraction scalar should accept a float-convertible value. Since the fraction is a subclass
    from scalar, it should be able to respect the same interface.
    '''
    f = units.FractionScalar('length', value=FractionValue(0), unit='in')
    f = f.CreateCopy(value=0.75)
    assert f.GetValue('in') == FractionValue(0.75)

def testFractionScalarWithDefaultValueOnCategory(unit_database_len):
    '''
    FractionScalar is not considering the default value from category on initialization
    '''
    db = unit_database_len

    db.AddCategory('my length', 'length', default_value=FractionValue(5, (1, 2)))

    scalar = units.FractionScalar('my length', unit='m')
    assert scalar.GetValue('m') == FractionValue(5, (1, 2))
    assert scalar.GetUnit() == 'm'
    assert scalar.GetFormatted() == '5 1/2 [m]'

