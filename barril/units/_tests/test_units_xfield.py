from __future__ import absolute_import, unicode_literals

import pytest

from coilib50.basic.fraction import FractionValue
from coilib50.subject import Subject
from coilib50.units import FractionScalar, Scalar
from coilib50.units.unit_database import InvalidUnitError
from coilib50.units.units_xfield import XFractionScalar, XScalar


def testXScalar():
    scalar = Scalar('length', 10, 'm')

    field = XScalar(scalar)
    assert field.CreateInstance() is scalar

    new_scalar = field.CreateInstance(10)
    assert new_scalar is not scalar
    assert new_scalar.value == 10
    assert new_scalar.unit == scalar.unit
    assert new_scalar.category == scalar.category

    new_scalar = field.ConvertValue(scalar, 20)
    assert new_scalar is not scalar
    assert new_scalar.value == 20
    assert new_scalar.unit == scalar.unit
    assert new_scalar.category == scalar.category

    new_scalar = field.ConvertValue(scalar, (20, 'cm'))
    assert new_scalar is not scalar
    assert new_scalar.value == 20
    assert new_scalar.unit == 'cm'
    assert new_scalar.category == scalar.category

    new_scalar = field.ConvertValue(scalar, (20, 'cm', 'depth'))
    assert new_scalar is not scalar
    assert new_scalar.value == 20
    assert new_scalar.unit == 'cm'
    assert new_scalar.category == 'depth'

    # Explicit category change is allowed, even though it is not usual.
    new_value = Scalar('pressure', 0.0, 'psi')
    new_scalar = field.ConvertValue(scalar, new_value)
    assert new_scalar is new_value
    assert new_scalar.value == 0
    assert new_scalar.unit == 'psi'
    assert new_scalar.category == 'pressure'


def testXScalarWithUnitDatabase(unit_database_posc):
    unit_db = unit_database_posc
    
    # Beware when using custom categories. It is possible to set values outside of set of valid
    # units. The example below exposes this with an example.
    unit_db.AddCategory(
        category='my_pressure',
        quantity_type='pressure',
        valid_units=['Pa'],
        default_unit='Pa'
    )
    
    scalar = Scalar('my_pressure', 10.0, 'Pa')
    field = XScalar(scalar)
    
    new_value = Scalar('my_pressure', 15.0, 'Pa')
    new_scalar = field.ConvertValue(scalar, new_value)
    assert new_scalar is new_value
    assert new_scalar.value == 15.0
    assert new_scalar.unit == 'Pa'
    assert new_scalar.category == 'my_pressure'

    new_scalar = field.ConvertValue(new_scalar, (20.0, 'psi'))
    assert new_scalar.value == 20.0
    assert new_scalar.unit == 'psi'
    assert new_scalar.category == 'my_pressure'

    # Also note that it is possible to change a field's category implicitly. This can be very
    # dangerous and the example below exposes this.
    new_value = Scalar(30.0, 'Pa')  # Default category will be 'pressure'
    new_scalar = field.ConvertValue(new_scalar, new_value)  # Override the category implicitly
    assert new_scalar.value == 30.0
    assert new_scalar.unit == 'Pa'
    assert new_scalar.category == 'pressure'


def testSubjectWithXScalar():

    class MySubject(Subject):

        Subject.Properties(
            scalar1=XScalar(),
            scalar2=XScalar('pressure'),
            scalar3=Scalar('pressure'),
        )

    sub = MySubject()
    assert sub.scalar1 == Scalar.CreateEmptyScalar()
    assert sub.scalar2 == Scalar('pressure')
    assert sub.scalar3 == Scalar('pressure')

    sub.scalar1 = 2.0
    assert sub.scalar1.value == 2.0
    assert sub.scalar1.unit == ''
    assert sub.scalar1.category == ''

    sub.scalar2 = 2.0, 'psi'
    assert sub.scalar2.value == 2.0
    assert sub.scalar2.unit == 'psi'
    assert sub.scalar2.category == 'pressure'

    with pytest.raises(InvalidUnitError):
        sub.SetScalar2((2.0, 'cm'))

    sub.scalar2 = 2.0, 'cm', 'depth'
    assert sub.scalar2.value == 2.0
    assert sub.scalar2.unit == 'cm'
    assert sub.scalar2.category == 'depth'

    sub.scalar3 = 3.0, 'bar'
    assert sub.scalar3.value == 3.0
    assert sub.scalar3.unit == 'bar'
    assert sub.scalar3.category == 'pressure'

    changes = []

    def Modified(sender, change, **kwargs):
        changes.append(change)

    sub.RegisterModified(Modified)
    sub.scalar1 = 3.0
    assert changes == [{'scalar1': (Scalar.CreateEmptyScalar(3.0), Scalar.CreateEmptyScalar(2.0))}]

    changes = []
    sub.scalar1 = 1.0, 'cm', 'length'
    sub.scalar2 = 2.0
    sub.scalar3 = 2.0, 'bar'
    # Expecting only two changes, since the scalar2 is already equal to 2.0
    assert len(changes) == 2
    assert changes == \
        [
            {'scalar1': (Scalar('length', 1.0, 'cm'), Scalar.CreateEmptyScalar(3.0))},
            {'scalar3': (Scalar('pressure', 2.0, 'bar'), Scalar('pressure', 3.0, 'bar'))},
        ]

    changes = []
    sub.BeginModify()
    sub.scalar1 = 0.0, 'cm'
    sub.scalar2 = 2.0, 'm'
    sub.scalar3 = 0.0, 'bar'
    sub.EndModify()
    # Expecting only two changes, since the scalar2 is already equal to 2.0
    assert len(changes) == 1
    changes = changes[0]
    assert changes['scalar1'] == ((Scalar('length', 0.0, 'cm'), Scalar('length', 1.0, 'cm')))
    assert changes['scalar2'] == ((Scalar('depth', 2.0, 'm'), Scalar('depth', 2.0, 'cm')))
    assert changes['scalar3'] == ((Scalar('pressure', 0.0, 'bar'), Scalar('pressure', 2.0, 'bar')))


def testXFractionScalar():
    scalar = FractionScalar(10, 'm')

    field = XFractionScalar(scalar)
    assert field.CreateInstance() == scalar

    new_scalar = field.CreateInstance(10)
    assert not new_scalar is scalar
    assert new_scalar.value == FractionValue(10)
    assert new_scalar.unit == scalar.unit
    assert new_scalar.category == scalar.category

    new_scalar = field.ConvertValue(scalar, 20)
    assert not new_scalar is scalar
    assert new_scalar.value == FractionValue(20)
    assert new_scalar.unit == scalar.unit
    assert new_scalar.category == scalar.category

    new_scalar = field.ConvertValue(scalar, (20, 'cm'))
    assert not new_scalar is scalar
    assert new_scalar.value == FractionValue(20)
    assert new_scalar.unit == 'cm'
    assert new_scalar.category == scalar.category

    new_scalar = field.ConvertValue(scalar, (20, 'cm', 'depth'))
    assert not new_scalar is scalar
    assert new_scalar.value == FractionValue(20)
    assert new_scalar.unit == 'cm'
    assert new_scalar.category == 'depth'

    new_value = FractionScalar('pressure', 0.0, 'psi')
    new_scalar = field.ConvertValue(scalar, new_value)
    assert new_scalar is new_value
    assert new_scalar.value == FractionValue(0)
    assert new_scalar.unit == 'psi'
    assert new_scalar.category == 'pressure'
