from __future__ import absolute_import, unicode_literals

import six

from barril.units.unit_database import InvalidUnitError, UnitDatabase


#===================================================================================================
# _SimpleScalar
#===================================================================================================
class _SimpleScalar(object):

    def __init__(self, value, unit, category=None):
        self._value = value
        self._value_quantity = _ObtainQuantity(unit, category)
        self._unit = unit

    def GetValue(self, unit=None):
        return UnitDatabase.GetSingleton().Convert(
            self._value_quantity.GetQuantityType(),
            self._value_quantity.GetUnit(),
            unit or self._unit,
            self._value)

    def SetUnit(self, unit):
        self._unit = unit

    def SetValue(self, value, unit=None):
        self._value_quantity = _ObtainQuantity(unit or self._unit, self._value_quantity.GetCategory())
        self._value = value


_quantities_cache = {}


#===================================================================================================
# _ObtainQuantity
#===================================================================================================
def _ObtainQuantity(unit, category=None):
    if not category:
        unit_database = UnitDatabase.GetSingleton()
        category = unit_database.GetDefaultCategory(unit)
        if not category:
            raise InvalidUnitError(unit)

    key = (category, unit)
    quantity = _quantities_cache.get(key)
    if quantity is None:
        quantity = _quantities_cache.setdefault(key, _SimpleQuantity(category, unit))
    return quantity


#===================================================================================================
# _SimpleQuantity
#===================================================================================================
class _SimpleQuantity(object):

    def __init__(self, category, unit):
        self._category = category
        self._unit = unit

    def GetCategory(self):
        return self._category

    def GetQuantityType(self):
        unit_database = UnitDatabase.GetSingleton()
        return unit_database.GetCategoryQuantityType(self._category)

    def GetUnit(self):
        return self._unit

    def __str__(self):
        return 'Quantity(%s, %s)' % (self._category, self._unit)

    if six.PY2:
        __unicode__ = __str__
        del __str__


#===================================================================================================
# _ComposingQuantity
#===================================================================================================
class _ComposingQuantity(object):

    def __init__(self, category_to_unit_and_exps):
        self._category_to_unit_and_exps = category_to_unit_and_exps


def testScalarRefactor():
    quantity = _ObtainQuantity('m')
    quantity2 = _ObtainQuantity('m')
    assert 'Quantity(length, m)' == six.text_type(quantity)
    assert quantity is quantity2

    scalar = _SimpleScalar(10, 'm')
    assert 10 == scalar.GetValue('m')
    assert 10 == scalar.GetValue()
    assert 0.01 == scalar.GetValue('km')

    scalar.SetUnit('km')
    assert 10 == scalar.GetValue('m')
    assert 0.01 == scalar.GetValue()
    assert 0.01 == scalar.GetValue('km')

    scalar.SetValue(10)
    assert 10 == scalar.GetValue('km')
    assert 10 == scalar.GetValue()
    assert 10000 == scalar.GetValue('m')
