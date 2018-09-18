from __future__ import absolute_import, unicode_literals

import copy
from functools import total_ordering

import six

from barril._foundation.types_ import CheckType
from barril.basic.fraction import FractionValue

from ._abstractvaluewithquantity import AbstractValueWithQuantityObject
from ._quantity import ObtainQuantity
from .unit_database import UnitDatabase


@total_ordering
class FractionScalar(AbstractValueWithQuantityObject):
    '''
    Base class for objects similar to scalars, but that represent its value as L{FractionValue}
    instance instead of a float. Useful to describe diameters for
    pipes and wells in a more natural way to the user (for instance, "5 3/4 inches").
    '''

    def _InternalCreateWithQuantity(self, quantity, value, unit_database=None):
        '''
        For internal use only. Is used to initialize the actual quantity.

        :type quantity: unicode or IQuantity
        :param quantity:
            The quantity of this scalar.

        :param FractionValue value:
            The initial value
        '''
        # Considering fraction values values are easily coerced from float values (though it is
        # important to note the opposite is not true) if the input value is not a fraction already
        # try to convert value to float. This also makes this subclass SetValue interface compatible
        # with superclass interface.
        try:
            if type(value) != FractionValue:
                value = FractionValue(number=float(value))
        except:
            # If not a fraction and coercion to float fails, use CheckType to provide a better error
            # message.
            CheckType(value, (FractionValue, float))

        self._value = value
        self._quantity = quantity
        self._unit_database = unit_database or UnitDatabase.GetSingleton()

    def CheckValidity(self):
        '''
        :raises ValueError: when current value is wrong somehow (out of limits, for example).
        '''
        self._quantity.CheckValue(float(self._value))

    # Value ----------------------------------------------------------------------------------------
    def GetAbstractValue(self, unit=None):
        '''

        :param unit:
        '''
        if unit is None:
            return self._value

        return self.ConvertFractionValue(
            self._value,
            self._quantity,
            self.unit,
            unit
        )

    GetValue = GetAbstractValue
    value = property(GetAbstractValue)

    def _GetDefaultValue(self, category_info, unit=None):
        '''

        :param category_info:
        :param unit:
        '''
        value = category_info.default_value
        if unit is not None:
            # needs to convert value to default unit
            value = ObtainQuantity(
                category_info.default_unit, category_info.category).ConvertScalarValue(value, unit)

        return value

    def GetValueAndUnit(self):
        return (self.GetValue(), self.GetUnit())

    @classmethod
    def ConvertFractionValue(cls, fraction_value, quantity, from_unit, to_unit):
        '''
        Converts the given fraction value to the given unit.

        :type fraction_value: L{FractionValue}
        :param fraction_value:
            the fraction value to convert

        :type quantity: IQuantity or unicode
        :param quantity:
            the IQuantity object to use in the conversion, or the quantity type itself

        :type from_unit: L{FractionValue}
        :param from_unit:
            current unit of the given fraction value

        :type to_unit: L{FractionValue}
        :param to_unit:
            the unit to convert the fraction value to

        :rtype: L{FractionValue}
        :returns:
            the converted fraction value
        '''
        # check if a quantity type unicode was passed
        if quantity.__class__ == six.text_type:
            # Note: actually ignoring the initial quantity type in this case because we
            # do the operation just using the from unit which may have any category (i.e.
            # the important thing is the quantity type, so, it can be created with the
            # default category).
            quantity = ObtainQuantity(from_unit)

        convert_to_quantity = ObtainQuantity(from_unit, quantity.GetComposingCategories())
        converted_number = convert_to_quantity.ConvertScalarValue(fraction_value.GetNumber(), to_unit)

        # convert the number
        result = FractionValue(number=converted_number)
        # convert fraction's numerator
        if fraction_value.GetFraction() is not None:
            converted_numerator = convert_to_quantity.ConvertScalarValue(
                fraction_value.GetFraction().numerator, to_unit)

            converted_fraction = copy.copy(fraction_value.GetFraction())
            converted_fraction.numerator = converted_numerator
            result.SetFraction(converted_fraction)
        return result

    # GetFormatted ------------------------------------------------------------------------------------
    def GetFormattedValue(self, unit=None, value_format=None):
        '''
        Returns the value part, that is, the number and fraction.

        :rtype: C{unicode}
        :returns:
            the formatted string
        '''
        return self.GetValue(unit).GetLocalizedString()

    def __str__(self):
        '''
        unicode() operator.

        :rtype: C{unicode}
        :returns:
            the string representation
        '''
        return self.GetFormatted()

    if six.PY2:
        __unicode__ = __str__
        del __str__

    def GetFormatted(self, unit=None):
        '''
        Returns the string representation for this FractionScalar.

        :param unicode unit:
            If None, returns the current unit, otherwise, returns the string representation of the
            value converted to the given unit.

        :rtype: unicode
        :returns:
            The string representation
        '''
        return self.GetFormattedValue(unit) + self.GetFormattedSuffix(unit)

    def __repr__(self):
        '''
        repr() operator.

        :rtype: C{unicode}
        :returns:
            the string representation
        '''
        return 'FractionScalar(%r, value=%r, unit=%r)' % (self._quantity.GetCategory(), self._value, self.unit)

    # Equality -------------------------------------------------------------------------------------
    def __eq__(self, other):
        '''
        == operator.

        :type other: L{FractionScalar}
        :param other:
            other fraction scalar

        :rtype: C{bool}
        :returns:
            if other is equal to self
        '''
        return type(self) == type(other) and self._value == other.value and \
            self._quantity == other._quantity

    def __lt__(self, other):
        '''
        Comparison between objects.

        :param FractionScalar other:
            The object to be compared to

        :rtype: 1 if this object is greater than the other, -1 it is less than, 0 if they are equal.
        '''
        # this is exactly the same comparison performed by the Scalar, however as they don't share
        # a base class where this method would fit, it was decided to implement it here, instead
        # of creating a base class just because of this method
        if self.quantity_type != other.quantity_type:
            msg = 'can not compare scalars of different quantity types: %r != %r'
            raise TypeError(msg % self.quantity_type, other.quantity_type)

        v1 = self._value
        v2 = other.GetValue(self.unit)
        return v1 < v2

    # RegisterFractionScalarConversion -----------------------------------------
    @classmethod
    def RegisterFractionScalarConversion(cls):
        '''
        Register a special unit conversion for FractionScalar.

        :param UnitDatabase db_unit:
            The unit-database instance to register the conversion into.
        '''

        def ConvertFractionScalar(db_unit, quantity_type, from_unit, to_unit, value):
            '''
            Converts the given Fraction Scalar by applying the converts method of this class.
            '''
            converted = cls.ConvertFractionValue(value, quantity_type, from_unit, to_unit)
            return FractionValue(number=float(converted))

        UnitDatabase.RegisterAdditionalConversionType(FractionValue, ConvertFractionScalar)


FractionScalar.RegisterFractionScalarConversion()
