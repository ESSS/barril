from __future__ import absolute_import, unicode_literals

from six.moves import zip  # @UnresolvedImport

from coilib50.subject import Subject

from ._array import Array
from .unit_database import InvalidUnitError, UnitDatabase

__all__ = ["UnitTable"]


#===================================================================================================
# UnitTable
#===================================================================================================
class UnitTable(Subject):

    Subject.Properties(
        categories=None,
        units=None,
        values=None,
    )

    def __init__(self, categories):
        Subject.__init__(self)
        self.categories = categories
        # default unit database
        self.unit_database = UnitDatabase.GetSingleton()

        # create array for each category
        self._arrays = []
        for category in self.categories:
            array = Array(category)
            self._arrays.append(array)

        # initialize units
        self.units = []
        for category in self.categories:
            self.units.append(self.unit_database.GetDefaultUnit(category))
        self.units = tuple(self.units)

#-------------------------------------------------------------------- Values

    def SetValues(self, values, units=None):
        '''
        Set the table values.

        :type values: C{list of tuples, with each tuple item a float}
        :param values:
            a list of rows, with one column per tuple item

        :type units: If given, a list of units, one for each column. If one of the items on the list
        :param units:
            is None, use the current unit for that column
        :type  units: C{sequence of unicode or None}

        .. note:: passing units DOES NOT change the current units.
        '''
        if units is not None:
            # convert to a list because we might change its contents
            units = list(units)
            if len(self.categories) != len(units):
                raise InvalidUnitError(tr('Values vector must have the same length as units vector'))
            for index, (category, unit) in enumerate(zip(self.categories, units)):
                if unit is None:
                    units[index] = self.units[index]
                else:
                    self.unit_database.CheckCategoryUnit(category, unit)
            # convert back to a tuple
            units = tuple(units)
        else:
            units = self.units

        values_t = list(zip(*values))

        if values:
            if len(self._arrays) != len(values_t):
                raise RuntimeError(tr('Number of columns must be %d' % len(self._arrays)))

            new_arrays = []
            for array, values, unit in zip(self._arrays, values_t, units):
                new_arrays.append(array.CreateCopy(values=values, unit=unit))
            self._arrays = new_arrays

        else:
            # clear all arrays
            new_arrays = []
            for array in self._arrays:
                new_arrays.append(array.CreateCopy(values=[]))
            self._arrays = new_arrays

        self.on_values(self, values)

    def GetValues(self, units=None):
        '''
        Get the table values.

        :type units: a list of units for the columns to be returned. If one of the items on the list
        :param units:
            is None, use the current unit for that column
        :type  units: C{sequence of unicode or None}
        '''
        if units is None:
            units = self.units

        values = []
        for index, (array, unit) in enumerate(zip(self._arrays, units)):
            if unit is None:
                unit = self.units[index]
            values.append(array.GetValues(unit))

        return list(zip(*values))

#---------------------------------------------------------------------- Equality

    def __eq__(self, other):
        return self.categories == other.categories and self.values == other.values

    def __neq_(self, other):
        return not self == other

#---------------------------------------------------------------------- Copy

    def CreateCopyInstance(self):
        return type(self)(self.categories[:])
