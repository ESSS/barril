from __future__ import absolute_import, unicode_literals

from ben10.foundation import callback
from ben10.foundation.decorators import Implements
from ben10.interface import ImplementsInterface, IsImplementation
from ben10.property_ import Property
from coilib50.units.unit_system_interface import IUnitSystem


@ImplementsInterface(IUnitSystem)
class UnitSystem(object):
    '''
    Default implementation for a Unit System.
    .. see:: IUnitSystem
    '''

    @Implements(IUnitSystem.__init__)
    def __init__(self, id, caption, units_mapping, read_only=False):
        self._id = id
        self._caption = caption
        self._units_mapping = units_mapping
        self._read_only = read_only
        self.on_default_unit = callback.Callback()

    @Implements(IUnitSystem.GetId)
    def GetId(self):
        return self._id

    @Implements(IUnitSystem.GetCaption)
    def GetCaption(self):
        return self._caption

    @Implements(IUnitSystem.SetCaption)
    def SetCaption(self, caption):
        self._caption = caption

    @Implements(IUnitSystem.GetUnitsMapping)
    def GetUnitsMapping(self):
        return self._units_mapping

    @Implements(IUnitSystem.IsReadOnly)
    def IsReadOnly(self):
        return self._read_only

    @Implements(IUnitSystem.SetReadOnly)
    def SetReadOnly(self, read_only):
        self._read_only = read_only

    # : duplicated signature to comply with Get/Set standard
    GetReadOnly = IsReadOnly
    read_only = Property(GetReadOnly, SetReadOnly)

    @Implements(IUnitSystem.GetDefaultUnit)
    def GetDefaultUnit(self, category):
        if not category:
            return None

        return self._units_mapping.get(category, None)

    @Implements(IUnitSystem.RemoveCategory)
    def RemoveCategory(self, category):
        try:
            del self._units_mapping[category]
            self.on_default_unit(category, None)
        except KeyError:
            # The category is not in the unit system, so there is nothing to do
            pass

    @Implements(IUnitSystem.SetDefaultUnit)
    def SetDefaultUnit(self, category, unit):
        self._units_mapping[category] = unit
        self.on_default_unit(category, unit)

    @Implements(IUnitSystem.__eq__)
    def __eq__(self, other):
        if not IsImplementation(other, IUnitSystem):
            return False

        return self.GetId() == other.GetId() and \
            self.GetCaption() == other.GetCaption() and \
            self.GetUnitsMapping() == other.GetUnitsMapping() and \
            self.IsReadOnly() == other.IsReadOnly()

    @Implements(IUnitSystem.__ne__)
    def __ne__(self, other):
        return not self == other
