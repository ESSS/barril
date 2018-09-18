# -*- coding: cp1252 -*-
from __future__ import absolute_import, unicode_literals

import six
import pytest
from pytest import approx

from barril._foundation.reraise import Reraise
from barril import units
from barril.units import UnitsError
from barril.units.unit_database import UnitDatabase


def testPoscWithoutFillCategories(unit_database_posc_len_no_category):
    unit_database = unit_database_posc_len_no_category

    unit_database.AddCategory('my_len', 'length')

    # this category does not exist because we didn't fill the categories
    with pytest.raises(UnitsError):
        units.Scalar('length', 100, 'km')

    u1 = units.Scalar('my_len', 100, 'km')
    u2 = units.Scalar('my_len', 100000, 'm')
    assert approx(abs(u1.value-u2.GetValue('km')), 7) == 0

def testMegagramPerCubicMeterToKilogramPerCubicMeter():
    unit_database = UnitDatabase.CreateDefaultSingleton()
    expected = 1000
    obtained = unit_database.Convert('density', 'Mg/m3', 'kg/m3', 1)
    assert obtained == expected

def testDivisionError():
    unit_database = UnitDatabase.CreateDefaultSingleton()
    for category, category_info in six.iteritems(unit_database.categories_to_quantity_types):
        base_unit = category_info.default_unit
        for unit in unit_database.GetValidUnits(category):
            for i in [-1, 0, 1]:
                try:
                    unit_database.Convert(category, base_unit, unit, i)
                except Exception as e:
                    Reraise(e, 'Error converting: from: %s to: %s' % (base_unit, unit))

                try:
                    unit_database.Convert(category, unit, base_unit, i)
                except Exception as e:
                    Reraise(e, 'Error converting: from: %s to: %s' % (unit, base_unit))

def testScfPerBblToM3ToM3():
    unit_database = UnitDatabase.CreateDefaultSingleton()
    expected = 0.17776487178535644
    obtained = unit_database.Convert('standard volume per volume', 'scf/bbl', 'scm(15C)/m3', 1.0)
    assert approx(abs(obtained-expected), 7) == 0

