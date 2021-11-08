import copy
from functools import total_ordering
from typing import Any
from typing import Optional
from typing import overload
from typing import Tuple
from typing import TYPE_CHECKING
from typing import Union

from ._abstractvaluewithquantity import AbstractValueWithQuantityObject
from ._quantity import ObtainQuantity
from ._quantity import Quantity
from .unit_database import CategoryInfo
from .unit_database import UnitDatabase
from barril._util.types_ import CheckType
from barril.basic.fraction import FractionValue

if TYPE_CHECKING:
    from barril.units import IQuantity


@total_ordering
class FractionScalar(AbstractValueWithQuantityObject):
    """
    Base class for objects similar to scalars, but that represent its value as L{FractionValue}
    instance instead of a float. Useful to describe diameters for
    pipes and wells in a more natural way to the user (for instance, "5 3/4 inches").
    """

    @overload
    def __init__(self, quantity: str):
        ...

    @overload
    def __init__(self, quantity: str, value: Union[FractionValue, float], unit: str):
        ...

    @overload
    def __init__(self, quantity: "IQuantity", value: Union[FractionValue, float]):
        ...

    @overload
    def __init__(self, quantity: str, unit: str):
        ...

    @overload
    def __init__(
        self, value: Union[FractionValue, float], unit: str, category: Optional[str] = None
    ):
        ...

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def _InternalCreateWithQuantity(
        self, quantity: Quantity, value: FractionValue, unit_database: Optional[UnitDatabase] = None
    ) -> None:
        """
        For internal use only. Is used to initialize the actual quantity.

        :param quantity:
            The quantity of this scalar.

        :param value:
            The initial value
        """
        # Considering fraction values values are easily coerced from float values (though it is
        # important to note the opposite is not true) if the input value is not a fraction already
        # try to convert value to float. This also makes this subclass SetValue interface compatible
        # with superclass interface.
        try:
            if type(value) != FractionValue:
                value = FractionValue(number=float(value))
        except Exception:
            # If not a fraction and coercion to float fails, use CheckType to provide a better error
            # message.
            CheckType(value, (FractionValue, float))

        self._value = value
        self._quantity = quantity
        self._unit_database = unit_database or UnitDatabase.GetSingleton()

    def CheckValidity(self) -> None:
        """
        :raises ValueError: when current value is wrong somehow (out of limits, for example).
        """
        self._quantity.CheckValue(float(self._value))

    # Value ----------------------------------------------------------------------------------------
    def GetAbstractValue(
        self, unit: Optional[str] = None
    ) -> FractionValue:  # type:ignore[override]
        """
        :param unit:
        """
        if unit is None:
            return self._value

        return self.ConvertFractionValue(self._value, self._quantity, self.unit, unit)

    def GetValue(self, unit: Optional[str] = None) -> FractionValue:
        return self.GetAbstractValue(unit)

    value = property(GetAbstractValue)

    def _GetDefaultValue(self, category_info: CategoryInfo, unit: Optional[str] = None) -> Any:
        value = category_info.default_value
        if unit is not None:
            # needs to convert value to default unit
            value = ObtainQuantity(
                category_info.default_unit, category_info.category
            ).ConvertScalarValue(value, unit)

        return value

    def GetValueAndUnit(self) -> Tuple[FractionValue, str]:
        return self.GetValue(), self.GetUnit()

    @classmethod
    def ConvertFractionValue(
        cls,
        fraction_value: FractionValue,
        quantity: Union[str, Quantity],
        from_unit: str,
        to_unit: str,
    ) -> FractionValue:
        """
        Converts the given fraction value to the given unit.

        :param fraction_value:
            the fraction value to convert

        :param quantity:
            the IQuantity object to use in the conversion, or the quantity type itself

        :param from_unit:
            current unit of the given fraction value

        :param to_unit:
            the unit to convert the fraction value to

        :returns:
            the converted fraction value
        """
        # check if a quantity type str was passed
        if isinstance(quantity, str):
            # Note: actually ignoring the initial quantity type in this case because we
            # do the operation just using the from unit which may have any category (i.e.
            # the important thing is the quantity type, so, it can be created with the
            # default category).
            quantity = ObtainQuantity(from_unit)

        convert_to_quantity = ObtainQuantity(from_unit, quantity.GetComposingCategories())
        converted_number = convert_to_quantity.ConvertScalarValue(
            fraction_value.GetNumber(), to_unit
        )

        # convert the number
        result = FractionValue(number=converted_number)
        # convert fraction's numerator
        if fraction_value.GetFraction() is not None:
            converted_numerator = convert_to_quantity.ConvertScalarValue(
                fraction_value.GetFraction().numerator, to_unit
            )

            converted_fraction = copy.copy(fraction_value.GetFraction())
            converted_fraction.numerator = converted_numerator
            result.SetFraction(converted_fraction)
        return result

    # GetFormatted ------------------------------------------------------------------------------------
    def GetFormattedValue(
        self, unit: Optional[str] = None, value_format: Optional[str] = None
    ) -> str:
        """
        Returns the value part, that is, the number and fraction.

        :returns:
            the formatted string
        """
        return self.GetValue(unit).GetLocalizedString()

    def __str__(self) -> str:
        """
        str() operator.

        :returns:
            the string representation
        """
        return self.GetFormatted()

    def GetFormatted(self, unit: Optional[str] = None) -> str:
        """
        Returns the string representation for this FractionScalar.

        :param unit:
            If None, returns the current unit, otherwise, returns the string representation of the
            value converted to the given unit.

        :returns:
            The string representation
        """
        return self.GetFormattedValue(unit) + self.GetFormattedSuffix(unit)

    def __repr__(self) -> str:
        """
        repr() operator.

        :rtype: str
        :returns:
            the string representation
        """
        return "FractionScalar({!r}, value={!r}, unit={!r})".format(
            self._quantity.GetCategory(), self._value, self.unit
        )

    # Equality -------------------------------------------------------------------------------------
    def __eq__(self, other: Any) -> bool:
        """
        == operator.

        :param other:
            other fraction scalar

        :returns:
            if other is equal to self
        """
        return (
            type(self) == type(other)
            and self._value == other.value
            and self._quantity == other._quantity
        )

    def __lt__(self, other: Any) -> bool:
        """
        Comparison between objects.

        :param other:
            The object to be compared to

        :rtype: 1 if this object is greater than the other, -1 it is less than, 0 if they are equal.
        """
        # this is exactly the same comparison performed by the Scalar, however as they don't share
        # a base class where this method would fit, it was decided to implement it here, instead
        # of creating a base class just because of this method
        if self.quantity_type != other.quantity_type:
            msg = "can not compare scalars of different quantity types: %r != %r"
            raise TypeError(msg % self.quantity_type, other.quantity_type)

        v1 = self._value
        v2 = other.GetValue(self.unit)
        return v1 < v2

    # RegisterFractionScalarConversion -----------------------------------------
    @classmethod
    def RegisterFractionScalarConversion(cls) -> None:
        """
        Register a special unit conversion for FractionScalar.

        :param UnitDatabase db_unit:
            The unit-database instance to register the conversion into.
        """

        def ConvertFractionScalar(
            db_unit: UnitDatabase, quantity_type: str, from_unit: str, to_unit: str, value: Any
        ) -> Any:
            """
            Converts the given Fraction Scalar by applying the converts method of this class.
            """
            converted = cls.ConvertFractionValue(value, quantity_type, from_unit, to_unit)
            return FractionValue(number=float(converted))

        UnitDatabase.RegisterAdditionalConversionType(FractionValue, ConvertFractionScalar)


FractionScalar.RegisterFractionScalarConversion()
