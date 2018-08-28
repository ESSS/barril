'''
B{Unit Management}

It is very common within an application (especially on engineering applications) to have
several different values within the application, regarding pressure, density, etc. But just
having the values without any scope is something that can be meaningless, as that value only
makes sense if we have a unit and we know what it relates to.

This module is designed to help the application manage those values and units, based on the
following B{requisites}:

  - changing all the units in the application that relate to something to a different unit
    (e.g.: all the units that relate to the well height that are currently in the application
    as meters should be treated with km from now on).
  - being able to easily change the unit on some entity and have its value updated (in python)
  - getting all the created elements that have some kind of measure, such as length or depth.
  - having the info on C++ is a requisite, but the automatic conversion utilities are not, as C++
    is used for hardcore processing, this is usually done manually (as a generic way would waste
    too much processing), so, basically, the structure in C++ is important, but things related to
    the application management are not.
  - have a default way of managing those values within the application, and giving default
    implementations for it (such as Scalars, Arrays)
  - being able to define the units that can be used for some category

Usage:

    >>> from barril import units
    >>> from barril.units import scalar
    >>>
    >>> unit_manager = units.UnitDatabase()
    >>> unit_manager.AddUnitBase('length', 'meters', 'm')
    >>> unit_manager.AddUnit('length', 'milimeters', 'mm', 'x * 1000.0', 'x / 1000.0')
    >>> unit_manager.AddUnit('length', 'centimeters', 'cm', 'x * 100.0', 'x / 100.0')
    >>> unit_manager.AddCategory('well-diameter', 'length')
    >>> s = scalar.Scalar.Create('well-diameter', 10, 'm', unit_manager)
    >>> repr(s)
    "'Scalar'('length', 10, 'm')"
    >>> print s.value
    10
    >>> print s.unit
    m
    >>> s.GetCategory()
    'well-diameter'
    >>> s.GetQuantityType()
    'length'
    >>> s.unit = 'cm'
    >>> repr(s)
    "'Scalar'('length', 1000.0, 'cm')"
    >>> print s
    1000.00 centimeters
    >>> print s.GetValue(unit='mm')
    10000.0


B{Design decisions}:

    - In order to make the validation of categories, quantity types and units, the unit-manager
    must be passed around when the objects are created and a weakref is kept for future changes.

    - It is not all 'static' as it was before because this would hinder some applications, especially
    applications with multiple documents, as those applications may need multiple unit-managers
    (one for each open document).


@see: L{definitions} for the basic interfaces defined.
'''

from __future__ import absolute_import, unicode_literals

from weakref import WeakValueDictionary

import six

from ._abstractvaluewithquantity import AbstractValueWithQuantityObject
from ._array import Array
from ._fixedarray import FixedArray
from ._fraction_scalar import FractionScalar
from ._quantity import ObtainQuantity, Quantity, ReadOnlyError
from ._scalar import Scalar
from ._scalar_factory import ScalarFactory
from ._unit_constants import (
    LENGTH_QUANTITY_TYPE, UNKNOWN_QUANTITY_TYPE, UNKNOWN_UNIT, CreateUnknwonwReadOnlyQuantity)
from .unit_database import (
    InvalidOperationError, InvalidQuantityTypeError, InvalidUnitError, UnitDatabase, UnitInfo,
    UnitsError)

__all__ = [
    "Array",
    "FixedArray",
    "FractionScalar",
    "InvalidQuantityTypeError",
    "InvalidUnitError",
    "Quantity",
    "ReadOnlyError",
    "Scalar",
    "ScalarFactory",
    "UnitDatabase",
    "UnitsError",
    "AbstractValueWithQuantityObject",
]

# Unknown quantity instance
UNKNOWN_QUANTITY = ObtainQuantity(UNKNOWN_UNIT, UNKNOWN_QUANTITY_TYPE)

# Unknown quantity weak value cache
UNKNOWN_QUANTITY_WEAK_CACHE = WeakValueDictionary()


#===================================================================================================
# GetUnknownQuantity
#===================================================================================================
def GetUnknownQuantity(unknown_caption=None):
    '''
    Returns the quantity object for Unknown units.

    :rtype: Quantity
    '''
    if unknown_caption:
        return ObtainQuantity(UNKNOWN_UNIT, UNKNOWN_QUANTITY_TYPE, unknown_caption)

    return UNKNOWN_QUANTITY


#===================================================================================================
# Utilities
#===================================================================================================
def ChangeScalars(owner, **scalars):
    '''
    Change the given set of scalars for the owner

    :param owner: object
        The objectwith scalar instances to be changed.

    :param kwargs scalars:
        A dict with the scalar attribute names and the values and unit to be changed

    e.g.
        # To change value and unit
        ChangeScalars(fluid, density=(10, 'lbm/galUS'), 'concentration=(1.0, '%'))
        # To change value only
        ChangeScalars(fluid, density=(10, None))
        # To change unit only
        ChangeScalars(fluid, density=(None, 'lbm/galUS'))
    '''
    for scalar_name, (value, unit) in six.iteritems(scalars):
        new_scalar = getattr(owner, scalar_name).CreateCopy(value=value, unit=unit)
        setattr(owner, scalar_name, new_scalar)
