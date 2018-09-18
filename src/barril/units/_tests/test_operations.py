from __future__ import absolute_import, division, unicode_literals

import operator

import six
import pytest

from barril.units import ObtainQuantity
from barril.units.unit_database import UnitDatabase


def testOperation():
    unit_database = UnitDatabase.GetSingleton()
    unit_database.CheckDefaultUnitDatabase()
    q = ObtainQuantity(unit='m', category='length')

    SCALAR_OPERATION = [
        operator.add,
        operator.sub,
        operator.truediv,
        operator.mul,
        operator.mod,
    ]
    SCALAR_TYPES = [int, float]
    if six.PY2:
        SCALAR_TYPES.append(long)

    for operation in SCALAR_OPERATION:
        for cast_type in SCALAR_TYPES:
            # Left
            q2 = operation(cast_type(2), q)
            assert q2.GetQuantityType() == 'length'
            assert q2.GetUnit() == 'm'

            # Right
            q2 = operation(q, cast_type(2))
            assert q2.GetQuantityType() == 'length'
            assert q2.GetUnit() == 'm'

    q2 = abs(q)
    assert q2.GetQuantityType() == 'length'
    assert q2.GetUnit() == 'm'

    q2 = q + q
    assert q2.GetQuantityType() == 'length'
    assert q2.GetUnit() == 'm'

    q2 = q - q
    assert q2.GetQuantityType() == 'length'
    assert q2.GetUnit() == 'm'

    q2 = q * int(2)
    assert q2.GetQuantityType() == 'length'
    assert q2.GetUnit() == 'm'

    q2 = q * 2.0
    assert q2.GetQuantityType() == 'length'
    assert q2.GetUnit() == 'm'

    q2 = q * q
    assert q2.GetQuantityType() == '(length) ** 2'
    assert q2.GetUnit() == 'm2'

    q2 = q * q * q
    assert q2.GetQuantityType() == '(length) ** 3'
    assert q2.GetUnit() == 'm3'

    # Check pow
    q2 = q ** 1
    assert q2.GetQuantityType() == 'length'
    assert q2.GetUnit() == 'm'

    q2 = q ** 2
    assert q2.GetQuantityType() == '(length) ** 2'
    assert q2.GetUnit() == 'm2'

    q2 = q ** 3
    assert q2.GetQuantityType() == '(length) ** 3'
    assert q2.GetUnit() == 'm3'

    q2 = pow(q, 3)
    assert q2.GetQuantityType() == '(length) ** 3'
    assert q2.GetUnit() == 'm3'

    q2 = (q * q) / q
    assert q2.GetQuantityType() == 'length'
    assert q2.GetUnit() == 'm'

    q2 = (q * q) / ObtainQuantity(unit='d', category='time')
    assert q2.GetQuantityType() == '(length) ** 2 / time'
    assert q2.GetUnit() == 'm2/d'

    with pytest.raises(TypeError):
        operator.mul(q, 's')

