from typing import Any
from typing import cast
from typing import Generic
from typing import Optional
from typing import overload
from typing import Tuple
from typing import TYPE_CHECKING
from typing import Union

from ._array import Array
from ._array import ValuesType
from barril.units.unit_database import CategoryInfo
from barril.units.unit_database import UnitDatabase

if TYPE_CHECKING:
    from ._quantity import Quantity
    from barril.units import Scalar

__all__ = ["FixedArray"]


class FixedArray(Array, Generic[ValuesType]):
    """
    Represents an Array with fixed number of elements.


    Like ``Array``, ``FixedArray`` is a ``Generic`` subclass, parametrized by their container type:

    .. code-block:: python

        a = FixedArray(3, [1, 2, 3], "m")
        reveal_type(a)

    .. code-block::

        note: Revealed type is "barril.units._fixedarray.FixedArray[builtins.list*[builtins.int*]]"
    """

    _dimension: Any = None

    @overload
    def __init__(self, dimension: int, category: Union[str, "Quantity"]):
        ...

    @overload
    def __init__(self, dimension: int, values: ValuesType, unit: str):
        ...

    @overload
    def __init__(self, dimension: int, category: str, values: ValuesType, unit: str):
        ...

    @overload
    def __init__(self, dimension: int, category: str, unit: str):
        ...

    @overload
    def __init__(self, dimension: int, category: "Quantity", values: ValuesType):
        ...

    def __init__(  # type:ignore[misc]
        self, dimension: int, category: str, values: Any = None, unit: Any = None
    ) -> None:
        """
        :param int dimension:
            The dimension for this array.

        :type category: string or IQuantity
        :param category:
            The category for the unit point or the IQuantity for this object
            (in this case, the unit will be ignored (if it is passed)).

        :type values: sequence or numpy array
        :param values:
            A sequence with its initial values.

        :param str unit:
            Unit (not used if a quantity is passed).
        """
        if dimension < 2:
            raise ValueError("Dimension MUST be 2 or more")
        self._dimension = dimension

        Array.__init__(self, category, values, unit)

    def _InternalCreateWithQuantity(  # type:ignore[override]
        self,
        quantity: "Quantity",
        values: Optional[ValuesType] = None,
        unit_database: Optional[UnitDatabase] = None,
        dimension: Optional[int] = None,
        value: Optional[ValuesType] = None,
    ) -> None:
        if value is not None:
            if values is not None:
                raise ValueError("Duplicated values parameter given")

            values = value

        assert values is not None
        if dimension is None:
            try:
                if self._dimension is None:
                    self._dimension = len(values)
            except AttributeError:
                pass

            dimension = self._dimension

        elif hasattr(self, "_dimension"):
            if self._dimension is not None and dimension != self._dimension:
                raise ValueError(
                    "Dimension re-definition mismatch: %s != %s" % (self._dimension, dimension)
                )

        if dimension < 2:
            raise ValueError("Dimension MUST be 2 or more")
        self._dimension = dimension

        if values is None:
            values = [0.0] * dimension
        self.CheckValues(values, dimension)

        Array._InternalCreateWithQuantity(self, quantity, values)

    def CreateCopy(  # type:ignore[override]
        self,
        values: Optional[ValuesType] = None,
        unit: Optional[str] = None,
        category: Optional[str] = None,
        **kwargs: object
    ) -> "FixedArray":
        return Array.CreateCopy(
            self, values=values, unit=unit, category=category, dimension=self._dimension, **kwargs
        )

    # Values ---------------------------------------------------------------------------------------
    def _GetDefaultValue(
        self, category_info: CategoryInfo, unit: Optional[str] = None
    ) -> ValuesType:
        return cast(ValuesType, [0.0] * self._dimension)

    def CheckValues(self, values: ValuesType, dimension: Optional[int] = None) -> None:
        """Checks whether the dimensions consistent with the dimensions in this unit point"""
        if dimension is None:
            dimension = self.dimension

        if len(values) != dimension:
            msg = "Values must have %d elements, but has %d"
            raise ValueError(msg % (dimension, len(values)))

    @classmethod
    def CreateEmptyArray(  # type:ignore[override]
        cls, dimension: int, values: Optional[ValuesType] = None
    ) -> "FixedArray":
        """
        Allows the creation of a array that does not have any associated category nor unit.

        :returns:
            Returns an empty array.
        """
        from ._quantity import Quantity

        if values is None:
            values = cast(ValuesType, [0.0] * dimension)

        quantity = Quantity.CreateEmpty()
        return cls.CreateWithQuantity(quantity, dimension=dimension, values=values)

    # Dimension ------------------------------------------------------------------------------------
    def GetDimension(self) -> int:
        return self._dimension

    dimension = property(GetDimension)

    # Equality -------------------------------------------------------------------------------------
    def __eq__(self, other: Any) -> bool:
        return Array.__eq__(self, other) and self.dimension == other.dimension

    def __reduce__(self) -> Any:
        """
        Defining reduce so that we can pickle fixed arrays.
        """
        return (
            FixedArray,
            (self._dimension, self._quantity, self.values, None),  # Unit defined in quantity
        )

    def ChangingIndex(
        self, index: int, value: Union[float, "Scalar", Tuple], use_value_unit: bool = True
    ) -> "FixedArray":
        """
        Creates a FixedArray from based on this FixedArray changing a single value based on the
        passed index.

        i.e.: array.ChangingIndex(0, Scalar(1.0, 'm'))
              will create a new FixedArray where the index == 0 is changed to the passed value.

        :param value:
            The value to be used to set at the given index.

        :param index:
            The index which should be changed.

        :param use_value_unit:
            If True and a Scalar is passed, the newly created array will have the unit of the
            scalar, not of the original array, otherwise (if False) the FixedArray unit will be
            kept.

        :return:
            The created FixedArray.
        """
        from barril.units import Scalar

        if isinstance(value, tuple):
            scalar = Scalar(self.GetValues()[index], self.GetUnit()).CreateCopy(*value)

        elif not isinstance(value, Scalar):
            scalar = Scalar(value, self.GetUnit())

        else:
            scalar = value

        if use_value_unit:
            quantity = scalar.GetQuantity()
        else:
            quantity = self.GetQuantity()

        values = list(self.GetValues(quantity.GetUnit()))
        values[index] = scalar.GetValue(quantity.GetUnit())
        return FixedArray(self.dimension, quantity, tuple(values))

    def IndexAsScalar(self, index: int, quantity: Optional["Quantity"] = None) -> "Scalar":
        """
        :param index:
            The index which should be gotten as a Scalar.

        :param quantity:
            The quantity in which we want the Scalar (uses the FixedArray quantity
            if not passed).

        :return Scalar:
            A Scalar representation of the given index.
        """
        from barril.units import Scalar

        if quantity is None:
            quantity = self.GetQuantity()
        return Scalar(  # type:ignore[call-overload]
            quantity, self.GetValues(unit=quantity.GetUnit())[index]
        )
