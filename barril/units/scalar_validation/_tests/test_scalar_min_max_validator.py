from __future__ import absolute_import, unicode_literals

from barril.units import Scalar
from barril.units.scalar_validation.scalar_min_max_validator import ScalarMinMaxValidator


def _CreateTestCategories(db):
    db.AddCategory(
        category='test category',
        quantity_type='dimensionless',
        override=True,
        default_unit='-',
        min_value=1.0,
        max_value=50.0,
        valid_units='-',
        is_min_exclusive=False,
        is_max_exclusive=False,
    )

    db.AddCategory(
        category='category exclusive',
        quantity_type='dimensionless',
        override=True,
        default_unit='-',
        min_value=1.0,
        max_value=50.0,
        valid_units='-',
        is_min_exclusive=True,
        is_max_exclusive=True,
        default_value=5.0
    )

def testScalarValidationMsgs(unit_database):

    def _Check(scalar, value, unit, expected_msg):
        some_scalar = scalar.CreateCopy(value=value, unit=unit)
        obtained_msg = \
            ScalarMinMaxValidator.CreateScalarCheckErrorMsg(some_scalar, 'Some Property')
        assert obtained_msg == expected_msg

    _CreateTestCategories(unit_database)

    some_scalar = Scalar('test category', 10.0, '-')

    # Test value below minimum -----------------------------------------------------------------
    expected_error_msg = \
        'Error in Some Property. Invalid value for Test Category: 0. Must be greater or equal to 1.0.'
    _Check(some_scalar, 0.0, '-', expected_error_msg)

    # Test value above maximum -----------------------------------------------------------------
    expected_error_msg = \
        'Error in Some Property. Invalid value for Test Category: 51. Must be less or equal to 50.0.'
    _Check(some_scalar, 51.0, '-', expected_error_msg)

    # Test no error without exclusive ----------------------------------------------------------
    _Check(some_scalar, 1.0, '-', None)
    _Check(some_scalar, 50.0, '-', None)

    # Test using min and max exclusive ---------------------------------------------------------
    some_scalar = Scalar('category exclusive', 10.0, '-')

    # Test value below minimum -----------------------------------------------------------------
    expected_error_msg = \
        'Error in Some Property. Invalid value for Category Exclusive: 1. Must be greater than 1.0.'
    _Check(some_scalar, 1.0, '-', expected_error_msg)

    # Test value above maximum -----------------------------------------------------------------
    expected_error_msg = \
        'Error in Some Property. Invalid value for Category Exclusive: 50. Must be less than 50.0.'
    _Check(some_scalar, 50.0, '-', expected_error_msg)

    # Test no error with exclusive -------------------------------------------------------------
    _Check(some_scalar, 49.0, '-', None)
    _Check(some_scalar, 2.0, '-', None)

