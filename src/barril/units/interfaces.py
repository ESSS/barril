"""
Barril basic interfaces are defined here.

Basic concepts used in the interfaces:

Category: Identifies the category for some value. This is defined in the application level. E.g.:
    Well length, Well diameter.

QuantityType: The type of the quantity we're interested in. E.g.: length, depth (this was previously
    defined as Measure, but with different meanings among applications, so, the name Measure has been
    'deprecated' in the favor of this one, so that old-habits about it are not continued -- and it is also
    referenced in posc).

Unit: the unit itself. E.g.: m, m/s, kg

Note: The naming conventions were gathered from posc:
    http://www.posc.org/ebiz/pefxml/patternsobjects.html http://www.posc.org/refs/poscUnits20.xml
"""

from oop_ext.interface import Interface


__all__ = [
    "IQuantity",
    "IScalar",
    "IQuantity2",
    "IQuantity3",
    "IObjectWithQuantity",
    "IArray",
]


class IQuantity(Interface):
    """
    The quantity is an object that has its associated category, quantity type and unit.

    It is important that each value in the application has an associated quantity (because
    otherwise, a value may be meaningless).
    """

    def GetCategory(self):
        """
        :rtype: str
        :returns:
            The constant category for this quantity.
        """

    def GetQuantityType(self):
        """
        :rtype: str
        :returns:
            The constant name of the quantity type for this quantity.
            This method may be slow.
        """

    def GetUnit(self):
        """
        :rtype: str
        :returns:
            The unit for this quantity.
        """


class IQuantity2(Interface):
    """
    Optional interface to the IQuantity used to deal with operations dealing with different
    units which result in derived units.

    With that in mind, this interface defines that all the information (category, quantity type and
    unit) may be dicts instead of only strings, where a dict is a string that points to a given
    expoent.

    In this way, a unit defined as m2/s would be a dict: {'m':2, 's':-1} that is later used to
    do operations.

    This return type is shared for all the 'Gets' defined in this interface

    Quantities that do not define this interface may not be used in operations that may result in
    a derived quantity.
    """

    def GetComposingCategories(self):
        """
        :rtype: tuple(str) or str
        :returns:
            A tuple with the categories used.

            A special use-case is provided if there's a single category with an exponent 1, in which
            case a string is returned (optimization).
            I.e.: instead of returning tuple('length',), 'length' will be returned.

        .. see:: GetComposingUnits to return the actual units/exponents for the categories
        """

    def GetComposingUnits(self):
        """
        :rtype: tuple(tuple(str, int)) or str
        :returns:
            A list that will have an entry for each category in this quantity.
            e.g.:tuple(('m',1), ('m',1))

            A special use-case is provided if there's a single unit with an exponent 1, in which
            case a string is returned (optimization).
            I.e.: instead of returning tuple(('m', 1)), 'm' will be returned.

        .. see:: GetComposingUnitsJoiningExponents
        """

    def GetComposingUnitsJoiningExponents(self):
        """
        :rtype: tuple(tuple(str, int))
        :returns:
            A list with an entry pointing to the total number of exponents found for each unit.
            e.g.:tuple(('m',2))

        .. see:: GetComposingUnits
        """

    def GetCategoryToUnitAndExps(self):
        """
            :rtype: an ordered dictionary with the name of a category -> list with 2 elements:
            [unit, exp] that determines the information about categories, quantities and their
            relations to an expoent.

            .. note:: The same INTERNAL REFERENCE should be returned, and not a copy (so, clients that
            change it WILL cause side-effects in the internal dict -- so, creating a deepcopy is
            the clients responsibility)
        """


class IQuantity3(Interface):
    def GetUnitDatabase(self):
        """
        :rtype: UnitDatabase
        :returns:
            The UnitDatabase to which this quantity is associated.
        """


class IQuantity6(Interface):
    """
    Interface that defines a way to get the unit caption properly. This means that the
    translation will be applied (without changing the internal unit, just its representation
    for the user) and additional info may be set for when an unknown unit is available.
    """

    def GetUnitCaption(self):
        """
        :rtype: str
        :returns:
            The text related to this quantity that should be shown to the user.
        """

    def SetUnknownCaption(self, caption):
        """
        :param str caption:
            The caption to be shown to the user when it's an unknown unit.

            An empty caption means that the regular unit should be shown to the user even
            when unknown.
        """

    def GetUnknownCaption(self):
        """
        :rtype: str
        :returns:
            The caption that's set to be shown to the user when it's an unknown unit.
        """


class IObjectWithQuantity(Interface):
    """
    Interface provided for an object that has an associated quantity.
    """

    def GetQuantity(self):
        """
        :rtype: IQuantity
        :returns:
            The quantity that is associated with this object.
            The quantity may be writable or read-only, depending on the object.
            Actually, it may also implement some of the other IQuantity* interfaces.
        """


class IScalar(IObjectWithQuantity, IQuantity):
    """
    Defines a value with an associated unit, without any support for modification, validation or
    unit conversion.
    """

    def GetValue(self, unit=None):
        """
        :param str unit:
            The unit we want to get the value back.
            Note that, for lightweight scalars, this parameter will be used *only* for verification
            that the stored unit is the expected one.
            For full scalars, it will be used to convert the value into the specified unit.

        :rtype: int, float, FractionValue, etc
        :returns:
            The value stored in this scalar. May be an int, float, etc.
        """

    def GetValueAndUnit(self):
        """
        :rtype: (float, str)
        :returns:
            Tuple with value and current unit name.
        """

    def IsValid(self):
        """
        :rtype: bool
        :returns:
            True if the current value is valid, False otherwise.
        """


class IArray(IObjectWithQuantity):
    """
        The Array defines a list of values with a quantity (so, it implements the IObjectWithQuantity
        interface)
    """

    def GetValues(self, unit=None):
        """
        :param str unit:
            This is the unit in which we want the value

        :rtype: sequence or numpy array.
        :returns:
            A sequence of values (int, double, float, etc)
        """
