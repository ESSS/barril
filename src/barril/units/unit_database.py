import copy
import math
import traceback
from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import Hashable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Type
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union

import attr
from oop_ext.foundation.singleton import Singleton

from barril._util.types_ import CheckType
from barril.units.interfaces import UnitExponentTuple


if TYPE_CHECKING:
    from barril.units import Quantity

# Contains the registry for all the available unit types.
__all__ = [
    "CategoryInfo",
    "InvalidOperationError",
    "InvalidQuantityTypeError",
    "InvalidUnitError",
    "UnitDatabase",
    "UnitInfo",
    "UnitsError",
]


_LEGACY_TO_CURRENT = {
    ("1000ft3", "Mcf"),
    ("1000m3", "Mm3"),
    ("M(ft3)", "MMcf"),
    ("M(m3)", "MMm3"),
    ("k(ft3)", "Mcf"),
}


def FixUnitIfIsLegacy(unit: str) -> Tuple[bool, str]:
    fixed_unit = unit
    try:
        for legacy, current in _LEGACY_TO_CURRENT:
            fixed_unit = fixed_unit.replace(legacy, current)
        return (unit != fixed_unit), fixed_unit
    except:
        return False, unit


class UnitsError(RuntimeError):
    """
    Base class for errors related to units.
    """


class InvalidQuantityTypeError(UnitsError):
    """
    Error raised when an invalid quantity type is found
    """

    def __init__(self, quantity_type: str, available: Optional[List[str]] = None):
        msg = f"Invalid quantity_type: {quantity_type}"
        if available is not None:
            msg += "\nAvailable:\n" + "\n".join(available)
        UnitsError.__init__(self, msg)


class InvalidUnitError(UnitsError):
    """
    Error raised when an invalid unit is found
    """

    def __init__(
        self,
        unit: str,
        quantity_type: Optional[str] = None,
        category: Optional[str] = None,
        valid_units: Optional[List[str]] = None,
    ):
        if quantity_type is not None:
            msg = f"Invalid unit for quantity_type {quantity_type}: {unit}"

        elif category is not None:
            msg = f"Invalid unit for category {category}: {unit}"

        else:
            msg = f"Invalid unit:{unit}"

        if valid_units is not None:
            msg += " [Valid Units: %s]" % valid_units

        UnitsError.__init__(self, msg)


class InvalidOperationError(UnitsError):
    """
    Error raised when some operation but couldn't actually be performed with the given units.
    E.g.: Summing meters + seconds is not valid (while meters + centimeters would be)
    """


class ComposedUnitError(UnitsError):
    """
    Error raised when a composed unit conversion is performed
    E.g.: Velocity_Array * Concentration_Array = m/s.g/cm3
    """


UnaryConversionFunc = Callable[[float], float]


class UnitInfo:
    """
    Holds information about a unit type
    """

    ADD_STR_INFO_TO_UNIT_INFO = False

    def __init__(
        self,
        quantity_type: str,
        name: str,
        unit: str,
        frombase: Union[str, UnaryConversionFunc],
        tobase: Union[str, UnaryConversionFunc],
        default_category: Optional[str] = None,
    ):
        """
        :param name:
            Name of the unit (e.g.: meter, millimiter).

        :param unit:
            String that represents the unit (symbol - e.g.: m, mm).

        :param frombase:
            the formula to convert from the base to this unit.

        :param tobase:
            The formula to convert from the this unit to the base.

        .. note:: frombase or tobase must be defined having the part that should be transformed as
            a %f, %s or just x
        """

        def MakeLambda(s: str) -> UnaryConversionFunc:
            s = s.replace("%s", "x").replace("%f", "x")
            assert "x" in s
            s.replace("x", "float(x)")
            ret = eval("lambda x:%s" % s)
            ret.__has_conversion__ = True
            return ret

        if isinstance(frombase, str):
            frombase_func = MakeLambda(frombase)
        else:
            frombase_func = frombase

        if isinstance(tobase, str):
            tobase_func = MakeLambda(tobase)
        else:
            tobase_func = tobase

        # The functions added to the UnitInfo must say whether they actually have some
        # conversion. If they do, and it's value is True, they may also have
        # __a__, __b__, __c__, __d__ identifying the posc convertions
        # (used for doing conversions for sci20 grid functions in C++)
        # If it's False, that means that the function will have no actual conversion.

        # If not identified, that means that they do have conversions associated
        if not hasattr(tobase_func, "__has_conversion__"):
            tobase_func.__has_conversion__ = True  # type:ignore[attr-defined]

        if not hasattr(frombase_func, "__has_conversion__"):
            frombase_func.__has_conversion__ = True  # type:ignore[attr-defined]

        self.name = name
        self.unit = unit
        self.frombase = frombase_func
        self.tobase = tobase_func
        self.quantity_type = quantity_type
        self.default_category = default_category

        if UnitInfo.ADD_STR_INFO_TO_UNIT_INFO:
            # must be added for the generation of the c++ version of the conversion
            self.frombase_str = frombase
            self.tobase_str = tobase

    def __hash__(self) -> int:
        return hash(self.unit)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(self, UnitInfo):
            return False
        return self.unit == other.unit


@attr.s(auto_attribs=True)
class CategoryInfo:
    """
    Holds information about a category
    """

    category: str = ""
    quantity_type: str = ""
    valid_units: Optional[List[str]] = attr.Factory(list)  # type:ignore[assignment]
    valid_units_set: Set[str] = attr.Factory(set)
    default_unit: Optional[str] = ""
    default_value: float = 0.0
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    is_min_exclusive: bool = False
    is_max_exclusive: bool = False
    caption: str = ""


T = TypeVar("T")
ConversionFunc = Callable[["UnitDatabase", str, str, str, T], T]


class UnitDatabase(Singleton):
    """
    Registry with all the available quantity types and units that represent the physical units.

    Quantity Types represent the type of the unit, for instance length or temperature, as strings.
    Every quantity type has one or more units associated with it.

    Units represent one specific unit inside a quantity_type, for instance meters and centimeters
    for length.
    """

    PREPOSITIONS_IN_CATEGORY_NAME = ("per", "of")

    @classmethod
    def CreateDefaultSingleton(cls) -> "UnitDatabase":
        result = cls(default_singleton=True)
        cls.FillUnitDatabaseWithPosc(result)
        return result

    # Some aliases to some quantity types
    _ADDITIONAL_CATEGORY_ALIASES = {
        "liquid volume flow rate": "volume flow rate",
        "gas volume flow rate": "volume flow rate",
        "liquid volume": "volume",
        "gas volume": "volume",
        "liquid volume per standard volume": "volume per standard volume",
        "gas volume per standard volume": "volume per standard volume",
        "date": "time",
    }

    @classmethod
    def FillUnitDatabaseWithPosc(
        cls, unit_database: "UnitDatabase", fill_categories: bool = True
    ) -> "UnitDatabase":
        """
        Fills a unit database with the posc values.

        :param UnitDatabase unit_database:
            The unit database to be filled.

        :param bool fill_categories:
            Indicates whether for each quantity type a category with the same name should be created.

        :rtype: UnitDatabase
        :returns:
            The unit database passed as a parameter.
        """
        from .posc import FillUnitDatabaseWithPosc

        unit_database.Clear()
        FillUnitDatabaseWithPosc(
            unit_database, fill_categories=fill_categories, override_categories=True
        )

        if fill_categories:
            for (quantity_alias, quantity_type) in cls._ADDITIONAL_CATEGORY_ALIASES.items():
                unit_database.AddCategory(quantity_alias, quantity_type)

        return unit_database

    def CheckValueForCategory(
        self, category: str, value: float, unit: Optional[str] = None
    ) -> None:
        """
        :param category:
            The category to be checked.

        :param value:
            The value to be checked for the given category.

        :param unit:
            The unit of the value passed (if not available, the default value is considered).
        """
        from ._quantity import ObtainQuantity

        quantity = ObtainQuantity(unit, category)
        quantity.CheckValue(value)

    def CheckDefaultUnitDatabase(self) -> None:
        """
        Checks if this is the default unit-database. If it's not a 'default' unit-database, an
        error is raised together with the stack trace from where it was originally created.

        :raises AssertionError:
            raises error if this was not created as the default unit database.
        """
        if hasattr(self, "_database_created_from"):
            raise AssertionError(
                "Not default unit-database. Creation: \n-------\n%s\n-------\n"
                % (self._database_created_from,)
            )

    # Additional conversions stored at the class (no point in storing them only in an instance,
    # even if it's a singleton). This is done because if a new database is created (say to support just
    # some specific units) it would be painfull to have to register all conversion functions manually.
    # This way we have a singleton that have the application units, other databases can be created
    # but all databases share the same conversion functions.
    #
    # dict of class supported -> conversion function
    # see RegisterAdditionalConversionType
    _additional_conversions: Dict[Type, ConversionFunc] = {}

    def __init__(self, default_singleton: bool = False):
        """
        Initializes the unit manager without any quantity types.

        :param bool default_singleton:
            If True, this is the unit database that's created through the CreateDefaultSingleton
            method. This is needed because any constants created a module or class level must have a
            reference to the default unit-database and not for some other database created in tests
            (so, this flag is used together with CheckDefaultUnitDatabase later on).
        """
        if not default_singleton:
            # If this is not the default singleton, mark from where was it created if we need
            # to check later on.
            from io import StringIO

            s = StringIO()
            traceback.print_stack(file=s)
            self._database_created_from = s.getvalue()

        # Quantities must be cached accordingly to the current unit-database.
        self.quantities_cache: Dict[Hashable, "Quantity"] = {}

        # Dictionary to cache whether a unit is valid in a category.
        self._category_unit_valid: Dict[Tuple[str, str], bool] = {}

        # dict of quantity_type => list of UnitInfo (the first unit in this list is the base unit for
        # the given quantity type)
        self.quantity_types: Dict[str, List[UnitInfo]] = {}

        # dict of unit name => UnitInfo
        self.unit_to_unit_info: Dict[str, UnitInfo] = {}
        self.categories_to_quantity_types: Dict[str, CategoryInfo] = {}

    # ----------------------------------------------- The interfaces below all work with the category

    @classmethod
    def FillSimple(cls, unit_database: "UnitDatabase") -> None:
        unit_database.AddUnitBase("length", "meters", "m")
        unit_database.AddUnit("length", "milimeters", "mm", "%f * 1000.0", "%f / 1000.0")
        unit_database.AddUnit("length", "centimeters", "cm", "%f * 100.0", "%f / 100.0")
        unit_database.AddUnit("length", "kilometers", "km", "%f / 1000.0", "%f * 1000.0")

        unit_database.AddUnitBase("time", "seconds", "s")
        unit_database.AddUnit("time", "minutes", "min", "%f * 60.0", " %f * 60.0")
        unit_database.AddUnit("time", "hours", "h", "%f * 3600.0", " %f * 3600.0")
        unit_database.AddUnit("time", "days", "d", "%f * 86400.0", " %f * 86400.0")

        unit_database.AddCategory("length", "length")
        unit_database.AddCategory("time", "time")

    def AddCategory(
        self,
        category: str,
        quantity_type: Optional[str] = None,
        valid_units: Optional[List[str]] = None,
        override: bool = False,
        default_unit: Optional[str] = None,
        default_value: Optional[float] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        is_min_exclusive: bool = False,
        is_max_exclusive: bool = False,
        caption: str = "",
        from_category: Optional[str] = None,
    ) -> CategoryInfo:
        """Adds a category to the unit-management. If it already exists, throws an error
        if override is not set to True

        :param category:
            The category to be added to the unit-management.

        :param quantity_type:
            The quantity type that this category maps to.

        :param valid_units:
            A set of the valid units for the given category.

        :param override:
            Whether to replace the quantity type for the category.

        :param default_unit:
            The default unit for the category

        :param default_value:
            The default value for the category

        :param min_value:
            Minimum value acceptable. If None, any value can be set.

        :param max_value:
            Maximum value acceptable. If None, any value can be set.

        :param is_min_exclusive:
            If the min_value given is exclusive.

        :param is_max_exclusive:
            If the max_value given is exclusive.

        :param caption:
            User friendly caption for this category.

        :param from_category:
            Category to copy other parameters from.

        :raises UnitsError:
            If the category was already added and override is not set to True
        """
        CheckType(category, str)

        if from_category and quantity_type:
            raise ValueError("cannot pass both quantity_type and from_category")

        if not override and category in self.categories_to_quantity_types:
            raise UnitsError("category %r already registered" % category)

        if min_value is not None and max_value is not None:
            if max_value < min_value:
                raise ValueError(
                    "min_value (%s) must be >= than min_value (%s)" % (min_value, max_value)
                )

        if from_category:
            category_info = self.GetCategoryInfo(from_category)
            quantity_type = category_info.quantity_type
            if valid_units is None:
                valid_units = category_info.valid_units
            if default_unit is None:
                default_unit = category_info.default_unit
            if default_value is None:
                default_value = category_info.default_value
            if min_value is None:
                min_value = category_info.min_value
            if max_value is None:
                max_value = category_info.max_value
            if is_min_exclusive is None:
                is_min_exclusive = category_info.is_min_exclusive
            if is_max_exclusive is None:
                is_max_exclusive = category_info.is_max_exclusive
            if caption is None:
                caption = category_info.caption

        assert quantity_type is not None

        # check if valid_units should inherit from the quantity_type
        if valid_units is not None:
            # valid units given: check if all the given units are valid
            quantity_units = set(self.GetUnits(quantity_type))
            for unit in valid_units:
                if unit not in quantity_units:
                    msg = "unit %r is not valid for quantity type %r.\nQuantity units: %r"
                    raise ValueError(msg % (unit, quantity_type, sorted(quantity_units)))

        # if (min_value is not None or max_value is not None) and default_unit is None:
        if default_unit is None:
            default_unit = self.GetBaseUnit(quantity_type)
            if valid_units and default_unit not in valid_units:
                default_unit = valid_units[0]
        else:
            quantity_units = set(self.GetUnits(quantity_type))
            if default_unit not in quantity_units:
                raise ValueError(
                    "unit %r is not valid for default quantity type %r"
                    % (default_unit, quantity_type)
                )

        # caption
        if not caption:
            caption = category.title()
            # Do not Title prepositions
            for word in self.PREPOSITIONS_IN_CATEGORY_NAME:
                caption = caption.replace(word.title() + " ", word + " ")

        # if the default_value has not been passed
        #   1) min_value defined? ---> min_value
        #   else
        #   2) max_value defined? ---> max_value
        #   else
        #   3) zero
        if default_value is None:
            if is_min_exclusive or is_max_exclusive:
                raise RuntimeError("default_value must be supplied")
            elif min_value is not None:
                default_value = min_value
            elif max_value is not None:
                default_value = max_value
            else:
                default_value = 0.0

        else:  # the default_value is defined

            msg = "Error while adding category %s: default_value %f %s %f"

            if min_value is not None:
                if is_min_exclusive:
                    assert default_value > min_value, msg % (
                        category,
                        default_value,
                        "must be >",
                        min_value,
                    )
                else:
                    assert default_value >= min_value, msg % (
                        category,
                        default_value,
                        "must be >=",
                        min_value,
                    )

            if max_value is not None:
                if is_max_exclusive:
                    assert default_value < max_value, msg % (
                        category,
                        default_value,
                        "must be <",
                        max_value,
                    )
                else:
                    assert default_value <= max_value, msg % (
                        category,
                        default_value,
                        "must be <=",
                        max_value,
                    )

        info = CategoryInfo(
            category=category,
            quantity_type=quantity_type,
            valid_units=valid_units,
            valid_units_set=set(valid_units) if valid_units is not None else set(),
            default_unit=default_unit,
            default_value=default_value,
            min_value=min_value,
            max_value=max_value,
            is_min_exclusive=is_min_exclusive,
            is_max_exclusive=is_max_exclusive,
            caption=caption,
        )

        self.categories_to_quantity_types[category] = info
        return info

    def IsValidCategory(self, category: str) -> bool:
        """
        Check if the given category is valid into the unit database.

        :param category:
            The category to check the validity.

        :returns:
            True is it is a valid category; otherwise False.
        """
        return category in self.categories_to_quantity_types

    def IterCategories(self) -> Iterator[str]:
        """
        Iterator for all the categories.

        :returns:
            An iterator that'll provide all the categories.
        """
        return iter(self.categories_to_quantity_types.keys())

    def GetCategoryInfo(self, category: str) -> CategoryInfo:
        """
        :param category:
            The category we're interested in.

        :returns:
            The category info for the category passed.
        """
        try:
            return self.categories_to_quantity_types[category]
        except KeyError:
            categories_str = ""
            for cat in sorted(self.categories_to_quantity_types.keys()):
                if cat is None:
                    cat = "None"
                categories_str += cat + "\n"
            raise InvalidQuantityTypeError(
                'The category: "%s" is not added to the unit manager.\n'
                "--- Available ---:\n%s" % (category, categories_str)
            )

    def GetCategoryQuantityType(self, category: str) -> str:
        """
        :returns:
            The quantity type of some category.
        """
        return self.GetCategoryInfo(category).quantity_type

    def FindUnitCase(self, category: str, unit: str) -> str:
        """
        Given a unit in any case, returns a unit that is a match with the correct case within
        the unit-database.

        :param category:
            The category for the given unit

        :param unit:
            The unit that should be used to match the case.

        :returns:
            the unit considering the actual case used within the unit database.

        :raises AssertionError:
            if no unit could be found or more than one was found (there should be
            only 1 match considering it in a case-insensitive way).
        """
        category_info = self.GetCategoryInfo(category)
        infos = self.GetInfos(category_info.quantity_type)

        matched = []

        unit_lower = unit.lower()
        for info in infos:
            if info.unit.lower() == unit_lower:
                matched.append(info.unit)

        if len(matched) == 1:
            return matched[0]
        else:
            raise AssertionError(
                "Expected 1 match not considering case for: '%s'. Found: %s"
                % (unit, [u for u in matched])
            )

    def CheckCategoryUnit(self, category: str, unit: str) -> None:
        """
        Check if the given category accepts the passed unit.

        :raises InvalidUnitError:
            if the unit provided is not accepted for this category
        """
        assert category.__class__ == str, f"Expected unit of type str, found {category}"
        assert unit.__class__ == str, f"Expected unit of type str, found {unit}"

        key = (category, unit)
        try:
            # i.e.: if not valid (valid = self._category_unit_valid[key])
            if not self._category_unit_valid[key]:
                raise InvalidUnitError(unit, None, category)
        except KeyError:
            if category.__class__ != str:
                raise TypeError("Only str is accepted. %s is not." % category.__class__)

            try:
                category_info = self.GetCategoryInfo(category)
                # When setting a unit, leave the user set any unit from the quantity type, even if there's
                # a subset for the category (the idea is that the units for the category are only used to
                # filter them in the UI, not really to do internal validations).
                self.CheckQuantityTypeUnit(category_info.quantity_type, unit)
                valid = True
            except UnitsError:
                valid = False

            self._category_unit_valid[key] = valid
            if not valid:
                raise InvalidUnitError(unit, None, category)

    def GetValidUnits(self, category: str) -> List[str]:
        """
        :rtype: list(str)
        :returns:
            The valid units for a given category. If the valid categories weren't given uses the valid units from
            quantity type.
        """
        # Special case: the empty category, as generated by Quantity.CreateEmpty(), has no valid units.
        if category == "":
            return []

        category_info = self.GetCategoryInfo(category)
        if category_info.valid_units is not None:
            return category_info.valid_units
        else:
            if category_info.quantity_type != category:
                return self.GetValidUnits(category_info.quantity_type)

            # the valid units have not been specified for the given category (so, let's return
            # the units for the quantity type)
            return self.GetUnits(category_info.quantity_type)

    def GetDefaultValue(self, category: str) -> float:
        """
        :returns:
            The default value for the given category.
        """
        category_info = self.GetCategoryInfo(category)
        return category_info.default_value

    def GetDefaultUnit(self, category: str) -> str:
        """
        :returns:
            The default unit for the given category.

        .. note::
            This method shouldn't return None, when the default_unit isn't defined for the category
            the quantity type base unit is used.
        """
        category_info = self.GetCategoryInfo(category)
        return category_info.default_unit or ""

    # --------------------- The interfaces below all work with the quantity type and not the category

    def AddUnit(
        self,
        quantity_type: str,
        name: str,
        unit: str,
        frombase: Union[str, UnaryConversionFunc],
        tobase: Union[str, UnaryConversionFunc],
        default_category: Optional[str] = None,
    ) -> None:
        """
        Registers a new unit type.

        :param quantity_type:
            The quantity type for the added unit.

        :param name:
            A user-friendly name for this unit.

        :param unit:
            The unit to be added.

        :param frombase:
            If string, an expression to convert from the base unit of this quantity_type to this
            unit. If callable, must accept a float value that applies the conversion.

        :param tobase:
            If a string, an expression to convert from this unit to the base unit. If callable, must
            accept a float value that applies the conversion.

        .. note:: Each expression must refer to %f or x as the current value of the unit.

        :param default_category:
            The default category for the added unit (if any).
        """
        assert quantity_type is not None
        if unit.__class__ != str:
            raise TypeError("Only str is accepted. %s is not." % unit.__class__)

        if unit is None:
            unit = name
        info = UnitInfo(
            quantity_type, name, unit, frombase, tobase, default_category=default_category
        )
        if unit in self.unit_to_unit_info:
            raise RuntimeError(
                "Unit: %s already added to the unit database for the quantity type: %s (trying to add to: %s)"
                % (unit, self.unit_to_unit_info[unit].quantity_type, quantity_type)
            )
        else:
            self.unit_to_unit_info[unit] = info
        quantity_type_list = self.quantity_types.setdefault(quantity_type, [])

        if unit in [q.unit for q in quantity_type_list]:
            raise RuntimeError("Unit already registered: %s (%s)" % (name, unit))

        quantity_type_list.append(info)

    def AddUnitBase(self, quantity_type: str, name: str, unit: str) -> None:
        """
        Add a base unit type. Inside each quantity_type, there must be at least one Base unit.

        Parameters have the same meaning as in AddUnit().
        """

        def identity(x: Any) -> Any:
            return x

        identity.__has_conversion__ = False  # type:ignore[attr-defined]
        self.AddUnit(quantity_type, name, unit, identity, identity)
        # move the base info to the first position
        # (that's a convention: the base is always in the first position)
        infos = self.quantity_types[quantity_type]
        base = infos[-1]  # was appended to the end in Units.Add
        del infos[-1]
        infos.insert(0, base)

    def GetBaseUnit(self, quantity_type: str) -> Optional[str]:
        """
        :param quantity_type:
            The quantity type for which we want a base unit.

        :returns:
            The base unit of the given quantity_type.

        :raises InvalidQuantityTypeError:
            if the quantity type is not valid
        """
        try:
            infos = self.quantity_types[quantity_type]
            return infos[0].unit
        except KeyError:
            self.CheckQuantityType(quantity_type)
        return None

    def GetDefaultCategory(self, unit: str) -> Optional[str]:
        """
        :param unit:
            The unit for which we want the category.

        :rtype: str or None
        :returns:
            The default category for the passed unit.
        """
        try:
            unit_info = self.unit_to_unit_info[unit]
        except KeyError:
            is_legacy, fixed_unit = FixUnitIfIsLegacy(unit)
            if not is_legacy:
                return None
            unit_info = self.unit_to_unit_info[fixed_unit]
        category = unit_info.default_category
        if category:
            return category
        category = unit_info.quantity_type
        if category in self.categories_to_quantity_types:
            return category
        return None

    def GetQuantityType(self, unit: str) -> Optional[str]:
        """
        :returns:
            A quantity_type that contains the respective unit.
        """
        try:
            return self.unit_to_unit_info[unit].quantity_type
        except KeyError:
            return None

    def FindSimilarUnitMatches(self, unit: str) -> List[str]:
        """
        This function will use heuristics to find similar units in the unit database to the
        passed unit.

        :param unit:
            The unit which doesn't have a direct match in the unit dabatase.

        :returns:
            Returns a list with possible matches for the passed unit, sorted.
        """
        import re

        compiled = re.compile(r"[\./]")
        unit_split = compiled.split(unit.lower())

        close_match = []
        for existing_unit in self.unit_to_unit_info.keys():
            existing_unit_split = compiled.split(existing_unit.lower())
            if len(existing_unit_split) == len(unit_split):
                for a, b in zip(existing_unit_split, unit_split):
                    if not a.startswith(b) and not b.startswith(a):
                        break
                else:
                    close_match.append(existing_unit)

        return sorted(close_match)

    def GetQuantityTypes(self) -> List[str]:
        """
        :returns:
            A list of the available categories, sorted.
        """
        return sorted(self.quantity_types.keys())

    def GetUnits(self, quantity_type: Optional[str] = None) -> List[str]:
        """
        :return:
            The units of that quantity_type (if quantity_type is given) otherwise, returns all
            available units.
        """
        return [x.unit for x in self.GetInfos(quantity_type)]

    def GetUnitName(self, quantity_type: str, unit: str) -> str:
        """
        :returns:
            The user-friendly name for the given unit.
        """
        info = self.GetInfo(quantity_type, unit)
        return info.name

    def GetUnitNames(self, quantity_type: str) -> List[str]:
        """
        :returns:
            The user-friendly names for all the units in the given quantity_type.

        :raises InvalidQuantityTypeError:
        """
        return [x.name for x in self.GetInfos(quantity_type)]

    def GetInfo(
        self, quantity_type: str, unit: str, fix_unknown: bool = False, fix_legacy: bool = True
    ) -> UnitInfo:
        """
        :param bool fix_unknown:
            If True won't raise error if quantity_type is unkwnown (and unit may be anything).
            Returns the unknown unit info in this situation.

        :param bool fix_legacy:
            If True and `unit` is in _LEGACY_TO_CURRENT, then it will return
            the current equivalent unit info.

        :rtype: UnitInfo
        :returns:
            The unit object registered with the given unit

        @raise InvalidQuantityTypeError
        @raise InvalidUnitError
        """

        def TryToGetUnitInfoFromUnit(unit: str) -> Optional[UnitInfo]:
            """
            This is the common case, where the unit matches the quantity type registered.
            """
            try:
                # Common case: unit matches the quantity type registered.
                unit_info = self.unit_to_unit_info[unit]
                if quantity_type == unit_info.quantity_type:
                    return unit_info
            except KeyError:
                pass  # Just ignore and go through the 'uncommon' case.
            return None

        unit_info = TryToGetUnitInfoFromUnit(unit)
        if unit_info is not None:
            return unit_info

        # First check if the quantity_type is a registered category
        try:
            category_info = self.categories_to_quantity_types[quantity_type]
        except KeyError:
            pass
        else:
            quantity_type = category_info.quantity_type

        try:
            quantity_types = self.quantity_types[quantity_type]
        except KeyError:
            raise InvalidQuantityTypeError(quantity_type, sorted(self.quantity_types.keys()))
        else:
            for info in quantity_types:
                if info.unit == unit:
                    return info
            else:
                if fix_unknown:
                    # Before actually triggering the error, handle the unknown case:
                    # We can have an unknown quantity type with a 'known' unit (i.e.: the reader
                    # says it's unknown, but we get a proper label for it in the UI, thus, it's a
                    # known 'unknown' quantity). So, in this case, proceed returning the unknown
                    # quantity unit information.
                    from ._unit_constants import UNKNOWN_QUANTITY_TYPE, UNKNOWN_UNIT

                    if quantity_type == UNKNOWN_QUANTITY_TYPE:
                        quantity_types = self.quantity_types[quantity_type]
                        for info in quantity_types:
                            if info.unit == UNKNOWN_UNIT:
                                return info

                if fix_legacy:
                    is_legacy, fixed_unit = FixUnitIfIsLegacy(unit)
                    if is_legacy:
                        unit_info = TryToGetUnitInfoFromUnit(fixed_unit)
                        if unit_info is not None:
                            return unit_info

                raise InvalidUnitError(
                    unit, quantity_type, valid_units=sorted([info.unit for info in quantity_types])
                )

    def GetInfos(self, quantity_type: Optional[str] = None) -> List[UnitInfo]:
        """
        :returns:
            All UnitInfos from that quantity_type (if quantity_type is given), otherwise return all
            UnitInfos.

        @raise InvalidQuantityTypeError
        """
        if quantity_type is None:
            all_infos = []
            for infos in self.quantity_types.values():
                all_infos.extend(infos)
            return all_infos
        else:
            try:
                return self.quantity_types[quantity_type]
            except KeyError:
                raise InvalidQuantityTypeError(quantity_type, list(self.quantity_types.keys()))

    def CheckQuantityType(self, quantity_type: str) -> None:
        """
        Checks if the quantity type is valid. If it is not, raise an InvalidQuantityTypeError.

        @raise InvalidQuantityTypeError
        @raise InvalidUnitError
        """
        if quantity_type not in self.quantity_types:
            raise InvalidQuantityTypeError(quantity_type, sorted(self.quantity_types))

    def CheckQuantityTypeUnit(self, quantity_type: str, unit: str) -> None:
        """
        Check if the given quantity type has the given unit.

        @raise InvalidUnitError
        """
        # NOTE: Using `fix_legacy=False` because when don't want to fix the legacy unit
        # at this point, we actually want `InvalidUnitError` is the unit is
        # legacy
        self.GetInfo(quantity_type, unit, fix_legacy=False)

    def _ConvertWithExp(
        self,
        quantity_type: str,
        from_unit_exps: Sequence[UnitExponentTuple],
        to_unit_exps: Sequence[UnitExponentTuple],
        value: float,
    ) -> float:
        """
        Converts a value from one unit to another unit considering that the units from and
        to have exponents.

        :param quantity_type:
            The quantity type that has the from and to units.

        :param from_unit_exps:
            The unit and exponent of the "from" unit.

        :param to_unit_exps:
            The unit and exponent of the "to" unit.

        :param float value:
            The value to be converted.

        :rtype: float
        :returns:
            Returns the converted value.
        """
        len_from_unit = len(from_unit_exps)
        len_to_unit = len(to_unit_exps)

        if len_to_unit == 0 or len_from_unit == 0:
            return value

        if len_from_unit != 1:
            raise ComposedUnitError(
                "Can only convert one unit to another (not a composed unit at this point)"
            )

        if len_to_unit != 1:
            raise ComposedUnitError(
                "Can only convert one unit to another (not a composed unit at this point)"
            )

        from_unit, from_exp = from_unit_exps[0]
        to_unit, to_exp = to_unit_exps[0]

        if from_exp != to_exp:
            raise ValueError(
                "Cannot convert among different exponents (%s) to (%s)"
                % ((from_unit, from_exp), (to_unit, to_exp))
            )

        if from_exp == to_exp == 1:
            # Special case handling
            return self.Convert(quantity_type, from_unit, to_unit, value)

        negative = False
        if value < 0.0:
            negative = True
            value = abs(value)

        value = math.pow(value, 1.0 / from_exp)  # Convert from the exponent
        value = self.Convert(quantity_type, from_unit, to_unit, value)
        ret = math.pow(value, to_exp)
        if negative:
            return -ret
        return ret

    @classmethod
    def RegisterAdditionalConversionType(cls, class_: Type, func: ConversionFunc) -> None:
        """
        This function may be used to register conversions for additional classes, not originally
        treated (e.g.: IGridFunction)

        :param type class_:
            This is the class that should be treated. So, when a conversion is requested,
            if a class is an instance of the class passed, it'll be used to do the conversions.

        :param callable func:
            The function that should do the conversion. It'll be called as
            func(unit_database, quantity_type, from_unit_info, to_unit_info, value)
        """
        if class_ not in cls._additional_conversions:
            cls._additional_conversions[class_] = func
        else:
            assert (
                cls._additional_conversions[class_] == func
            ), "The class %s already has a convertion function registered" % (str(class_))

    def Convert(
        self,
        category_or_quantity_type: str,
        from_unit: Union[str, Sequence[UnitExponentTuple]],
        to_unit: Union[str, Sequence[UnitExponentTuple]],
        value: Any,
    ) -> Any:
        """
        Converts a value from one unit to another unit (given the quantity type that contains
        both units), so, note that the quantity type at this point is always the same (can't convert
        units with quantity types that don't match).

        :param category_or_quantity_type:
            The category or quantity type for doing the conversion (if it's a category it's
            converted into the quantity type inside this method).

        :param from_unit:
            A string determining the unit from the value we want to convert or a list of exponents.

        :param to_unit:
            A string determining to convert the value to or a list of exponents.

        :param value:
            The value that should be converted.

        .. note:: that from_unit and to_unit must only have 1 item at this point.

        :returns:
            The converted value
        """
        supported_types = tuple(self._additional_conversions)
        convert_function: Optional[ConversionFunc] = None
        if isinstance(value, supported_types):
            for key, convert_function in self._additional_conversions.items():
                if isinstance(value, key):
                    break  # keep convert_function for later use
            else:
                assert False

        # operations with exponents...
        from_is_list = from_unit.__class__ in (list, tuple)
        to_is_list = to_unit.__class__ in (list, tuple)

        if from_is_list or to_is_list:
            from_unit_exps = cast(list, from_unit) if from_is_list else [(cast(str, from_unit), 1)]
            to_unit_exps = cast(list, to_unit) if to_is_list else [(cast(str, to_unit), 1)]

            # same unit: no conversion needed
            if from_unit_exps == to_unit_exps:
                return value

            if (
                category_or_quantity_type.__class__ in (list, tuple)
                and len(category_or_quantity_type) == 1
            ):
                category_or_quantity_type = category_or_quantity_type[0]
            return self._ConvertWithExp(
                category_or_quantity_type, from_unit_exps, to_unit_exps, value
            )

        from_unit = cast(str, from_unit)
        to_unit = cast(str, to_unit)

        # same unit: no conversion needed
        if from_unit == to_unit:
            return value

        # simple operations (same exponent)
        try:
            quantity_type = self.categories_to_quantity_types[
                category_or_quantity_type
            ].quantity_type
        except KeyError:
            self.CheckQuantityType(category_or_quantity_type)
            quantity_type = category_or_quantity_type

        if convert_function is not None:
            return convert_function(self, quantity_type, from_unit, to_unit, value)

        this = self.GetInfo(quantity_type, from_unit, fix_unknown=True)
        other = self.GetInfo(quantity_type, to_unit, fix_unknown=True)

        if isinstance(value, (float, int)):
            return other.frombase(this.tobase(value))
        else:  # list / tuple
            frombase = other.frombase
            tobase = this.tobase
            values_gen = (frombase(tobase(v)) for v in value)

            if isinstance(value, tuple):
                return tuple(values_gen)
            else:
                return list(values_gen)

    def Clear(self) -> None:
        """
        Removes all the quantity types registered.
        """
        self.quantity_types.clear()
        self.categories_to_quantity_types.clear()
        self.unit_to_unit_info.clear()
        self.quantities_cache.clear()
        self._category_unit_valid.clear()

    # Operations with different quantities ---------------------------------------------------------
    def _DoOperationWithSameQuantity(
        self,
        quantity1: "Quantity",
        quantity2: "Quantity",
        value1: T,
        value2: T,
        operation: Callable[[T, T], T],
    ) -> Tuple["Quantity", T]:
        """
        Given 2 quantities, do an operation that DOES NOT accept the creation of a new composed
        quantity (e.g.: sum, subtraction)
        """
        if quantity1 == quantity2:
            return quantity1, operation(value1, value2)

        else:
            # otherwise, we must transform the units in the quantity1 to their counterparts
            # in the quantity2 (without changing anything in the categories at this time)
            category_to_unit_and_exp1 = copy.deepcopy(quantity1.GetCategoryToUnitAndExps())
            category_to_unit_and_exp2 = copy.deepcopy(quantity2.GetCategoryToUnitAndExps())

            (
                category_to_unit_and_exp1,
                category_to_unit_and_exp2,
                value1,
                value2,
            ) = self._MatchQuantities(
                category_to_unit_and_exp1, category_to_unit_and_exp2, value1, value2
            )

            # at this point the quantity types and units must be the same (the categories may actually
            # be different)
            quantity1 = quantity1.CreateCopyInstance(category_to_unit_and_exp1)
            quantity2 = quantity2.CreateCopyInstance(category_to_unit_and_exp2)

            composing_units1 = set(quantity1.GetComposingUnitsJoiningExponents())
            composing_units2 = set(quantity2.GetComposingUnitsJoiningExponents())
            if composing_units1 != composing_units2:
                if len(composing_units1) == 0:
                    # no unit in the 1st part (just take the 2nd as the correct one)
                    quantity1 = quantity2

                elif len(composing_units2) == 0:
                    pass  # ok, no units in the second part...

                else:
                    raise InvalidOperationError(
                        "Error. Can't do operation because units don't match: (%s != %s)"
                        % (composing_units1, composing_units2)
                    )

            return quantity1, operation(value1, value2)

    def Sum(
        self, quantity1: "Quantity", quantity2: "Quantity", value1: T, value2: T
    ) -> Tuple["Quantity", T]:
        func = lambda a, b: a + b
        return self._DoOperationWithSameQuantity(quantity1, quantity2, value1, value2, func)

    def Subtract(
        self, quantity1: "Quantity", quantity2: "Quantity", value1: T, value2: T
    ) -> Tuple["Quantity", T]:
        func = lambda a, b: a - b
        return self._DoOperationWithSameQuantity(quantity1, quantity2, value1, value2, func)

    def Divide(
        self, quantity1: "Quantity", quantity2: "Quantity", value1: T, value2: T
    ) -> Tuple["Quantity", T]:
        return self._DoOperationResultingInNewQuantity(
            quantity1, quantity2, value1, value2, lambda a, b: a - b, lambda a, b: a / b
        )

    def FloorDivide(
        self, quantity1: "Quantity", quantity2: "Quantity", value1: T, value2: T
    ) -> Tuple["Quantity", T]:
        return self._DoOperationResultingInNewQuantity(
            quantity1, quantity2, value1, value2, lambda a, b: a - b, lambda a, b: a // b
        )

    def Multiply(
        self, quantity1: "Quantity", quantity2: "Quantity", value1: T, value2: T
    ) -> Tuple["Quantity", T]:
        """
        Multiplication with different quantities.

        Rationale:

        - the multiplication of different quantities can result in a derived quantity type.
        - the quantities / values should be transformed if there are quantity types that are
          equal in bot quantities (e.g.: if there's cm in the quantity1 and m in the quantity2,
          the value1 and the quantity1 must be converted to m before proceeding with the
          actual multiplication)
        - note that if a given quantity type has different units in the quantity1 or in
          the quantity2, they must 1st be converted to have the same unit in a given quantity type.
        - after the quantities are compatible, it's just a matter of creating a join of
          the available units and summing the expoents to create the resulting quantity
          (and multiplying the actual values).

        :type quantity1: IQuantity (related to value1)
        :param quantity1:
        :type quantity2: IQuantity (related to value2)
        :param quantity2:
        :type value1: iterable or number
        :param value1:
        :type value2: iterable or number
        :param value2:
        :rtype: tuple(IQuantity, value)
        """
        return self._DoOperationResultingInNewQuantity(
            quantity1, quantity2, value1, value2, lambda a, b: a + b, lambda a, b: a * b
        )

    def _MatchQuantities(
        self,
        category_to_unit_and_exp1: Any,
        category_to_unit_and_exp2: Any,
        value1: Any,
        value2: Any,
    ) -> Tuple[Any, Any, Any, Any]:
        """
        Matches all the units for a given quantity type (so, if a unit 'm' is found, if
        a 'cm' is later found, convert it to 'm' -- as well as it's composing value).

        :rtype: the dicts passed with the quantity types matched to the same units and the corresponding
        values converted to match those changes.
        """
        quantity_types_found_to_used_unit: Dict[Any, Any] = {}

        # 1st thing is putting the same unit for a given quantity type (both sides)
        for c in (category_to_unit_and_exp1, category_to_unit_and_exp2):
            for category, unit_exp in list(c.items()):
                unit, _exp = unit_exp
                quantity_type = self.GetCategoryQuantityType(category)
                used_unit_for_quantity_type = quantity_types_found_to_used_unit.get(quantity_type)
                if used_unit_for_quantity_type is None:
                    quantity_types_found_to_used_unit[quantity_type] = unit
                else:
                    # don't worry about the exponent at this time, just update the unit and the related value.
                    if c is category_to_unit_and_exp1:
                        value1 = self.Convert(
                            quantity_type, unit, used_unit_for_quantity_type, value1
                        )
                    else:
                        value2 = self.Convert(
                            quantity_type, unit, used_unit_for_quantity_type, value2
                        )
                    unit_exp[0] = used_unit_for_quantity_type
        return category_to_unit_and_exp1, category_to_unit_and_exp2, value1, value2

    def _DoOperationResultingInNewQuantity(
        self,
        quantity1: "Quantity",
        quantity2: "Quantity",
        value1: Any,
        value2: Any,
        operation_exp: Any,
        operation: Any,
    ) -> Any:
        """
        Given 2 quantities, do an operation that accepts the creation of a new quantity that is
        composed of the quantities passed (e.g.: division, multiplication).
        """
        from ._quantity import Quantity

        # otherwise, we must transform the units in the quantity1 to their counterparts
        # in the quantity2 (without changing anything in the categories at this time)
        category_to_unit_and_exp1 = quantity1.GetCategoryToUnitAndExpsCopy()
        category_to_unit_and_exp2 = quantity2.GetCategoryToUnitAndExpsCopy()

        (
            category_to_unit_and_exp1,
            category_to_unit_and_exp2,
            value1,
            value2,
        ) = self._MatchQuantities(
            category_to_unit_and_exp1, category_to_unit_and_exp2, value1, value2
        )

        # add the categories to the resulting one
        for category2, (unit2, exp2) in list(category_to_unit_and_exp2.items()):
            if category2 not in category_to_unit_and_exp1:
                exp1 = 0
                category_to_unit_and_exp1[category2] = [unit2, operation_exp(exp1, exp2)]
            else:
                unit_exp1 = category_to_unit_and_exp1[category2]
                unit1, exp1 = unit_exp1  # type:ignore[assignment]
                if unit1 == unit2:
                    unit_exp1[1] = operation_exp(exp1, exp2)  # type:ignore[index]
                else:
                    raise RuntimeError(
                        "This should've been covered already (%s != %s)." % (unit1, unit2)
                    )

        # unit -> expoent
        only_units_expoents: Dict[Any, Any] = {}
        for c, (unit, exp) in list(category_to_unit_and_exp1.items()):
            existing = only_units_expoents.get(unit, 0)
            only_units_expoents[unit] = existing + exp

        # remove the ones that have exponent = 0
        for c, (unit, exp) in list(category_to_unit_and_exp1.items()):
            if exp == 0 or only_units_expoents[unit] == 0:
                # that's ok, it's been removed from the expression...
                del category_to_unit_and_exp1[c]

        result = Quantity.CreateDerived(category_to_unit_and_exp1)
        return result, operation(value1, value2)


class RegisterConversion:

    _registered = False

    @classmethod
    def RegisterNumpyConversion(cls) -> None:
        """
        Register a special unit conversion for numpy arrays.

        :param UnitDatabase db:
            The unit-database instance to register the conversion into.
        """
        import numpy

        def ConvertNumpyArray(
            db: UnitDatabase, quantity_type: str, from_unit: str, to_unit: str, array: Any
        ) -> Any:
            """
            Converts the given numpy array by applying the conversion as if it was a scalar,
            since arrays support the numeric operators, which are applied element-wise.
            """
            from_unit_info = db.GetInfo(quantity_type, from_unit, fix_unknown=True)
            to_unit_info = db.GetInfo(quantity_type, to_unit, fix_unknown=True)

            to_base = from_unit_info.tobase
            from_base = to_unit_info.frombase
            return from_base(to_base(array))

        UnitDatabase.RegisterAdditionalConversionType(numpy.ndarray, ConvertNumpyArray)


RegisterConversion.RegisterNumpyConversion()
