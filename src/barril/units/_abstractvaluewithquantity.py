from typing import Any
from typing import cast
from typing import ClassVar
from typing import List
from typing import NoReturn
from typing import Optional
from typing import overload
from typing import Type
from typing import TypeVar
from typing import Union

from oop_ext.interface import ImplementsInterface

from ._quantity import ObtainQuantity
from ._quantity import Quantity
from .interfaces import IObjectWithQuantity
from .interfaces import IQuantity
from barril.units.unit_database import CategoryInfo
from barril.units.unit_database import UnitDatabase

__all__ = ["AbstractValueWithQuantityObject"]


T = TypeVar("T", bound="AbstractValueWithQuantityObject")


@ImplementsInterface(IObjectWithQuantity, IQuantity)
class AbstractValueWithQuantityObject:
    """
    This is an abstract class that provides a default implementation for having a class
    that has a value associated with a quantity.

    Subclasses should only provide a method for getting and setting the value, as it may be a
    numarray object, list of floats, etc (so, the user may want to call it GetValue, GetValues,
    GetNumarray, ...).

    .. see:: L{Scalar} for an implementation example
    """

    def __init__(
        self, category: Union[str, Quantity], value: Any = None, unit: Optional[str] = None
    ):
        # NOTE: we don't even try to add overloads here because each subclass defines their own
        # overloads, often in confusing ways; adding them here would just add to the
        # confusion.

        unit_database = UnitDatabase.GetSingleton()
        if isinstance(category, Quantity):
            quantity = category

            assert unit is None, "If quantity is given, the unit must not!"

            if value is None:
                value = self._GetDefaultValue(quantity.GetCategoryInfo())

        else:
            if not isinstance(category, str):
                # Support for creating a scalar as:
                # Scalar(10, 'm')
                # Scalar(10, 'm', 'length')
                value, unit, category = category, value, unit  # type:ignore[assignment]

            if value is None or unit is None:
                if value is None:
                    category_info = unit_database.GetCategoryInfo(category)
                    value = self._GetDefaultValue(category_info, unit)
                    if unit is None:
                        unit = category_info.default_unit
                        assert unit is not None
                else:
                    # Note: if the category is given with a value, the unit MUST also be given.
                    # (because if later we change the default unit, the original category would be wrong).
                    assert (
                        unit is not None
                    ), "If category and value are given, the unit must be specified too."

            quantity = ObtainQuantity(unit, category)  # type:ignore[arg-type, assignment]

        self._quantity = quantity
        self._InternalCreateWithQuantity(quantity, value, unit_database)

    def _GetDefaultValue(self, category_info: CategoryInfo, unit: Optional[str] = None) -> Any:
        raise NotImplementedError

    def _InternalCreateWithQuantity(
        self, quantity: Quantity, value: Any, unit_database: Optional[UnitDatabase] = None
    ) -> None:
        raise NotImplementedError

    def IsValid(self) -> bool:
        """
        :rtype: bool
        :returns:
            Checks if current state is valid.
            Should be implemented by each derived implementation.
        """
        if self.GetQuantity().IsDerived():
            return True
        try:
            self.CheckValidity()
        except ValueError:
            return False
        return True

    def CheckValidity(self) -> None:
        raise NotImplementedError

    def ConvertScalarValue(self, value: Any, to_unit: str) -> Any:
        raise NotImplementedError

    def HasCategory(self) -> bool:
        """
        Returns whether this instance has any associated category

        :returns:
            If there's some category composing this object
        """
        return len(self._quantity.GetComposingCategories()) > 0

    # UnitDatabase ---------------------------------------------------------------------------------
    def GetUnitDatabase(self) -> UnitDatabase:
        """
        :rtype: UnitDatabase
        :returns:
            The unit database that was used in the creation of this object.
        """
        return self._quantity.GetUnitDatabase()

    # Quantity -------------------------------------------------------------------------------------
    def GetQuantity(self) -> Quantity:
        """
        :rtype: Quantity
        :returns:
            The Quantity that is associated with this object.
        """
        return self._quantity

    # Category -------------------------------------------------------------------------------------
    def GetCategory(self) -> str:
        return self._quantity.GetCategory()

    category = property(GetCategory)

    # QuantityType ---------------------------------------------------------------------------------
    def GetQuantityType(self) -> str:
        return self._quantity.GetQuantityType()

    quantity_type = property(GetQuantityType)

    # Unit -----------------------------------------------------------------------------------------
    def GetUnit(self) -> str:
        return self._quantity.GetUnit()

    unit = property(GetUnit)

    # UnitDatabase Shortcuts -----------------------------------------------------------------------
    def GetUnitName(self) -> str:
        """
        :rtype: str
        :returns:
            Returns a user-friendly name for the given unit (i.e.: 'm' would me 'meters')
        """
        return self._quantity.GetUnitName()

    def GetValidUnits(self) -> List[str]:
        """
        :rtype: list(str)
        :returns:
            Returns a list with all the valid units for the category for this object + the current
            unit if it's not in the list of valid units (because it may be using a unit valid for
            the quantity type even if it doesn't match a unit in the category).
        """
        valid_units = self.GetUnitDatabase().GetValidUnits(self.GetCategory())
        current_unit = self.GetQuantity().GetUnit()
        if current_unit not in valid_units:
            valid_units.append(current_unit)
        return valid_units

    @classmethod
    def CreateWithQuantity(cls: Type[T], quantity: Quantity, *args: object, **kwargs: object) -> T:
        """
        This is a secondary interface for creating the object with an existing quantity.

        :param Quantity quantity:
            The quantity for this object

        @param args and kwargs: Those are dependent on the actual class -- this parameters
            are passed directly to _InternalCreateWithQuantity.
        """

        class Stub:
            pass

        stub = Stub()  # type:ignore[assignment]
        stub.__class__ = cls  # type:ignore[assignment]
        stub._InternalCreateWithQuantity(quantity, *args, **kwargs)  # type:ignore[attr-defined]
        return cast(T, stub)

    # Copy -----------------------------------------------------------------------------------------
    def Copy(self: T) -> T:
        """
        :returns:
            Returns self, it is immutable.
        """
        return self

    def CreateCopyInstance(self: T) -> T:
        """
        :rtype: Scalar
        :returns:
            Returns a new scalar that's a copy of this scalar.
        """
        return self

    def __copy__(self: T) -> T:
        """
        Copy protocol.
        """
        return self.Copy()

    def __deepcopy__(self: T, memo: object) -> T:
        """
        Copy protocol.
        """
        return self.Copy()

    def GetAbstractValue(self, unit: Optional[str] = None) -> Any:
        raise NotImplementedError

    def CreateCopy(
        self: T,
        value: Any = None,
        unit: Optional[str] = None,
        category: Optional[str] = None,
        **kwargs: object
    ) -> T:
        try:
            if value is None:
                value = self.GetAbstractValue(unit)

            if unit is None and category is None:
                return self.CreateWithQuantity(self._quantity, value=value, **kwargs)

            elif category is not None:
                if unit is None:
                    raise TypeError("If category is given, the unit must be specified too.")

                return self.CreateWithQuantity(
                    ObtainQuantity(unit, category), value=value, **kwargs
                )

            elif unit is not None:
                if self._quantity.GetCategory():
                    return self.CreateWithQuantity(
                        ObtainQuantity(unit, self._quantity.GetCategory()), value=value, **kwargs
                    )
                else:
                    # Handling empty quantity
                    return self.CreateWithQuantity(ObtainQuantity(unit), value=value, **kwargs)

            else:
                raise RuntimeError("Execution should never get here!")

        except TypeError as e:
            raise TypeError(
                "Error creating new instance of %s: %s\n"
                "(Should be overridden in '%s' class if it takes parameters in __init__)"
                % (self.__class__.__name__, e, self.__class__.__name__)
            )

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> NoReturn:
        raise NotImplementedError(
            "Objects with a quantity are not hashable (as they're usually mutable)."
        )

    # Format ---------------------------------------------------------------------------------------

    FORMATTED_SUFFIX_FORMAT = " [%s]"

    @classmethod
    def GetFormattedSuffixFormat(cls) -> str:
        """
        Returns the formatted suffix for the unit.

        :returns:
            The formatted suffix
        """
        return cls.FORMATTED_SUFFIX_FORMAT

    @classmethod
    def SetFormattedSuffixFormat(cls, pattern: str) -> None:
        """
        Sets the format for the formatted text suffix, which may include the unit (Use "%s" to
        place the unit.).

        :param pattern:
            A format-like string containing one C{%s} format code
        """
        try:
            pattern % "unit"
        except TypeError as e:
            raise TypeError(
                "Incompatible pattern for Scalar suffix. Expected a format for a str value."
            ) from e
        cls.FORMATTED_SUFFIX_FORMAT = pattern

    def GetFormattedSuffix(self, unit: Optional[str] = None) -> str:
        """
        Returns the suffix for the formatted string using the current unit.

        :rtype: str
        :returns:
            The suffix
        """
        if unit is None:
            unit = self.GetUnit()
        return self.FORMATTED_SUFFIX_FORMAT % unit

    #: sentinel used to change the category of the object (see ChangeCategory in subclasses)
    DEFAULT_CATEGORY_VALUE: ClassVar[Any] = object()
    #: sentinel used to change the category of the object (see ChangeCategory in subclasses)
    CURRENT_VALUE: ClassVar[Any] = object()
