from __future__ import absolute_import, unicode_literals

import pytest

from barril._foundation.odict import odict
from barril.units import InvalidOperationError, InvalidUnitError, ObtainQuantity, Quantity


def testDerivedQuantities(unit_database_len_time):
    # define a simple quantity
    _q1 = ObtainQuantity(unit='s', category='Time')  # see if it works
    _q2 = ObtainQuantity(unit='m', category='Table size')  # see if it works
    q3 = Quantity.CreateDerived(odict([('Table size', ['m', 2]), ('Time', ['s', -1])]))
    q4 = Quantity.CreateDerived(odict([('Table size', ['m', 2]), ('Time', ['s', -2])]))
    q5 = Quantity.CreateDerived(odict([('Table size', ['m', 1]), ('City size', ['m', 1]), ('Time', ['s', -2])]))
    q6 = Quantity.CreateDerived(odict([('Time', ['s', -2])]))
    q7 = Quantity.CreateDerived(odict([('Table size', ['m', 1]), ('Time', ['s', 2])]))

    with pytest.raises(InvalidUnitError):
        Quantity.CreateDerived(odict([('Table size', ['invalid', 1]),
         ('City size', ['m', 1]), ('Time', ['s', -2])]))

    assert '(Table size) ** 2 / Time' == q3.GetCategory()
    assert 'm2/s' == q3.GetUnit()

    assert '(Table size) ** 2 / (Time) ** 2' == q4.GetCategory()
    assert 'm2/s2' == q4.GetUnit()
    assert '1/s2' == q6.GetUnit()
    assert 'm.s2' == q7.GetUnit()

    assert (('m', 2), ('s', -2)) == q4.GetComposingUnits()
    assert (('m', 1), ('m', 1), ('s', -2)) == q5.GetComposingUnits()

def testConvertionWithDerivedUnits(unit_database_len_time):
    empty = Quantity.CreateDerived(odict())
    m = Quantity.CreateDerived(odict([('Table size', ['m', 1])]))
    m_city = Quantity.CreateDerived(odict([('City size', ['m', 1])]))
    cm = Quantity.CreateDerived(odict([('Table size', ['cm', 1])]))
    km_city = Quantity.CreateDerived(odict([('City size', ['km', 1])]))
    m2 = Quantity.CreateDerived(odict([('Table size', ['m', 2])]))
    s = Quantity.CreateDerived(odict([('Time', ['s', -1])]))
    m2s = Quantity.CreateDerived(odict([('Table size', ['m', 2]), ('Time', ['s', -1])]))
    cat_mix_m2 = Quantity.CreateDerived(odict([('Table size', ['m', 1]), ('City size', ['m', 1])]))

    unit_database = unit_database_len_time
    # multiplication
    assert (m2, 2) == unit_database.Multiply(m, m, 1, 2)
    assert (m2s, 2) == unit_database.Multiply(m2, s, 1, 2)
    assert (m2s, 2) == unit_database.Multiply(m2, s, 1, 2)
    assert (m2, 1) == unit_database.Multiply(m, cm, 1, 100)
    assert (cat_mix_m2, 1) == unit_database.Multiply(m, m_city, 1, 1)
    assert (cat_mix_m2, 1) == unit_database.Multiply(m, km_city, 1, 0.001)

    # division
    assert (m, 0.001) == unit_database.Divide(cat_mix_m2, km_city, 1, 1)
    # check division with cancelling units (and different categories)
    assert (empty, 1) == unit_database.Divide(m, m_city, 1, 1)

    # sum
    assert (m, 1 + 0.01) == unit_database.Sum(m, cm, 1, 1)
    assert (m, 2) == unit_database.Sum(m, m_city, 1, 1)

    # subtraction
    # check with operation so that we have an exact match (without need for almost equals,
    # as that should be the same exact operation done later)
    assert (m, 1 - 0.01) == unit_database.Subtract(m, cm, 1, 1)
    with pytest.raises(InvalidOperationError):
        unit_database.Subtract(m, s, 1, 1)

def testDeepcopy(unit_database_len_time):
    import copy

    # Note: the part below is flaky for a test because it relies on getting a refcount to None
    # which could change if there are other threads running. The code is kept just as a
    # reference in case we have to debug such a situation again (there was a bug in odict where
    # it decreased references to None when it shouldn't and it crashed the program later on).

    # m = odict([('Table size', ['m', 1])])
    # import gc
    # import sys
    # my_none = None
    # for i in range(100):
    #     gc.collect()
    #
    # Note:
    # for i in range(200):
    #     gc.collect()
    #     if i < 100:
    #         prev = sys.getrefcount(my_none)
    #     else:
    #         curr = sys.getrefcount(my_none)
    #         self.assert_(curr >= prev,
    #             'The ref count cannot get lower for None (previous:%s current:%s).' % (prev, curr))
    #
    #     # Notice that print sys.getrefcount(None) is always decrementing (this is the error)
    #     m = copy.deepcopy(m)

    m = Quantity.CreateDerived(odict([('Table size', ['m', 1])]))
    m0 = copy.deepcopy(m)
    assert m is m0  # Check if our cache is working.

def testReadOnlyOperation(unit_database_len_time):
    unit_database = unit_database_len_time
    m_ro = ObtainQuantity('m', 'Table size')
    m_rw = ObtainQuantity('m', 'Table size')

    m2 = Quantity.CreateDerived(odict([('Table size', ['m', 2])]))

    # multiplication
    assert (m2, 2) == unit_database.Multiply(m_rw, m_rw, 1, 2)
    assert (m2, 2) == unit_database.Multiply(m_ro, m_rw, 1, 2)
    assert (m2, 2) == unit_database.Multiply(m_ro, m_ro, 1, 2)
    assert (m2, 2) == unit_database.Multiply(m_rw, m_ro, 1, 2)

    quantity, _ = unit_database.Multiply(m_ro, m_ro, 1, 2)
    assert isinstance(quantity, Quantity)

    quantity, _ = unit_database.Multiply(m_rw, m_rw, 1, 2)
    assert isinstance(quantity, Quantity)
    quantity, _ = unit_database.Multiply(m_rw, m_ro, 1, 2)
    assert isinstance(quantity, Quantity)
    quantity, _ = unit_database.Multiply(m_ro, m_rw, 1, 2)
    assert isinstance(quantity, Quantity)
