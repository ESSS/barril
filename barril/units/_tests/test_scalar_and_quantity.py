from __future__ import absolute_import, division, print_function, unicode_literals

from ben10.foundation.decorators import Implements
from ben10.interface import AssertImplements, ImplementsInterface
from coilib50.units import IObjectWithQuantity, IQuantity, IQuantity3, IScalar, Scalar
from coilib50.units.unit_database import UnitDatabase
import pytest


@ImplementsInterface(
    IQuantity,
    IQuantity3,
    IObjectWithQuantity,
    no_check=True
)
class _LightweightQuantity(object):
    '''
    A lightweight representation of a quantity. This class has the following purposes:

    1) To be a "model" implementation (or goal) for the current IQuantity interfaces.
       The current coilib50.units.Quantity implementation has some advanced features (used in
       very few places) that make it heavy and slow.

    2) To be checked, in terms of performance, against the full Quantity and against a tuple
       representation.

    .. see:: coilib50.units.Quantity

    This should be as lightweight as possible, storing only strings, and just the information
    needed: the unit (such as 'kg/m3') and the category (such as 'density').

    The LightweightQuantity also assumes that the used UnitDatabase is the singleton one.
    '''

    __slots__ = ['_unit', '_category']

    def __init__(self, unit, category):
        '''
        :param unicode unit:
            The unit name. It must be valid within that category.

        :param unicode category:
            A valid category.
        '''
        self._unit = unit
        self._category = category

    @Implements(IQuantity.GetCategory)
    def GetCategory(self):
        return self._category

    @Implements(IQuantity.GetUnit)
    def GetUnit(self):
        return self._unit

    @Implements(IQuantity.GetQuantityType)
    def GetQuantityType(self):
        category_info = self.GetUnitDatabase().GetCategoryInfo(self.GetCategory())
        return category_info.quantity_type

    @Implements(IObjectWithQuantity.GetQuantity)
    def GetQuantity(self):
        return self

    @Implements(IQuantity3.GetUnitDatabase)
    def GetUnitDatabase(self):
        return UnitDatabase.GetSingleton()


#===================================================================================================
# _LightweightScalar
#===================================================================================================
@ImplementsInterface(
    IScalar,
    IQuantity3,
    no_check=True,
)
class _LightweightScalar(tuple):  # Could derive from _LightweightQuantity, but this way is faster
    '''
    This is a lightweight version of a Scalar object. Should be as lightweight as a namedtuple,
    without events or any other kind of overhead. This class should be convertible to a full
    Scalar.

    Assumptions:
        - Uses the Singleton unit database
        - The category and the unit must be valid (will not be checked at initialization)
    '''

    __slots__ = []

    def __new__(cls, value, unit, category):
        return tuple.__new__(cls, (value, unit, category))

    @Implements(IScalar.GetValue)
    def GetValue(self, unit=None):
        assert unit is None or unit == self[1], 'LightweightScalar does not support unit conversion.'
        return self[0]

    @Implements(IScalar.GetValueAndUnit)
    def GetValueAndUnit(self):
        return (self[0], self[1])

    @Implements(IScalar.IsValid)
    def IsValid(self):
        return self.CheckValue(self[0])

    @Implements(IQuantity.GetCategory)
    def GetCategory(self):
        return self[2]

    @Implements(IQuantity.GetUnit)
    def GetUnit(self):
        return self[1]

    @Implements(IQuantity.GetQuantityType)
    def GetQuantityType(self):
        category_info = self.GetUnitDatabase().GetCategoryInfo(self[2])
        return category_info.quantity_type

    @Implements(IObjectWithQuantity.GetQuantity)
    def GetQuantity(self):
        return self

    @Implements(IQuantity3.GetUnitDatabase)
    def GetUnitDatabase(self):
        return UnitDatabase.GetSingleton()

    def __iter__(self):
        '''
        Allows unpacking this object into a (value, unit) tuple.
        '''
        return iter((self[0], self[1]))



def testCreationAndInterface():
    x = _LightweightScalar(value=1.0, unit='kg/m3', category='density')

    AssertImplements(x, IScalar)
    assert x.GetValue() == 1.0

    AssertImplements(x, IQuantity)
    assert x.GetUnit() == 'kg/m3'
    assert x.GetCategory() == 'density'
    assert x.GetQuantityType() == 'density'

    AssertImplements(x, IObjectWithQuantity)
    assert x.GetQuantity().GetUnit() == 'kg/m3'
    assert x.GetQuantity().GetCategory() == 'density'
    assert x.GetQuantity().GetQuantityType() == 'density'

def testConversionToFullScalar():
    y = _LightweightScalar(value=1.0, unit='kg/m3', category='density')
    x = Scalar(value=y.GetValue(), unit=y.GetUnit(), category=y.GetCategory())

    AssertImplements(x, IScalar)
    assert x.GetValue() == 1.0

    AssertImplements(x, IQuantity)
    assert x.GetUnit() == 'kg/m3'
    assert x.GetCategory() == 'density'
    assert x.GetQuantityType() == 'density'

    AssertImplements(x, IObjectWithQuantity)
    assert x.GetQuantity().GetUnit() == 'kg/m3'
    assert x.GetQuantity().GetCategory() == 'density'
    assert x.GetQuantity().GetQuantityType() == 'density'

    # Full Scalar supports conversion
    assert x.GetValue(unit='g/cm3') == 0.001

def testLazyChecking():
    from coilib50.units.unit_database import InvalidQuantityTypeError

    # Category 'meta density' does not exist
    x = _LightweightScalar(value=0.001, unit='kg/m3', category='meta density')

    # But the creation of _LightweightScalar does not check this...

    AssertImplements(x, IScalar)
    assert x.GetValue() == 0.001

    AssertImplements(x, IQuantity)
    assert x.GetUnit() == 'kg/m3'
    assert x.GetCategory() == 'meta density'

    # We will get the message error only when trying to get the related quantity type:
    with pytest.raises(InvalidQuantityTypeError):
        x.GetQuantityType()

def testGettingValueWithDifferentUnit():
    x = _LightweightScalar(value=0.001, unit='g/cm3', category='concentration')

    # But the creation of _LightweightScalar does not check this...

    AssertImplements(x, IScalar)
    assert x.GetValue() == 0.001
    assert x.GetValue('g/cm3') == 0.001
    assert x.GetValueAndUnit() == (0.001, 'g/cm3')

    AssertImplements(x, IQuantity)
    assert x.GetUnit() == 'g/cm3'
    assert x.GetCategory() == 'concentration'
    assert x.GetQuantityType() == 'density'

    # We will get an assertion error when trying to get the value with a different unit
    with pytest.raises(AssertionError):
        x.GetValue('kg/cm3')

def testUnpackingToValueAndUnit():
    x = _LightweightScalar(value=0.001, unit='g/cm3', category='concentration')

    value, unit = x

    assert value == 0.001
    assert unit == 'g/cm3'

def testQuantityCreationAndInterface():
    x = _LightweightQuantity(unit='kg/m3', category='concentration')

    AssertImplements(x, IQuantity)
    assert x.GetUnit() == 'kg/m3'
    assert x.GetCategory() == 'concentration'
    assert x.GetQuantityType() == 'density'

    AssertImplements(x, IObjectWithQuantity)
    assert x.GetQuantity().GetUnit() == 'kg/m3'
    assert x.GetQuantity().GetCategory() == 'concentration'
    assert x.GetQuantity().GetQuantityType() == 'density'

def testQuantityLazyChecking():
    from coilib50.units.unit_database import InvalidQuantityTypeError

    # Category 'meta density' does not exist
    x = _LightweightQuantity(unit='kg/m3', category='meta density')

    # But the creation of _LightweightQuantity does not check this...
    AssertImplements(x, IQuantity)
    assert x.GetUnit() == 'kg/m3'
    assert x.GetCategory() == 'meta density'

    # We will get the message error only when trying to get the related quantity type:
    with pytest.raises(InvalidQuantityTypeError):
        x.GetQuantityType()

