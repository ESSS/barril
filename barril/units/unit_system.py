from __future__ import absolute_import, unicode_literals

from ben10.foundation import callback
from ben10.property_ import Property


class UnitSystem(object):
    '''
    Default implementation for a Unit System.
    '''

    def __init__(self, id, caption, units_mapping, read_only=False):
        self._id = id
        self._caption = caption
        self._units_mapping = units_mapping
        self._read_only = read_only
        self.on_default_unit = callback.Callback()

    def GetId(self):
        return self._id

    def GetCaption(self):
        return self._caption

    def SetCaption(self, caption):
        self._caption = caption

    def GetUnitsMapping(self):
        return self._units_mapping

    def IsReadOnly(self):
        return self._read_only

    def SetReadOnly(self, read_only):
        self._read_only = read_only

    # : duplicated signature to comply with Get/Set standard
    GetReadOnly = IsReadOnly
    read_only = Property(GetReadOnly, SetReadOnly)

    def GetDefaultUnit(self, category):
        if not category:
            return None

        return self._units_mapping.get(category, None)

    def RemoveCategory(self, category):
        try:
            del self._units_mapping[category]
            self.on_default_unit(category, None)
        except KeyError:
            # The category is not in the unit system, so there is nothing to do
            pass

    def SetDefaultUnit(self, category, unit):
        self._units_mapping[category] = unit
        self.on_default_unit(category, unit)

    def __eq__(self, other):
        if not IsImplementation(other, UnitSystem):
            return False

        return self.GetId() == other.GetId() and \
            self.GetCaption() == other.GetCaption() and \
            self.GetUnitsMapping() == other.GetUnitsMapping() and \
            self.IsReadOnly() == other.IsReadOnly()

    def __ne__(self, other):
        return not self == other
