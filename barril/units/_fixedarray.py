from __future__ import absolute_import, unicode_literals

from ._array import Array
from ._quantity import Quantity

__all__ = ["FixedArray"]


#===================================================================================================
# FixedArray
#===================================================================================================
class FixedArray(Array):
    '''Represents an Array with fixed number of elements.
    '''
    _dimension = None

    def __init__(
        self,
        dimension,
        category,
        values=None,
        unit=None,
        ):
        '''
        :param int dimension:
            The dimension for this array.

        :type category: string or IQuantity
        :param category:
            The category for the unit point or the IQuantity for this object
            (in this case, the unit will be ignored (if it is passed)).

        :type values: sequence or numpy array
        :param values:
            A sequence with its initial values.

        :param unicode unit:
            Unit (not used if a quantity is passed).
        '''
        if dimension < 2:
            raise ValueError('Dimension MUST be 2 or more')
        self._dimension = dimension

        Array.__init__(self, category, values, unit)

    def _InternalCreateWithQuantity(
        self,
        quantity,
        values=None,
        unit_database=None,
        dimension=None,
        value=None
        ):
        if value is not None:
            if values is not None:
                raise ValueError('Duplicated values parameter given')

            values = value

        if dimension is None:
            try:
                if self._dimension is None:
                    self._dimension = len(values)
            except AttributeError:
                pass

            dimension = self._dimension

        elif hasattr(self, '_dimension'):
            if self._dimension is not None and dimension != self._dimension:
                raise ValueError('Dimension re-definition mismatch: %s != %s' % (self._dimension, dimension))

        if dimension < 2:
            raise ValueError('Dimension MUST be 2 or more')
        self._dimension = dimension

        if values is None:
            values = [0.0] * dimension
        self.CheckValues(values, dimension)

        Array._InternalCreateWithQuantity(self, quantity, values)

    def CreateCopy(self, values=None, unit=None, category=None, **kwargs):
        return Array.CreateCopy(
            self,
            values=values,
            unit=unit,
            category=category,
            dimension=self._dimension,
            **kwargs
        )

    # Values ---------------------------------------------------------------------------------------
    def _GetDefaultValue(self, category_info, unit=None):
        '''

        :param category_info:
        :param unit:
        '''
        return [0.0] * self._dimension

    def CheckValues(self, values, dimension=None):
        '''Checks whether the dimensions consistent with the dimensions in this unit point
        '''
        if dimension is None:
            dimension = self.dimension

        if len(values) != dimension:
            msg = 'Values must have %d elements, but has %d'
            raise ValueError(msg % (dimension, len(values)))

    @classmethod
    def CreateEmptyArray(cls, dimension, values=None):
        '''
        Allows the creation of a array that does not have any associated category nor unit.

        :rtype: Array
        :returns:
            Returns an empty array.
        '''
        if values is None:
            values = [0.0] * dimension

        quantity = Quantity.CreateEmpty()
        return cls.CreateWithQuantity(quantity, dimension=dimension, values=values)

    # Dimension ------------------------------------------------------------------------------------
    def GetDimension(self):
        return self._dimension

    dimension = property(GetDimension)

    # Equality -------------------------------------------------------------------------------------
    def __eq__(self, other):
        return Array.__eq__(self, other) and self.dimension == other.dimension

    def __reduce__(self):
        """
        Defining reduce so that we can pickle fixed arrays.
        """
        return FixedArray, (
            self._dimension,
            self._quantity,
            self.values,
            None,  # Unit defined in quantity
        )

    def ChangingIndex(self, index, value, use_value_unit=True):
        '''
        Creates a FixedArray from based on this FixedArray changing a single value based on the
        passed index.

        i.e.: array.ChangingIndex(0, Scalar(1.0, 'm'))
              will create a new FixedArray where the index == 0 is changed to the passed value.

        :param Scalar|float|tuple value:
            The value to be used to set at the given index.

        :param int index:
            The index which should be changed.

        :param bool use_value_unit:
            If True and a Scalar is passed, the newly created array will have the unit of the
            scalar, not of the original array, otherwise (if False) the FixedArray unit will be
            kept.

        :return FixedArray:
            The created FixedArray.
        '''
        from barril.units import Scalar
        from barril.units import FixedArray

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

    def IndexAsScalar(self, index, quantity=None):
        '''
        :param int index:
            The index which should be gotten as a Scalar.

        :param IQuantity quantity:
            The quantity in which we want the Scalar (uses the FixedArray quantity
            if not passed).

        :return Scalar:
            A Scalar representation of the given index.
        '''
        from barril.units import Scalar
        if quantity is None:
            quantity = self.GetQuantity()
        return Scalar(quantity, self.GetValues(unit=quantity.GetUnit())[index])
