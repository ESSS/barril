"""
This module provides the implementation of an Scalar object.
"""
from functools import total_ordering
from typing import Any
from typing import cast
from typing import Optional
from typing import overload
from typing import Tuple
from typing import Union

from oop_ext.interface import ImplementsInterface

from ._abstractvaluewithquantity import AbstractValueWithQuantityObject
from ._quantity import ObtainQuantity
from ._quantity import Quantity
from .interfaces import IQuantity
from .interfaces import IScalar
from .unit_database import CategoryInfo
from .unit_database import UnitDatabase
from barril._util.types_ import IsNumber

__all__ = ["Scalar"]


@total_ordering
@ImplementsInterface(IScalar, IQuantity)
class Scalar(AbstractValueWithQuantityObject):
    """
    This object represents a scalar (a value that has an associated quantity).

    **Scalar Creation**

    Scalars can be created by giving a value, unit or category, in some combinations.

    Assuming the default value for category "length" is 10[m], all the example below create
    equal scalars:

    .. code-block:: python

        Scalar("length")
        Scalar(10.0, "m", "length")
        Scalar(10.0, "m")
        Scalar((10.0, "m"))  # tuple of (value, unit)

    The last form is useful if you want to make a convenient interface for users of a class or method,
    accepting either a tuple or Scalar:

    .. code-block:: python

        def Compute(x, y):
            x, y = Scalar(x), Scalar(y)

    Which allows the user of the method to just pass a tuple, without having to create a Scalar explicitly:

    .. code-block:: python

        Compute(
            x=(10, "m"), y=(15, "m")
        )  # is equivalent to Compute(x=Scalar(10, 'm'), y=Scalar(15, 'm'))

    Note that the following form is invalid, because if category and value is given, unit is mandatory.

    .. code-block:: python

        Scalar("length", 1.0)

    :type _internal_unit: This is the unit in which the value has been set (but not necessarily the
    :ivar _internal_unit:
        unit which is visible to the outside world)

    .. note::
        In case you're wondering, we cannot make a Scalar with __slots__ because our callback
        system (i.e.: callback.After) won't work with it.
    """

    @overload
    def __init__(self, category: Quantity, value: Optional[float] = None) -> None:
        ...

    @overload
    def __init__(self, category: str, value: Optional[float] = None, unit: Optional[str] = None):
        ...

    @overload
    def __init__(self, value: float, unit: str, category: Optional[str] = None):
        ...

    @overload
    def __init__(self, value_and_unit: Tuple[float, str]):
        ...

    def __init__(  # type:ignore[misc]
        self, category: Any, value: Any = None, unit: Any = None
    ) -> None:
        if category.__class__ is tuple:
            # Support for creating a scalar as:
            # Scalar((10, 'm'))
            assert value is None and unit is None
            value, unit = category
            AbstractValueWithQuantityObject.__init__(self, value, unit)
        else:
            AbstractValueWithQuantityObject.__init__(
                self, category=category, value=value, unit=unit
            )

    def _InternalCreateWithQuantity(
        self,
        quantity: Quantity,
        value: Optional[float] = None,
        unit_database: Optional[UnitDatabase] = None,
    ) -> None:
        """
        For internal use only. Is used to initialize the actual quantity.

        :param quantity:
            The quantity of this scalar.

        :param value:
            The initial value.

        :param UnitDatabase unit_database:
            The unit database that should be used for this object.

        """
        if value is None:
            self._value = self._GetDefaultValue(quantity.GetCategoryInfo())
        else:
            self._value = float(value)

        self._unit_database = unit_database or UnitDatabase.GetSingleton()
        self._quantity = quantity

    # Value ----------------------------------------------------------------------------------------
    _value: float

    def GetAbstractValue(self, unit: Optional[str] = None) -> float:
        """

        :param unit:
        """
        if unit is None:
            return self._value
        else:
            return self._quantity.ConvertScalarValue(self._value, unit)

    GetValue = GetAbstractValue
    value = property(GetAbstractValue)

    def _GetDefaultValue(self, category_info: CategoryInfo, unit: Optional[str] = None) -> Any:
        """

        :param category_info:
        :param unit:
        """
        try:
            value = category_info.default_value
        except AttributeError:
            return 0.0

        if unit is not None:
            # needs to convert value to default unit
            value = ObtainQuantity(
                category_info.default_unit, category_info.category
            ).ConvertScalarValue(value, unit)

        return value

    def GetValueAndUnit(self) -> Tuple[float, str]:
        return self._value, self.GetUnit()

    def CheckValidity(self) -> None:
        """
        :raises ValueError: when current value is wrong somehow (out of limits, for example).
        """
        self._quantity.CheckValue(self._value)

    # Handling 'empty' scalar ----------------------------------------------------------------------

    @classmethod
    def CreateEmptyScalar(cls, value: float = 0.0) -> "Scalar":
        """
        Allows the creation of a scalar that does not have any associated
        category nor unit.

        :rtype: Scalar
        :returns:
            Returns an empty scalar (i.e.: without any unit) with the passed value and returns it.
        """
        quantity = Quantity.CreateEmpty()
        return cls.CreateWithQuantity(quantity, value=value)

    # Repr -----------------------------------------------------------------------------------------

    def __repr__(self) -> str:
        return "{}({}, '{}', '{}')".format(
            self.__class__.__name__, self._value, self.GetUnit(), self.GetCategory()
        )

    def __str__(self) -> str:
        """
        Should return a user-friendly representation of this object.

        :rtype: str
        :returns:
            The formatted string
        """
        return self.GetFormatted()

    # Format ---------------------------------------------------------------------------------------

    FORMATTED_VALUE_FORMAT = "%g"

    @classmethod
    def GetFormattedValueFormat(cls) -> str:
        return cls.FORMATTED_VALUE_FORMAT

    @classmethod
    def SetFormattedValueFormat(cls, value_format: str) -> None:
        """
        Sets the format for the numeric part of the scalar.
        """
        try:
            value_format % 1.11
        except TypeError as e:
            raise TypeError(
                "Incompatible format for Scalar value. Expected a format for a float value."
            ) from e
        cls.FORMATTED_VALUE_FORMAT = value_format

    def GetFormattedValue(
        self, unit: Optional[str] = None, value_format: Optional[str] = None
    ) -> str:
        """
        Returns the scalar value formated using the given format or the default format.

        The default format can be modified globally (for all Scalars) using the class method
        SetFormattedFormat.

        .. note:: The unit is NOT returned in this method.

        :param unit:
            The unit in which the value should be gotten.

        :param value_format:
            If not None (default), replaces the default value_format defined in
            Scalar.FORMATTED_VALUE_FORMAT

        :returns:
            A string with the value of this scalar formatted.
        """
        from barril.basic.format_float import FormatFloat

        if value_format is None:
            value_format = self.FORMATTED_VALUE_FORMAT
        return FormatFloat(value_format, self.GetValue(unit))

    def GetFormatted(self, unit: Optional[str] = None, value_format: Optional[str] = None) -> str:
        """
        Returns this scalar in a formatted format (i.e.: formatted value + unit).

        :param unit:
            The unit in which the value should be gotten.


        :param value_format:
            See Scalar.GetFormattedValue
        """
        return self.GetFormattedValue(unit, value_format) + self.GetFormattedSuffix(unit)

    # Compare --------------------------------------------------------------------------------------

    def __eq__(self, other: Any) -> bool:
        return (
            type(self) is type(other)
            and self._value == other.value
            and self._quantity == other._quantity
        )

    def AlmostEqual(self, other: "Scalar", precision: int) -> bool:
        return (
            type(self) is type(other)
            and round(self._value - other.value, precision) == 0
            and self._quantity == other._quantity
        )

    def __hash__(self) -> int:  # type:ignore[override]
        return hash((self._value, self._quantity))

    def __lt__(self, other: Any) -> bool:
        if self.quantity_type != other.quantity_type:
            msg = "can not compare scalars of different quantity types: %r != %r"
            raise TypeError(msg % (self.quantity_type, other.quantity_type))

        v1 = self._value
        v2 = other.GetValue(self.unit)
        return v1 < v2

    # right ----------------------------------------------------------------------------------------
    def __rtruediv__(self, other: Any) -> "Scalar":
        return self._DoOperation(other, self, "Divide", lambda a, b: a / b)

    def __rfloordiv__(self, other: Any) -> "Scalar":
        return self._DoOperation(other, self, "FloorDivide", lambda a, b: a // b)

    def __rmul__(self, other: Any) -> "Scalar":
        return self._DoOperation(other, self, "Multiply", lambda a, b: a * b)

    def __rsub__(self, other: Any) -> "Scalar":
        return self._DoOperation(other, self, "Subtract", lambda a, b: a - b)

    def __radd__(self, other: Any) -> "Scalar":
        return self._DoOperation(other, self, "Sum", lambda a, b: a + b)

    # basic ----------------------------------------------------------------------------------------
    def __truediv__(self, other: Any) -> "Scalar":
        return self._DoOperation(self, other, "Divide", lambda a, b: a / b)

    def __floordiv__(self, other: Any) -> "Scalar":
        return self._DoOperation(self, other, "FloorDivide", lambda a, b: a // b)

    def __mul__(self, other: Any) -> "Scalar":
        return self._DoOperation(self, other, "Multiply", lambda a, b: a * b)

    def __sub__(self, other: Any) -> "Scalar":
        return self._DoOperation(self, other, "Subtract", lambda a, b: a - b)

    def __add__(self, other: Any) -> "Scalar":
        return self._DoOperation(self, other, "Sum", lambda a, b: a + b)

    def __pow__(self, exponent: int) -> "Scalar":
        result = self
        for _ in range(exponent - 1):
            result = result * self
        return result

    def _DoOperation(self, p1: Any, p2: Any, operation: Any, callback_operation: Any) -> Any:
        p1_is_number = IsNumber(p1)
        if p1_is_number and operation not in ["Divide", "FloorDivide"]:
            return self.__class__.CreateWithQuantity(
                self._quantity, callback_operation(p1, self._value)
            )

        if IsNumber(p2):
            return self.__class__.CreateWithQuantity(
                self._quantity, callback_operation(self._value, p2)
            )

        unit_database = self._unit_database
        operation_func = getattr(unit_database, operation)
        if p1_is_number:
            assert operation in [
                "Divide",
                "FloorDivide",
            ], "Only operation Divide and FloorDivide allowed here!"
            q, v = operation_func(Quantity.CreateEmpty(), p2.GetQuantity(), p1, p2.value)
        else:
            q, v = operation_func(p1.GetQuantity(), p2.GetQuantity(), self._value, p2.value)
        return self.__class__.CreateWithQuantity(q, v)

    def __reduce__(self) -> Any:
        """
        Defining reduce so that we can pickle scalars.
        """
        return Scalar, (self._quantity, self.value, None)  # Unit defined in quantity
