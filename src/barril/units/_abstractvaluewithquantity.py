from __future__ import absolute_import, unicode_literals

import six

from barril.units._quantity import _Quantity
from barril.units.unit_database import UnitDatabase

from ._quantity import ObtainQuantity

__all__ = [str("AbstractValueWithQuantityObject")]  # pylint: disable=invalid-all-object


class AbstractValueWithQuantityObject(object):
    '''
    This is an abstract class that provides a default implementation for having a class
    that has a value associated with a quantity.

    Subclasses should only provide a method for getting and setting the value, as it may be a
    numarray object, list of floats, etc (so, the user may want to call it GetValue, GetValues,
    GetNumarray, ...).

    .. see:: L{Scalar} for an implementation example
    '''

    def __init__(self, category, value=None, unit=None):

        unit_database = UnitDatabase.GetSingleton()
        if category.__class__ == _Quantity:
            quantity = category

            assert unit is None, \
                'If quantity is given, the unit must not!'

            if value is None:
                value = self._GetDefaultValue(quantity.GetCategoryInfo())

        else:
            if category.__class__ != six.text_type:
                # Support for creating a scalar as:
                # Scalar(10, 'm')
                # Scalar(10, 'm', 'length')
                value, unit, category = category, value, unit

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
                    assert unit is not None, \
                        'If category and value are given, the unit must be specified too.'

            assert type(unit) is not bytes
            assert type(category) is not bytes
            quantity = ObtainQuantity(unit, category)

        self._InternalCreateWithQuantity(quantity, value, unit_database)

    def IsValid(self):
        '''
        :rtype: bool
        :returns:
            Checks if current state is valid.
            Should be implemented by each derived implementation.
        '''
        if self.GetQuantity().IsDerived():
            return True
        try:
            self.CheckValidity()
        except ValueError:
            return False
        return True

    def HasCategory(self):
        '''
        Returns whether this instance has any associated category

        :rtype: bool
        :returns:
            If there's some category composing this object
        '''
        return len(self._quantity.GetComposingCategories()) > 0

    # UnitDatabase ---------------------------------------------------------------------------------
    def GetUnitDatabase(self):
        '''
        :rtype: UnitDatabase
        :returns:
            The unit database that was used in the creation of this object.
        '''
        return self._quantity.GetUnitDatabase()

    # Quantity -------------------------------------------------------------------------------------
    def GetQuantity(self):
        '''
        :rtype: Quantity
        :returns:
            The Quantity that is associated with this object.
        '''
        return self._quantity

    # Category -------------------------------------------------------------------------------------
    def GetCategory(self):
        return self._quantity.GetCategory()

    category = property(GetCategory)

    # QuantityType ---------------------------------------------------------------------------------
    def GetQuantityType(self):
        return self._quantity.GetQuantityType()

    quantity_type = property(GetQuantityType)

    # Unit -----------------------------------------------------------------------------------------
    def GetUnit(self):
        return self._quantity.GetUnit()

    unit = property(GetUnit)

    # UnitDatabase Shortcuts -----------------------------------------------------------------------
    def GetUnitName(self):
        '''
        :rtype: unicode
        :returns:
            Returns a user-friendly name for the given unit (i.e.: 'm' would me 'meters')
        '''
        return self._quantity.GetUnitName()

    def GetValidUnits(self):
        '''
        :rtype: list(unicode)
        :returns:
            Returns a list with all the valid units for the category for this object + the current
            unit if it's not in the list of valid units (because it may be using a unit valid for
            the quantity type even if it doesn't match a unit in the category).
        '''
        valid_units = self.GetUnitDatabase().GetValidUnits(self.GetCategory())
        current_unit = self.GetQuantity().GetUnit()
        if current_unit not in valid_units:
            valid_units.append(current_unit)
        return valid_units

    #===============================================================================================
    # __Stub
    #===============================================================================================
    class __Stub(object):
        '''
        Helper class for used in CreateWithQuantity.
        '''

    @classmethod
    def CreateWithQuantity(cls, quantity, *args, **kwargs):
        '''
        This is a secondary interface for creating the object with an existing quantity.

        :param Quantity quantity:
            The quantity for this object

        @param args and kwargs: Those are dependent on the actual class -- this parameters
            are passed directly to _InternalCreateWithQuantity.
        '''

        stub = cls.__Stub()
        stub.__class__ = cls
        stub._InternalCreateWithQuantity(quantity, *args, **kwargs)
        return stub

    # Copy -----------------------------------------------------------------------------------------
    def Copy(self):
        '''
        :rtype: Scalar
        :returns:
            Returns self, since Scalar is immutable
        '''
        return self

    def CreateCopyInstance(self):
        '''
        :rtype: Scalar
        :returns:
            Returns a new scalar that's a copy of this scalar.
        '''
        return self

    def __copy__(self):
        '''
        Copy protocol.
        '''
        return self.Copy()

    def __deepcopy__(self, memo):
        '''
        Copy protocol.
        '''
        return self.Copy()

    def CreateCopy(self, value=None, unit=None, category=None, **kwargs):
        '''
        :rtype: Scalar
        :returns:
            Returns a new scalar that's a copy of this scalar.
        '''
        try:
            if value is None:
                value = self.GetAbstractValue(unit)

            if unit is None and category is None:
                return self.CreateWithQuantity(self._quantity, value=value, **kwargs)

            elif category is not None:
                if unit is None:
                    raise TypeError('If category is given, the unit must be specified too.')

                return self.CreateWithQuantity(ObtainQuantity(unit, category), value=value, **kwargs)

            elif unit is not None:
                if self._quantity.GetCategory():
                    return self.CreateWithQuantity(
                        ObtainQuantity(unit, self._quantity.GetCategory()), value=value, **kwargs)
                else:
                    # Handling empty quantity
                    return self.CreateWithQuantity(
                        ObtainQuantity(unit), value=value, **kwargs)

            else:
                raise RuntimeError("Execution should never get here!")

        except TypeError as e:
            raise TypeError("Error creating new instance of %s: %s\n"
                            "(Should be overridden in '%s' class if it takes parameters in __init__)" %
                            (self.__class__.__name__, e, self.__class__.__name__))


    def __ne__(self, other):
        return not self == other

    def __hash__(self, *args, **kwargs):
        raise NotImplementedError(
            "Objects with a quantity are not hashable (as they're usually mutable).")

    # Format ---------------------------------------------------------------------------------------

    FORMATTED_SUFFIX_FORMAT = ' [%s]'

    @classmethod
    def GetFormattedSuffixFormat(cls):
        '''
        Returns the formatted suffix for the unit.

        :rtype: unicode
        :returns:
            The formatted suffix
        '''
        return cls.FORMATTED_SUFFIX_FORMAT

    @classmethod
    def SetFormattedSuffixFormat(cls, pattern):
        '''
        Sets the format for the formatted text suffix, which may include the unit (Use "%s" to
        place the unit.).

        :param unicode pattern:
            A format-like string containing one C{%s} format code
        '''
        try:
            pattern % 'unit'
        except TypeError as e:
            from barril._foundation.reraise import Reraise
            Reraise(e, 'Incompatible pattern for Scalar suffix. Expected a format for a unicode value.')
        cls.FORMATTED_SUFFIX_FORMAT = pattern

    def GetFormattedSuffix(self, unit=None):
        '''
        Returns the suffix for the formatted string using the current unit.

        :rtype: unicode
        :returns:
            The suffix
        '''
        if unit is None:
            unit = self.GetUnit()
        return self.FORMATTED_SUFFIX_FORMAT % unit

    # : sentinel used to change the category of the object (see ChangeCategory in subclasses)
    DEFAULT_CATEGORY_VALUE = object()
    # : sentinel used to change the category of the object (see ChangeCategory in subclasses)
    CURRENT_VALUE = object()
