"""
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
    >>> from barril.units import Scalar
    >>> s = Scalar(10, 'm')
    >>> repr(s)
    "Scalar(10.0, 'm', 'length')"
    >>> s.value, s.unit
    (10.0, 'm')
    >>> s.GetCategory()
    'length'
    >>> s.GetQuantityType()
    'length'
    >>> s.CreateCopy(unit="cm")
    Scalar(1000.0, 'cm', 'length')

B{Design decisions}:

    - In order to make the validation of categories, quantity types and units, the unit-manager
    must be passed around when the objects are created and a weakref is kept for future changes.

    - It is not all 'static' as it was before because this would hinder some applications, especially
    applications with multiple documents, as those applications may need multiple unit-managers
    (one for each open document).


@see: L{definitions} for the basic interfaces defined.
"""
from typing import Any
from typing import Optional
from typing import Tuple
from typing import TYPE_CHECKING
from weakref import WeakValueDictionary

from ._abstractvaluewithquantity import AbstractValueWithQuantityObject  # noqa
from ._array import Array
from ._array import ValuesType
from ._fixedarray import FixedArray  # noqa
from ._fraction_scalar import FractionScalar  # noqa
from ._quantity import ObtainQuantity
from ._quantity import Quantity
from ._quantity import ReadOnlyError
from ._scalar import Scalar  # noqa
from ._unit_constants import CreateUnknwonwReadOnlyQuantity
from ._unit_constants import LENGTH_QUANTITY_TYPE
from ._unit_constants import UNKNOWN_QUANTITY_TYPE
from ._unit_constants import UNKNOWN_UNIT
from .interfaces import IArray
from .interfaces import IObjectWithQuantity
from .interfaces import IQuantity
from .interfaces import IQuantity2
from .interfaces import IQuantity3
from .interfaces import IQuantity6
from .interfaces import IScalar
from .unit_database import InvalidOperationError
from .unit_database import InvalidQuantityTypeError
from .unit_database import InvalidUnitError
from .unit_database import UnitDatabase
from .unit_database import UnitInfo
from .unit_database import UnitsError

# Needed for Python<3.9: WeakValueDictionary doesn't support
# the subscription operator.
if TYPE_CHECKING:
    QuantityWeakDictionary = WeakValueDictionary[str, Quantity]
else:
    QuantityWeakDictionary = WeakValueDictionary

__all__ = [
    "AbstractValueWithQuantityObject",
    "Array",
    "ChangeScalars",
    "FixedArray",
    "FractionScalar",
    "GetUnknownQuantity",
    "IArray",
    "IObjectWithQuantity",
    "IQuantity",
    "IScalar",
    "InvalidQuantityTypeError",
    "InvalidUnitError",
    "ObtainQuantity",
    "Quantity",
    "ReadOnlyError",
    "Scalar",
    "UnitDatabase",
    "UnitsError",
    "ValuesType",
]

# Unknown quantity instance
UNKNOWN_QUANTITY = ObtainQuantity(UNKNOWN_UNIT, UNKNOWN_QUANTITY_TYPE)

# Unknown quantity weak value cache
UNKNOWN_QUANTITY_WEAK_CACHE: QuantityWeakDictionary = QuantityWeakDictionary()


def GetUnknownQuantity(unknown_caption: Optional[str] = None) -> Quantity:
    """
    Returns the quantity object for Unknown units.

    :rtype: Quantity
    """
    if unknown_caption:
        return ObtainQuantity(UNKNOWN_UNIT, UNKNOWN_QUANTITY_TYPE, unknown_caption)

    return UNKNOWN_QUANTITY


def ChangeScalars(owner: object, **scalars: Tuple[Any, Any]) -> None:
    """
    Change the given set of scalars for the owner

    :param owner:
        The object with scalar instances to be changed.

    :param kwargs scalars:
        A dict with the scalar attribute names and the values and unit to be changed

    e.g.
        # To change value and unit
        ChangeScalars(fluid, density=(10, 'lbm/galUS'), 'concentration=(1.0, '%'))
        # To change value only
        ChangeScalars(fluid, density=(10, None))
        # To change unit only
        ChangeScalars(fluid, density=(None, 'lbm/galUS'))
    """
    for scalar_name, (value, unit) in scalars.items():
        new_scalar = getattr(owner, scalar_name).CreateCopy(value=value, unit=unit)
        setattr(owner, scalar_name, new_scalar)
