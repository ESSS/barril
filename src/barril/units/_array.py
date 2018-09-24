from __future__ import absolute_import, unicode_literals

import six

from barril._foundation.types_ import IsNumber
from barril.basic.format_float import FormatFloat
from barril.units.unit_database import UnitDatabase

from ._abstractvaluewithquantity import AbstractValueWithQuantityObject
from ._quantity import Quantity

__all__ = [str("Array")]  # pylint: disable=invalid-all-object


class Array(AbstractValueWithQuantityObject):
    '''
    Array represents a sequence of values that also have an unit associated.

    Some ways to construct it (note that usually numpy arrays should be used).

        - Array(numpy.array([0, 1, 2, 3, 4], numpy.float64), 'm')

        - Array([0, 1, 2, 3, 4], 'm')

        - Array('length', [0, 1, 2, 3, 4], 'm')

        - Array(ObtainQuantity('m', 'length'), [0, 1, 2, 3, 4])
    '''

    def __init__(self, category, values=None, unit=None):
        AbstractValueWithQuantityObject.__init__(self, category, value=values, unit=unit)

    def _InternalCreateWithQuantity(self, quantity, values=None, unit_database=None, value=None):
        if value is not None:
            if values is not None:
                raise ValueError('Duplicated values parameter given')
            values = value

        self._value = values
        self._unit_database = unit_database or UnitDatabase.GetSingleton()
        self._quantity = quantity
        self._is_valid = None
        self._validity_exception = None

    def CheckValidity(self):
        '''
        :raises ValueError: when current value is wrong somehow (out of limits, for example).
        '''
        self.ValidateValues(self._value, self._quantity)

    def CreateCopy(self, values=None, unit=None, category=None, **kwargs):
        return AbstractValueWithQuantityObject.CreateCopy(
            self, value=values, unit=unit, category=category, **kwargs)

    # Values ---------------------------------------------------------------------------------------
    def GetAbstractValue(self, unit=None):
        '''@param unit: this is the unit in which we want the values
        :rtype: list(number)
        :returns:
            the values stored. May be an a list of int, float, etc.
        '''
        values = self._value
        if unit is None or unit == self._quantity._unit:
            return values

        def IsListOfTuples(v):
            try:
                return len(v) > 0 and isinstance(v[0], tuple)
            except TypeError:
                return False  # numpy raises a TypeError if it's a 0D array, so ignores it

        if IsListOfTuples(values):
            result = []
            Convert = self._quantity.Convert
            for elem in values:
                result.append(tuple(Convert(v, unit) for v in elem))
            return values.__class__(result)

        else:
            return self._quantity.Convert(values, unit)

    GetValues = GetAbstractValue
    values = property(GetAbstractValue)

    def _GetDefaultValue(self, category_info, unit=None):
        '''

        :param category_info:
        :param unit:
        '''
        return []

    def ValidateValues(self, values, quantity):
        '''Set the value to store in this values_quantity. May be an int,
        float, numarray, list of floats, etc.

        :type values: sequence(values) or numpy array.
        :param values:
            The values to be set.

        :param unicode unit:
            The unit of the values being passed (note that GetUnit will still return the previous
            unit set -- this unit is only to indicate the internal value).
        '''
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

    def _DoValidateValues(self, values, quantity):
        '''
        .. seealso:: :meth:`.ValidateValues`
        '''
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

                        iterator = iter(values)

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
    def CreateEmptyArray(cls, values=None):
        '''
            Allows the creation of a array that does not have any associated
            category nor unit.

            :rtype: Array
        '''
        if values is None:
            values = []

        quantity = Quantity.CreateEmpty()
        return cls.CreateWithQuantity(quantity, values=values)

    # Equality -------------------------------------------------------------------------------------
    def __eq__(self, other):
        if not isinstance(other, Array):
            return False

        return tuple(self.values) == tuple(other.values) \
            and self._quantity == other._quantity \
            and self.unit == other.unit

    def __repr__(self):
        values_str = '[%s]' % ', '.join(six.text_type(v) for v in self.values)
        return '%s(%s, %s, %s)' % (self.__class__.__name__, self.GetQuantityType(), values_str, self.GetUnit())

    def __str__(self):
        '''
        Should return a user-friendly representation of this object.

        :rtype: unicode
        :returns:
            The formatted string
        '''
        if len(self.values) > 0 and isinstance(self.values[0], tuple):
            values_str = ' '.join(six.text_type(v) for v in self.values)
        else:
            values_str = ' '.join((FormatFloat('%g', v)) for v in self.values)

        return values_str + self.GetFormattedSuffix()

    if six.PY2:
        __unicode__ = __str__
        del __str__

    # Basic operators ------------------------------------------------------------------------------
    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return self.values[index]

    def __iter__(self):
        return iter(self.values)

    def __truediv__(self, other):
        return self._DoOperation(self, other, 'Divide')

    def __mul__(self, other):
        return self._DoOperation(self, other, 'Multiply')

    def __add__(self, other):
        return self._DoOperation(self, other, 'Sum')

    def __sub__(self, other):
        return self._DoOperation(self, other, 'Subtract')

    # Right-Basic operators ------------------------------------------------------------------------
    def __rdiv__(self, other):
        return self._DoOperation(other, self, 'Divide')

    def __rmul__(self, other):
        return self._DoOperation(other, self, 'Multiply')

    def __radd__(self, other):
        return self._DoOperation(other, self, 'Sum')

    def __rsub__(self, other):
        return self._DoOperation(other, self, 'Subtract')

    def _DoOperation(self, p1, p2, operation):
        '''
            Actually go on and do an operation considering the data we have to transform considering
            any combination of: number, list and numpy
        '''
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
        operation = getattr(unit_database, operation)

        # if handling numpy, just call it all at once!
        if values_iteration.IsNumpy():
            v0, v1 = next(iter(values_iteration))
            q, v = operation(q1, q2, v0, v1)
            return self.__class__.CreateWithQuantity(q, v)
        else:
            # not numpy: create a new structure to hold the values
            result = []
            for v0, v1 in values_iteration:
                q, v = operation(q1, q2, v0, v1)
                result.append(v)

            if values_iteration.IsTuple():
                result = tuple(result)
            return self.__class__.CreateWithQuantity(q, result)
