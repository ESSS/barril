from typing import Any
from typing import cast
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import overload
from typing import Sequence
from typing import TypeVar
from typing import Union

from oop_ext.interface import ImplementsInterface

from ._abstractvaluewithquantity import AbstractValueWithQuantityObject
from ._abstractvaluewithquantity import T
from ._quantity import Quantity
from ._scalar import Scalar
from .interfaces import IArray
from .interfaces import ValuesType
from barril._util.types_ import IsNumber
from barril.basic.format_float import FormatFloat
from barril.units.unit_database import CategoryInfo
from barril.units.unit_database import UnitDatabase


__all__ = ["Array"]


SelfT = TypeVar("SelfT", bound="Array")


@ImplementsInterface(IArray)
class Array(AbstractValueWithQuantityObject, Generic[ValuesType]):
    """
    Array represents a sequence of values that also have an unit associated.

    Some ways to construct it (note that usually numpy arrays should be used).

    .. code-block:: python

        Array(numpy.array([0, 1, 2, 3, 4], numpy.float64), "m")

        Array([0, 1, 2, 3, 4], "m")

        Array("length", [0, 1, 2, 3, 4], "m")

        Array(ObtainQuantity("m", "length"), [0, 1, 2, 3, 4])


    Arrays are a ``Generic`` subclass, parametrized by their container type:

    .. code-block:: python

        a = Array([1, 2, 3], "m")
        reveal_type(a)

    .. code-block::

        note: Revealed type is "barril.units._array.Array[builtins.list*[builtins.int*]]"

    Functions/methods which receive arrays can be declared with more specific types:

    .. code-block:: python

        def compute(inputs: Array[np.ndarray]) -> Array[np.ndarray]:
            ...


        def compute(inputs: Array[np.ndarray[np.float64]]) -> Array[np.ndarray[np.float64]]:
            ...

    """

    @overload
    def __init__(self, category: Union[str, Quantity]):
        ...

    @overload
    def __init__(self, values: ValuesType, unit: str, category: Optional[str] = None):
        ...

    @overload
    def __init__(self, category: str, values: ValuesType, unit: str):
        ...

    @overload
    def __init__(self, category: Quantity, values: ValuesType):
        ...

    def __init__(  # type:ignore[misc]
        self, category: str, values: Any = None, unit: Any = None
    ) -> None:
        super().__init__(category, value=values, unit=unit)

    def _InternalCreateWithQuantity(  # type:ignore[override]
        self,
        quantity: Quantity,
        values: Optional[ValuesType] = None,
        unit_database: Optional[UnitDatabase] = None,
        value: Optional[ValuesType] = None,
    ) -> None:
        if value is not None:
            if values is not None:
                raise ValueError("Duplicated values parameter given")
            values = value

        assert values is not None
        self._value = values
        self._unit_database = unit_database or UnitDatabase.GetSingleton()
        self._quantity = quantity
        self._is_valid: Optional[bool] = None
        self._validity_exception: Optional[Exception] = None

    def CheckValidity(self) -> None:
        """
        :raises ValueError: when current value is wrong somehow (out of limits, for example).
        """
        self.ValidateValues(self._value, self._quantity)

    def CreateCopy(  # type:ignore[override]
        self: SelfT,
        values: Optional[ValuesType] = None,
        unit: Optional[str] = None,
        category: Optional[str] = None,
        **kwargs: object
    ) -> SelfT:
        return AbstractValueWithQuantityObject.CreateCopy(
            self, value=values, unit=unit, category=category, **kwargs
        )

    # Values ---------------------------------------------------------------------------------------
    def GetAbstractValue(self, unit: Optional[str] = None) -> ValuesType:
        """
        :param unit: this is the unit in which we want the values
        :returns:
            the values stored. May be an a list of int, float, etc.
        """
        values = self._value
        if unit is None or unit == self._quantity.unit:
            return values

        def IsListOfTuples(v: Any) -> bool:
            try:
                return len(v) > 0 and isinstance(v[0], tuple)
            except TypeError:
                return False  # numpy raises a TypeError if it's a 0D array, so ignores it

        if IsListOfTuples(values):
            result = []
            Convert = self._quantity.Convert
            for elem in values:
                result.append(tuple(Convert(v, unit) for v in elem))
            return type(values)(result)  # type:ignore[call-arg, arg-type]

        else:
            return self._quantity.Convert(values, unit)

    GetValues = GetAbstractValue
    values = property(GetAbstractValue)

    def _GetDefaultValue(
        self, category_info: CategoryInfo, unit: Optional[str] = None
    ) -> ValuesType:
        return cast(ValuesType, [])

    def ValidateValues(self, values: ValuesType, quantity: Quantity) -> None:
        """Set the value to store in this values_quantity. May be an int,
        float, numarray, list of floats, etc.

        :param values:
            The values to be set.

        :param quantity:
            The quantity of the values being passed (note that GetUnit will still return the previous
            unit set -- this unit is only to indicate the internal value).
        """
        if self._is_valid is True:
            return

        if self._validity_exception is not None:
            raise self._validity_exception

        try:
            self._DoValidateValues(values, quantity)
        except Exception as e:
            self._validity_exception = e
            self._is_valid = False
            raise
        else:
            self._is_valid = True

    def _DoValidateValues(self, values: ValuesType, quantity: Quantity) -> None:
        """
        .. seealso:: :meth:`.ValidateValues`
        """
        is_derived = quantity.IsDerived()
        if not is_derived:
            # only check min, max if we have only 1 category (otherwise, we won't have a valid assumption
            # about the actual values)
            category_info = quantity.GetCategoryInfo()

            if category_info.min_value is not None or category_info.max_value is not None:
                # verify if values are in the given limits (if needed)
                CheckValue = quantity.CheckValue
                if len(values) > 0:
                    if isinstance(values[0], tuple):
                        for value in values:
                            if isinstance(value, tuple):
                                for v in value:
                                    CheckValue(v)
                    else:
                        import numpy

                        isnam = numpy.isnan

                        # Search for the first non-NaN value to initialize MIN/MAX.
                        is_numpy = isinstance(values, numpy.ndarray)

                        iterator: Iterator[Any] = iter(values)

                        for value in iterator:
                            if isnam(value):
                                continue

                            # Iterate until we get a non-nan number
                            min_value = max_value = value

                            # Keep on the iteration now that we can already make the check.
                            for value in iterator:
                                if isnam(value):
                                    # NaNs would fail the min_value validation below.
                                    continue

                                if value < min_value:
                                    min_value = value

                                elif value > max_value:
                                    max_value = value

                            if is_numpy:
                                min_value = float(min_value)
                                max_value = float(max_value)

                            CheckValue(min_value)
                            CheckValue(max_value)

                            # Break the outer 'for' used just to get the min/max
                            break

    @classmethod
    def FromScalars(
        cls,
        scalars: Iterable[Scalar],
        *,
        unit: Optional[str] = None,
        category: Optional[str] = None
    ) -> "Array":
        """
        Create an Array from a sequence of Scalars.

        When not defined, the unit and category assumed will be from the first Scalar on the sequence.

        :param values:
            A sequence of Scalars. When the values parameter is an empty sequence and
            the unit is not provided an Array with an empty quantity will be returned.

        :param unit:
            A string representing the unit, if not defined
            the unit from the first Scalar on the sequence will be used.

        :param category:
            A string representing the category, if not defined
            the category from the first Scalar on the sequence will be used.
        """
        scalars = iter(scalars)
        try:
            first_scalar = next(scalars)
        except StopIteration:
            if unit is None and category is None:
                return cls.CreateEmptyArray()
            elif category is None:
                category = UnitDatabase.GetSingleton().GetDefaultCategory(unit)
                return cls(values=[], unit=unit, category=category)  # type:ignore[arg-type]
            else:
                assert unit is None
                return cls(  # type:ignore[call-overload]
                    values=[], unit=unit, category=category
                )  # This actually will raise an exception

        unit = unit or first_scalar.unit
        category = category or first_scalar.category
        values = [first_scalar.GetValue(unit)] + [scalar.GetValue(unit) for scalar in scalars]
        return cls(values=values, unit=unit, category=category)

    @classmethod
    def CreateEmptyArray(cls, values: Optional[Sequence[float]] = None) -> "Array":
        """
        Allows the creation of a array that does not have any associated
        category nor unit.

        :rtype: Array
        """
        if values is None:
            values = []

        quantity = Quantity.CreateEmpty()
        return cls.CreateWithQuantity(quantity, values=values)

    # Equality -------------------------------------------------------------------------------------
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Array):
            return False

        return (
            tuple(self.values) == tuple(other.values)
            and self._quantity == other._quantity
            and self.unit == other.unit
        )

    def __repr__(self) -> str:
        values_str = "[%s]" % ", ".join(str(v) for v in self.values)
        return "{}({}, {}, {})".format(
            self.__class__.__name__, self.GetQuantityType(), values_str, self.GetUnit()
        )

    def __str__(self) -> str:
        """
        Should return a user-friendly representation of this object.

        :rtype: str
        :returns:
            The formatted string
        """
        if len(self.values) > 0 and isinstance(self.values[0], tuple):
            values_str = " ".join(str(v) for v in self.values)
        else:
            values_str = " ".join((FormatFloat("%g", v)) for v in self.values)

        return values_str + self.GetFormattedSuffix()

    # Basic operators ------------------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self.values)

    @overload
    def __getitem__(self, index: int) -> Any:
        ...

    @overload
    def __getitem__(self, index: slice) -> ValuesType:
        ...

    def __getitem__(self, index: Any) -> Any:
        return self.values[index]

    def __iter__(self) -> Iterator[Any]:
        return iter(self.values)

    def __truediv__(self: SelfT, other: Any) -> SelfT:
        return self._DoOperation(self, other, "Divide")

    def __floordiv__(self: SelfT, other: Any) -> SelfT:
        return self._DoOperation(self, other, "FloorDivide")

    def __mul__(self: SelfT, other: Any) -> SelfT:
        return self._DoOperation(self, other, "Multiply")

    def __add__(self: SelfT, other: Any) -> SelfT:
        return self._DoOperation(self, other, "Sum")

    def __sub__(self: SelfT, other: Any) -> SelfT:
        return self._DoOperation(self, other, "Subtract")

    # Right-Basic operators ------------------------------------------------------------------------
    def __rtruediv__(self: SelfT, other: Any) -> SelfT:
        return self._DoOperation(other, self, "Divide")

    def __rfloordiv__(self: SelfT, other: Any) -> SelfT:
        return self._DoOperation(other, self, "FloorDivide")

    def __rdiv__(self: SelfT, other: Any) -> SelfT:
        return self._DoOperation(other, self, "Divide")

    def __rmul__(self: SelfT, other: Any) -> SelfT:
        return self._DoOperation(other, self, "Multiply")

    def __radd__(self: SelfT, other: Any) -> SelfT:
        return self._DoOperation(other, self, "Sum")

    def __rsub__(self: SelfT, other: Any) -> SelfT:
        return self._DoOperation(other, self, "Subtract")

    def _DoOperation(self, p1: SelfT, p2: SelfT, operation: str) -> SelfT:
        """
        Actually go on and do an operation considering the data we have to transform considering
        any combination of: number, list and numpy
        """
        from ._value_generator import _ValueGenerator
        import numpy

        # get the quantities and setup the value generator properly
        if IsNumber(p1) or isinstance(p1, numpy.ndarray):
            values_iteration = _ValueGenerator(p1, p2.values)
            q2 = p2.GetQuantity()
            q1 = Quantity.CreateEmpty()

        elif IsNumber(p2) or isinstance(p2, numpy.ndarray):
            values_iteration = _ValueGenerator(p1.values, p2)
            q1 = p1.GetQuantity()
            q2 = Quantity.CreateEmpty()

        else:
            values_iteration = _ValueGenerator(p1.values, p2.values)
            q1 = p1.GetQuantity()
            q2 = p2.GetQuantity()

        unit_database = self.GetUnitDatabase()
        operation_func = getattr(unit_database, operation)

        # if handling numpy, just call it all at once!
        if values_iteration.IsNumpy():
            v0, v1 = next(iter(values_iteration))
            q, v = operation_func(q1, q2, v0, v1)
            return self.__class__.CreateWithQuantity(q, v)  # type:ignore[return-value]
        else:
            # not numpy: create a new structure to hold the values
            result = []
            for v0, v1 in values_iteration:
                q, v = operation_func(q1, q2, v0, v1)
                result.append(v)

            if values_iteration.IsTuple():
                result = tuple(result)  # type:ignore[assignment]
            return self.__class__.CreateWithQuantity(q, result)  # type:ignore[return-value]
