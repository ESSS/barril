from __future__ import absolute_import, unicode_literals

from coilib50 import units
from coilib50.units import InvalidUnitError

import pytest


def testValues(unit_database_len_temp):
    table = units.UnitTable(['length', 'temperature'])
    assert table.units == ('m', 'degC')
    values = [
        (1.0, 14.1),
        (3.0, 16.2),
        (4.3, -3.5)
    ]
    table.SetValues(values, units=('m', 'degC'))

    assert table.values[1] == (3.0, 16.2)
    assert table.units == ('m', 'degC')

    with pytest.raises(InvalidUnitError):
        table.SetValues([(1.1, 2.2)], units=('degC', 'm'))

    table.units = ('km', 'degC')

    assert table.values == [
        (1.0e-3, 14.1),
        (3.0e-3, 16.2),
        (4.3e-3, -3.5)
    ]

    # test SetValues passing the units (one of them the current, as None)
    table.SetValues([(1.0e-3, 15.0), (2.0e-3, 30.0)], units=(None, 'K'))
    assert table.units == ('km', 'degC')  # the current units don't change
    assert table.values == [(1.0e-3, 15.0 - 270), (2.0e-3, 30.0 - 270)]

    # test GetValues passing the units (one of them the current, as None)
    table.units = ('km', 'K')
    assert table.GetValues(units=('m', None)) == [(1.0, 15.0), (2.0, 30.0)]

def testEmpty():
    table = units.UnitTable(['length', 'temperature'])
    assert table.values == []

    values = [
        (1.0, 14.1),
        (3.0, 16.2),
        (4.3, -3.5)
    ]
    table.SetValues(values, units=('m', 'degC'))
    table.SetValues([])  # try to empty the table
    assert table.values == []

def testInitWithWrongUnits():
    table = units.UnitTable(['length', 'temperature'])
    table.units = ('m', 'y')
    values = [
        (1.0, 14.1),
        (3.0, 16.2),
        (4.3, -3.5)
    ]
    with pytest.raises(InvalidUnitError):
        table.SetValues(values)

def testCopy():
    table = units.UnitTable(['length', 'temperature'])
    values = [
        (1.0, 14.1),
        (3.0, 16.2),
        (4.3, -3.5)
    ]
    table.SetValues(values)

    other_table = table.Copy()

    assert other_table.GetValues() == values


