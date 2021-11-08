"""
This module provides the implementation of an Quantity object.
"""
from collections import OrderedDict
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import NoReturn
from typing import Optional
from typing import overload
from typing import Sequence
from typing import Tuple
from typing import TypeVar
from typing import Union

from oop_ext.interface import ImplementsInterface

from ._unit_constants import UNKNOWN_UNIT
from .interfaces import IQuantity
from .interfaces import IQuantity2
from .interfaces import IQuantity3
from .interfaces import IQuantity6
from .interfaces import UnitExponentTuple
from barril.units.exceptions import QuantityValidationError
from barril.units.unit_database import CategoryInfo
from barril.units.unit_database import FixUnitIfIsLegacy
from barril.units.unit_database import InvalidUnitError
from barril.units.unit_database import UnitDatabase
from barril.units.unit_database import UnitsError

__all__ = ["Quantity", "ObtainQuantity"]


@overload
def ObtainQuantity(
    unit: str,
    category: Optional[str] = None,
    unknown_unit_caption: Optional[str] = None,
) -> "Quantity":
    ...


@overload
def ObtainQuantity(
    unit: str,
    category: Union[Tuple[str, ...], str],
) -> "Quantity":
    ...


@overload
def ObtainQuantity(
    unit: Union[None, List[UnitExponentTuple], Dict[str, Sequence[Union[str, int]]]],
    category: Optional[str] = None,
    unknown_unit_caption: Optional[str] = None,
) -> "Quantity":
    ...


def ObtainQuantity(
    unit: Union[str, None, List[UnitExponentTuple], Dict[str, Sequence[Union[str, int]]]],
    category: Optional[Union[Tuple[str, ...], str]] = None,
    unknown_unit_caption: Optional[str] = None,
) -> "Quantity":
    """
    :type unit: str or OrderedDict(str -> list(str, int))
    :param unit:
        Either the string representing the unit or an ordered dict with the composing unit
        information (if composing all the info, including the category will be received in this
        parameter).

    :param str category:
        The category for the quantity. If not given it's gotten based on the unit passed.

    :param str unknown_unit_caption:
        The caption for the unit (used if unknown).

    :rtype Quantity:
    """
    unit_database = UnitDatabase.GetSingleton()
    quantities_cache = unit_database.quantities_cache

    if isinstance(unit, (list, tuple)):
        # It may be a derived unit with list(tuple(str, int)) -- in which case the category
        # must also be a list (of the same size)
        if len(unit) == 1 and unit[0][1] == 1:
            # Although passed as composing, it's a simple case
            unit = unit[0][0]
            if isinstance(category, (list, tuple)):
                category = category[0]
        else:
            assert isinstance(category, (list, tuple))
            unit = OrderedDict((cat, unit_and_exp) for (cat, unit_and_exp) in zip(category, unit))
            category = None

    if isinstance(unit, dict):
        assert category is None
        if len(unit) == 1 and next(iter(unit.values()))[1] == 1:  # type:ignore[comparison-overlap]
            # Although passed as composing, it's a simple case
            category, (unit, _exp) = next(iter(unit.items()))  # type:ignore[assignment]
        else:
            key = tuple(
                (category, tuple(unit_and_exp)) for (category, unit_and_exp) in unit.items()
            )
            if unknown_unit_caption:
                key += (unknown_unit_caption,)
            try:
                return quantities_cache[key]
            except KeyError:
                quantity = quantities_cache[key] = Quantity(unit, None, unknown_unit_caption)
                return quantity

    key = (category, unit, unknown_unit_caption)  # type:ignore[assignment]
    try:
        return quantities_cache[key]
    except KeyError:
        pass  # Just go on with the regular flow.

    if not isinstance(unit, str):
        if category is None:
            raise AssertionError("Currently only supporting unit as a string.")
        else:
            # Unit is given by the category
            unit = unit_database.GetDefaultUnit(category)
        quantity = quantities_cache[key] = Quantity(category, unit, unknown_unit_caption)
        return quantity

    elif category is None:
        category = unit_database.GetDefaultCategory(unit)
        if not category:
            is_legacy, unit = FixUnitIfIsLegacy(unit)
            if is_legacy:
                category = unit_database.GetDefaultCategory(unit)
            else:
                raise UnitsError(f"Unable to get default category for: {unit}")

        key_with_resolved_category = (category, unit, unknown_unit_caption)
        try:
            return quantities_cache[key_with_resolved_category]
        except KeyError:
            quantity = quantities_cache[key_with_resolved_category] = Quantity(
                category, unit, unknown_unit_caption
            )
            # Cache it with None category too.
            quantities_cache[key] = quantity
            return quantity

    else:
        quantities_cache[key] = quantity = Quantity(category, unit, unknown_unit_caption)
        return quantity


class ReadOnlyError(NotImplementedError):
    """
    Error thrown if some change is attempted in the quantity (as it's now read-only).
    """


T = TypeVar("T")


@ImplementsInterface(IQuantity, IQuantity2, IQuantity3, IQuantity6, no_check=True)
class Quantity:
    """
    The quantity is an object that has its associated category, quantity type and unit.

    Internally we represent the information as a dict with the information needed for derived
    units in the following way:

    .. note:: The preferred way to get a Quantity is through ObtainQuantity, although
    Quantity(category, unit) was maintained for backward-compatibility.
    """

    _EMPTY_QUANTITY: ClassVar[Optional["Quantity"]] = None

    @classmethod
    def CreateEmpty(cls) -> "Quantity":
        """
        Create a quantity without any internal unit.

        :rtype: Quantity
        :returns:
            Returns an empty quantity.
        """
        empty = cls._EMPTY_QUANTITY
        if empty is None:
            empty = cls._EMPTY_QUANTITY = ObtainQuantity(OrderedDict())
        return empty

    @classmethod
    def CreateDerived(
        cls,
        category_to_unit_and_exps: Dict[str, Sequence[Union[str, int]]],
        unknown_unit_caption: Optional[str] = None,
    ) -> "Quantity":
        """
        Same as _CreateDerived, but always validating the category and units.

        .. see:: _CreateDerived for parameters.
        """
        return cls._CreateDerived(
            category_to_unit_and_exps, unknown_unit_caption=unknown_unit_caption
        )

    @classmethod
    def _CreateDerived(
        cls,
        category_to_unit_and_exps: Dict[str, Sequence[Union[str, int]]],
        validate_category_and_units: bool = True,
        unknown_unit_caption: Optional[str] = None,
    ) -> "Quantity":
        """
        Create a category that represents a derived quantity (usually resulting from operations
        among quantities).

        :type category_to_unit_and_exps: OrderedDict(str->(list(str, int)))
        :param category_to_unit_and_exps:
            This odict defines the category as well as the unit in a way that we can specify exponents.

        :param bool validate_category_and_units:
            If True, the category and units will be validated (otherwise, it'll just create it
            without trying to validate any value (note that it's meant to be used internally
            to make creating the quantity faster without having to actually validate it)

        :rtype: cls
        :returns:
            An instance that represents a quantity with the given categories, units and exponents.
        """
        unit_database = UnitDatabase.GetSingleton()

        if validate_category_and_units:
            assert hasattr(
                category_to_unit_and_exps, "items"
            ), "validate_category_and_units needs to be a dict"
            for category, (unit, _exp) in category_to_unit_and_exps.items():
                # will do the checkings needed for validation (category/unit)
                # so that we can later just store the internal information without
                # any other check.

                # changes to accomodate making operations with derived units (internally the
                # information must be a dict)
                if category.__class__ != str:
                    raise TypeError("Only str is accepted. %s is not." % category.__class__)

                # Getting the category should be enough to know that it's valid.
                category_info = unit_database.GetCategoryInfo(category)

                # if no unit was given, assume base unit for this quantity_type
                if unit is None:
                    unit = category_info.default_unit
                else:
                    if not isinstance(unit, str):
                        raise TypeError("Only str is accepted. %s is not." % unit.__class__)
                    unit_database.CheckQuantityTypeUnit(category_info.quantity_type, unit)

        return ObtainQuantity(
            OrderedDict(
                (category, unit_and_exp[:])
                for (category, unit_and_exp) in category_to_unit_and_exps.items()
            ),
            unknown_unit_caption=unknown_unit_caption,
        )

    __slots__ = [
        "__weakref__",
        "_category",
        "_category_info",
        "_category_to_unit_and_exps",
        "_composing_categories",
        "_composing_units",
        "_composing_units_joining_exponents",
        "_hash",
        "_is_derived",
        "_quantity_type",
        "_tobase",
        "_unit",
        "_unit_database",
        "_unknown_unit_caption",
        "_category_info",
        "_configured",
    ]

    _category_to_unit_and_exps: Dict[str, Sequence[Union[str, int]]]
    _unknown_unit_caption: Optional[str]
    _category_info: CategoryInfo

    def __new__(
        cls, category: str, unit: str, unknown_unit_caption: Optional[str] = None
    ) -> "Quantity":
        """
        Overridden because we don't want to call the Quantity.__new__ (which would result
        in a StackOverflowError).
        """
        return object.__new__(cls)

    def __copy__(self) -> "Quantity":
        """
        As we're now immutable, always return itself.
        """
        return self

    def __deepcopy__(self, *args: object, **kwargs: object) -> "Quantity":
        """
        As we're now immutable, always return itself.
        """
        return self

    def __reduce__(self) -> Union[str, Tuple[Any, ...]]:
        """
        Used in pickle protocol

        :rtype: tuple(callable, args)
        :returns:
            Used during the pickle so that we can restore it as the same instance it was before
            (i.e.: don't create a new instance).
        """
        lst: List[Any] = list(
            (category, unit_and_exp)
            for (category, unit_and_exp) in self._category_to_unit_and_exps.items()
        )
        if self._unknown_unit_caption:
            lst.append(self._unknown_unit_caption)
        else:
            lst.append(None)
        return _ObtainReduced, (lst,)

    def __init__(
        self, category: Any, unit: Any, unknown_unit_caption: Optional[str] = None
    ) -> None:
        """
        :param category:
            The category to which the new quantity should be bound or an odict with information on
            the derived category/unit (in which case the unit parameter is ignored).

        :param str unit:
            The unit which the new quantity should have.
        """
        try:
            # Bail out if unit is already configured: this may happen when the Quantity constructor
            # is called directly: if Quantity() is called, the protocol will call __new__ and even
            # if a configured instance is returned, it'll call __init__ again, so, this is a check
            # for this situation so that we return if the quantity is already configured.
            self._unknown_unit_caption
            return
        except AttributeError:
            pass

        # Keep self._unit_database for faster access.
        unit_database = self._unit_database = UnitDatabase.GetSingleton()

        if unknown_unit_caption is not None:
            assert (
                unknown_unit_caption.__class__ == str
            ), "Unit caption must be a string. Note: the unit database and unit system parameters were removed."
            self._unknown_unit_caption = unknown_unit_caption
        else:
            self._unknown_unit_caption = ""

        if category.__class__ is OrderedDict:
            assert unit is None
            self._category_to_unit_and_exps = category
            self._is_derived = True

            rep_and_exp: OrderedDict[Any, Any] = OrderedDict()
            for category, (_unit, exp) in self._category_to_unit_and_exps.items():
                quantity_type = unit_database.GetCategoryQuantityType(category)
                existing = rep_and_exp.get(quantity_type, 0)
                rep_and_exp[quantity_type] = existing + exp

            self._category = self._MakeStr(
                [
                    (category, exp)
                    for category, (_unit, exp) in self._category_to_unit_and_exps.items()
                ]
            )
            self._quantity_type = self._MakeStr(list(rep_and_exp.items()))
            self._unit = self._CreateUnitsWithJoinedExponentsString()
            self._composing_units = tuple(
                (unit, exp) for _category, (unit, exp) in self._category_to_unit_and_exps.items()
            )
            self._composing_categories = tuple(self._category_to_unit_and_exps.keys())
            self._category_info = None  # type:ignore[assignment]
            return

        self._is_derived = False

        # changes to accommodate making operations with derived units (internally the
        # information must be a dict)
        if category.__class__ != str:
            raise TypeError("Only str is accepted. %s is not." % category.__class__)

        # Getting the category should be enough to check that it's valid.
        category_info = unit_database.GetCategoryInfo(category)
        self._category_info = category_info

        # if no unit was given, assume base unit for this quantity_type
        if unit is None:
            unit = category_info.default_unit
        else:
            if unit.__class__ != str:
                raise TypeError("Only str is accepted. %s is not." % unit.__class__)

            try:
                unit_database.CheckCategoryUnit(category, unit)
            except InvalidUnitError as e:
                is_legacy, unit = FixUnitIfIsLegacy(unit)
                if is_legacy:
                    unit_database.CheckCategoryUnit(category, unit)
                else:
                    raise e

        # store it as odict so that we can have a decent order when creating a string from
        # an operation.
        category_to_unit_and_exps = OrderedDict()
        category_to_unit_and_exps[category] = [unit, 1]
        self._category_to_unit_and_exps = category_to_unit_and_exps  # type:ignore[assignment]

        self._category = category
        self._quantity_type = unit_database.GetCategoryQuantityType(category)
        self._unit = unit
        self._tobase = self._unit_database.GetInfo(
            self._quantity_type, self._unit, fix_unknown=True
        ).tobase
        self._composing_units = unit
        self._composing_categories = category

    def MakeCopy(
        self, category_to_unit_and_exps: Optional[Dict[str, Sequence[Union[str, int]]]] = None
    ) -> "Quantity":
        """
        Creates a new copy of this instance

        .. see:: _CreateDerived for parameter.
        :returns:
            An copy of the current instance.
        """
        if category_to_unit_and_exps is None:
            return self  # As it's immutable, we can just return itself!

        # when creating it, a deepcopy of _category_to_unit_and_exps is done
        ret = Quantity._CreateDerived(
            category_to_unit_and_exps,
            validate_category_and_units=False,
            unknown_unit_caption=self._unknown_unit_caption,
        )
        return ret

    def CreateCopyInstance(
        self, category_to_unit_and_exps: Optional[Dict[str, Sequence[Union[str, int]]]] = None
    ) -> "Quantity":
        """
        Creates a copy of this quantity with a new category/unit.

        .. see:: _CreateDerived for parameter.
        """
        if category_to_unit_and_exps is None:
            return self  # As it's immutable, we can just return itself!
        return self.MakeCopy(category_to_unit_and_exps)

    def Copy(self) -> "Quantity":
        """
        Create a copy of this class.
        """
        return self  # As it's immutable, we can just return itself!

    def __repr__(self) -> str:
        if self._unknown_unit_caption:
            return "Quantity({!r}, {!r}, {!r})".format(
                self.GetCategory(), self._unit, self._unknown_unit_caption
            )

        return "Quantity({!r}, {!r})".format(self.GetCategory(), self._unit)

    def SetUnknownCaption(self, caption: str) -> NoReturn:
        raise ReadOnlyError("Quantity is now read-only.")

    def GetUnknownCaption(self) -> Optional[str]:
        return self._unknown_unit_caption

    def GetUnitCaption(self) -> str:
        unit = self._unit
        if unit == UNKNOWN_UNIT and self._unknown_unit_caption:
            # For now let's leave both (may need further discussions)
            unit = self._unknown_unit_caption + " " + UNKNOWN_UNIT

        return unit

    def GetCategory(self) -> str:
        return self._category

    def _MakeStr(self, repr_and_exp: Any) -> str:
        """
        Used to make a string representation given a string and its exponents

        :type repr_and_exp: list(tuple(str, int))
        :param repr_and_exp:
            List of string, exponent.

        :rtype: str
        :returns:
            A string with the string and the given exponents. E.g.:
            Receiving [('m', 2)] will return m ** 2
            Receiving [('cm', -1)] will return 1 / cm
            Exponents = 0 are not added to the returned string.
        """
        ret = ""

        for rep, exp in repr_and_exp:
            if exp > 0:
                if ret:
                    ret += " * "

                if exp != 1:
                    ret += f"({rep}) ** {exp}"
                else:
                    ret += rep

        added_div = False
        for rep, exp in repr_and_exp:
            if exp < 0:
                if not added_div:
                    added_div = True
                    if ret:
                        ret += " / "
                    else:
                        ret += "1 / "

                if exp != -1:
                    ret += "({}) ** {}".format(rep, abs(exp))
                else:
                    ret += rep

        return ret

    def GetQuantityType(self) -> str:
        return self._quantity_type

    def _CreateUnitsWithJoinedExponentsString(self) -> str:
        """
        Create a string with the joined units and exponents of the units to be shown to the
        user.

        :returns:
            A string with the units with the joined exponents.
            E.g.: m2, 1/m and so on (dependent on the unit it has internally)
        """
        ret = ""
        composing_units = self.GetComposingUnitsJoiningExponents()
        for unit, exp in composing_units:
            if exp > 0:
                if ret:
                    ret += "."

                if exp != 1:
                    ret += f"{unit}{exp}"
                else:
                    ret += unit

        added_div = False
        for unit, exp in composing_units:
            if exp < 0:
                if not added_div:
                    added_div = True
                    if ret:
                        ret += "/"
                    else:
                        ret += "1/"

                ret += unit
                if exp != -1:
                    ret += str(abs(exp))

        return ret

    def GetUnit(self) -> str:
        return self._unit

    unit = property(GetUnit)

    def GetUnitName(self) -> str:
        """
        :rtype: str
        :returns:
            A description of the unit showing all the containing parts in the category,
            units and the exponent for each. This differs from the default unit because the
            default GetUnit will only return the final name of the unit, composing all the
            available parts into a single exponent (e.g. if it's composed of more than one
            'm', each with exponent 1, it would appear 2 times in this method and would appear
            'm2' in the GetUnit).
        """
        repr_and_exp: OrderedDict[Any, Any] = OrderedDict()
        unit_database = self._unit_database

        for category, (unit, exp) in self._category_to_unit_and_exps.items():
            quantity_type = unit_database.GetCategoryQuantityType(category)
            unit_name = unit_database.GetUnitName(quantity_type, unit)
            existing = repr_and_exp.get(unit_name, 0)
            repr_and_exp[unit_name] = existing + exp

        return self._MakeStr(list(repr_and_exp.items()))

    def GetValidUnits(self) -> List[str]:
        """
        Shortcut for getting the valid units

        :returns:
            The valid units.
        """
        return self.GetUnitDatabase().GetValidUnits(self.GetCategory())

    def IsDerived(self) -> bool:
        """
        :returns:
            Returns whether this quantity has derived units.
        """
        return self._is_derived

    def GetCategoryInfo(self) -> CategoryInfo:
        """
        :returns:
            Returns the category info associated with this quantity.
        """
        return self._category_info

    def ConvertScalarValue(self, value: T, to_unit: str) -> T:
        """
        Convert a value to another unit.

        :param value:
            The value to be converted.

        :param to_unit:
            The target unit for the value.

        :returns:
            Returns the scalar converted to the passed unit.
        """
        if not self._is_derived:
            from_unit = self._unit

            # same unit: no conversion needed
            if from_unit == to_unit:
                return value

            other = self._unit_database.GetInfo(self._quantity_type, to_unit, fix_unknown=True)

            return other.frombase(self._tobase(value))
        else:
            return self.Convert(value, to_unit)

    def Convert(self, value: T, to_unit: str) -> T:
        """
        Convert any value object which has a conversion registered (note: ConvertScalarValue may
        be used to convert a float value in a more optimized way).

        :param object value:
            The value to be converted (array, numpy, etc.)

        :param to_unit:
            The target unit for the value.

        :returns:
            An object with values to the passed unit.
        """
        return self._unit_database.Convert(
            self._composing_categories, self._composing_units, to_unit, value
        )

    @classmethod
    def _GetComparison(cls, operator: str, use_literals: bool = False) -> str:
        """
        Method for getting different representations of comparisons for messages, using operator or
        literals.

        :param operator:
            The key to the operator.

        :param use_literals:
            If literals are to be used.

        :returns str:
            A comparison representation, with operator or literal.
        """
        OPERATOR_COMPARISON = {">": ">", "<": "<", ">=": ">=", "<=": "<="}
        LITERALS_COMPARISON = {
            ">": "greater than",
            "<": "less than",
            ">=": "greater or equal to",
            "<=": "less or equal to",
        }
        if use_literals:
            return LITERALS_COMPARISON[operator]

        return OPERATOR_COMPARISON[operator]

    def _RaiseValueError(
        self, value: float, operator: str, limit_value: float, use_literals: bool
    ) -> None:
        """
        Raises a QuantityValidationError exception with a formatted message about the comparison of the value
        with it's limit and it's values as attributes.

        :param value:
            Value with boundary error.

        :param operator:
            The key to the operator.

        :param limit_value:
            Value that defines the limit of the category.

        :param use_literals:
            If literals are to be used in the error message.
        """
        assert self._category_info
        invalid_value_message = "Invalid value for {}: {:g}. Must be {} {!r}.".format(
            self._category_info.caption,
            value,
            self._GetComparison(operator, use_literals),
            limit_value,
        )

        raise QuantityValidationError(
            invalid_value_message,
            self._category_info.caption,
            value,
            self._GetComparison(operator, use_literals),
            limit_value,
        )

    def CheckValue(self, value: Any, use_literals: bool = False) -> None:
        """
        Checks if the passed value is valid for this quantity.

        :param value:
            The value to be checked.

        :raises QuantityValidationError:
            if the value is not valid for this quantity.
        """
        if self._is_derived:  # It's not possible to check value for a derived category.
            return

        category_info = self._category_info
        unit = self._unit

        # checking minimum value
        if category_info.min_value is not None or category_info.max_value is not None:
            # convert value to check limit
            if unit != category_info.default_unit:
                value = self.ConvertScalarValue(
                    value, category_info.default_unit  # type:ignore[arg-type]
                )

            if category_info.min_value is not None:
                if category_info.is_min_exclusive:
                    if not value > category_info.min_value:
                        self._RaiseValueError(value, ">", category_info.min_value, use_literals)
                else:
                    if not value >= category_info.min_value:
                        self._RaiseValueError(value, ">=", category_info.min_value, use_literals)

            # checking maximum value
            if category_info.max_value is not None:
                if category_info.is_max_exclusive:
                    if not value < category_info.max_value:
                        self._RaiseValueError(value, "<", category_info.max_value, use_literals)
                else:
                    if not value <= category_info.max_value:
                        self._RaiseValueError(value, "<=", category_info.max_value, use_literals)

    def GetUnitDatabase(self) -> UnitDatabase:
        return self._unit_database

    def GetCategoryToUnitAndExps(self) -> Dict[str, Sequence[Union[str, int]]]:
        return self._category_to_unit_and_exps

    def GetComposingCategories(self) -> Union[Tuple[str, ...], str]:
        return self._composing_categories

    def GetComposingUnits(self) -> Union[Tuple[UnitExponentTuple, ...], str]:
        return self._composing_units  # type:ignore[return-value]

    def GetComposingUnitsJoiningExponents(self) -> Tuple[UnitExponentTuple, ...]:
        self._composing_units_joining_exponents: Tuple[UnitExponentTuple, ...]
        try:
            return self._composing_units_joining_exponents
        except AttributeError:
            ret: OrderedDict[Any, Any] = OrderedDict()
            for _category, (unit, exp) in self._category_to_unit_and_exps.items():
                existing = ret.get(unit, 0)
                ret[unit] = existing + exp
            self._composing_units_joining_exponents = tuple(ret.items())
        return self._composing_units_joining_exponents

    def GetCategoryToUnitAndExpsCopy(
        self, unit_and_exps: Optional[Dict[str, Sequence[Union[str, int]]]] = None
    ) -> Dict[str, Sequence[Union[str, int]]]:
        """
        Same as Quantity.GetCategoryToUnitAndExps but returns a copy instead of the internal
        instance.

        .. see:: Quantity.GetCategoryToUnitAndExps
        """
        if unit_and_exps is None:
            unit_and_exps = self._category_to_unit_and_exps

        return OrderedDict(
            (category, unit_and_exp[:]) for (category, unit_and_exp) in unit_and_exps.items()
        )

    def __hash__(self) -> int:
        self._hash: int
        try:
            return self._hash
        except AttributeError:
            lst = list(
                (category, tuple(unit_and_exp))
                for (category, unit_and_exp) in self._category_to_unit_and_exps.items()
            )
            lst.append(self._unknown_unit_caption)  # type:ignore[arg-type]
            self._hash = hash(tuple(lst))
        return self._hash

    def __eq__(self, other: object) -> bool:
        """
        Compares if this instance is equivalent to another quantity

        :param object other:
            The object we want to compare to

        :rtype: boo
        :returns:
            True if they're equal and False otherwise
        """
        if not isinstance(other, Quantity):
            return False

        return (
            tuple(self._category_to_unit_and_exps.items())
            == tuple(other._category_to_unit_and_exps.items())
            and self._unknown_unit_caption == other._unknown_unit_caption
        )

    # Used to cast a constant value
    BASE_NUMBER = (int, float)

    OPERATION_ADD = "Sum"
    OPERATION_DIVIDE = "Divide"
    OPERATION_MULTIPLY = "Multiply"
    OPERATION_SUBTRACT = "Subtract"

    # lonly ----------------------------------------------------------------------------------------
    def __abs__(self) -> "Quantity":
        return self

    # right ----------------------------------------------------------------------------------------

    def __rmod__(self, other: Any) -> "Quantity":
        return self.__truediv__(other)

    def __rmul__(self, other: Any) -> "Quantity":
        return self._DoOperation(other, self, self.OPERATION_MULTIPLY)

    def __rsub__(self, other: Any) -> "Quantity":
        return self._DoOperation(other, self, self.OPERATION_SUBTRACT)

    def __radd__(self, other: Any) -> "Quantity":
        return self._DoOperation(other, self, self.OPERATION_ADD)

    # basic ----------------------------------------------------------------------------------------
    def __truediv__(self, other: Any) -> "Quantity":
        return self._DoOperation(self, other, self.OPERATION_DIVIDE)

    def __mod__(self, other: Any) -> "Quantity":
        return self.__truediv__(other)

    def __rtruediv__(self, other: Any) -> "Quantity":
        return self.__truediv__(other)

    def __mul__(self, other: Any) -> "Quantity":
        return self._DoOperation(self, other, self.OPERATION_MULTIPLY)

    def __sub__(self, other: Any) -> "Quantity":
        return self._DoOperation(self, other, self.OPERATION_SUBTRACT)

    def __add__(self, other: Any) -> "Quantity":
        return self._DoOperation(self, other, self.OPERATION_ADD)

    def __pow__(self, exponent: int) -> "Quantity":
        result = self
        for _ in range(exponent - 1):
            result = self._DoOperation(self, result, self.OPERATION_MULTIPLY)
        return result

    def _DoOperation(self, q1: "Quantity", q2: "Quantity", operation: str) -> "Quantity":
        """
        Performs the given operation on the quantities returning the result

        :param Quantity q1:
            The left side operation quantity

        :param Quantity q2:
            The right side operation quantity

        :param OPERATION_* operation:
            The operation to be performed

        :rtype: Quantity
        :returns:
            The resulting quantity from the operation with the proper type and unit
            e.g. ('length', 'm') * ('length', 'm') = ('length **2', 'm2')
        """
        if isinstance(q1, self.BASE_NUMBER):
            return q2
        elif isinstance(q2, self.BASE_NUMBER):
            return q1
        elif isinstance(q1, Quantity) and isinstance(q2, Quantity):
            unit_database = self.GetUnitDatabase()
            op_func = getattr(unit_database, operation)
            q, _v = op_func(q1, q2, 1.0, 1.0)
            return q
        else:
            return NotImplemented


def _ObtainReduced(state: Any) -> Any:
    """
    :param list state:
        The value returned from Quantity.__reduce__ (used in pickle protocol).
    """
    unknown_unit_caption = state.pop(-1)
    return ObtainQuantity(OrderedDict(state), None, unknown_unit_caption)
