from __future__ import absolute_import, unicode_literals

from barril.units import ObtainQuantity, Quantity, UnitDatabase
import pytest


def testReadOnlyQuantity(unit_database_empty):
    unit_database = unit_database_empty

    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddUnit('length', 'centimeters', 'cm', '%f * 100.0', '%f / 100.0')
    unit_database.AddCategory('length', 'length')

    read_only_quantity = ObtainQuantity('m', 'length')
    with pytest.raises(AttributeError):
        read_only_quantity.SetUnit('cm')

    # When creating a copy of a read only quantity we'll make it not read only anymore!
    copy = read_only_quantity.MakeCopy(Quantity)
    assert copy.GetUnitDatabase() is unit_database

def testMultiplyReadOnlyQuantity():
    '''
    Raising an Error when Geometry quantity is read only (...)

    This test simulates the conditions of the bug report. This bug has been fixed before I try
    to reproduce here.
    '''
    unit_database = UnitDatabase.GetSingleton()

    meters = ObtainQuantity('m', 'length')

    r_quantity, _value = unit_database.Multiply(meters, meters, 1.0, 1.0)
    assert r_quantity.GetUnit() == 'm2'

