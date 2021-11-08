from typing import Any
from typing import Dict
from typing import Optional

from oop_ext.foundation import callback
from oop_ext.foundation.decorators import Implements
from oop_ext.interface import ImplementsInterface
from oop_ext.interface import IsImplementation

from .unit_system_interface import IUnitSystem


@ImplementsInterface(IUnitSystem)
class UnitSystem:
    """
    Default implementation for a Unit System.
    .. see:: IUnitSystem
    """

    @Implements(IUnitSystem.__init__)
    def __init__(
        self,
        id: Optional[str],
        caption: str,
        units_mapping: Dict[str, str],
        read_only: bool = False,
    ) -> None:
        self._id = id
        self._caption = caption
        self._units_mapping = units_mapping
        self._read_only = read_only
        self.on_default_unit: callback.Callback2[str, Optional[str]] = callback.Callback2()

    @Implements(IUnitSystem.GetId)
    def GetId(self) -> Optional[str]:
        return self._id

    @Implements(IUnitSystem.GetCaption)
    def GetCaption(self) -> str:
        return self._caption

    @Implements(IUnitSystem.SetCaption)
    def SetCaption(self, caption: str) -> None:
        self._caption = caption

    @Implements(IUnitSystem.GetUnitsMapping)
    def GetUnitsMapping(self) -> Dict[str, str]:
        return self._units_mapping

    @Implements(IUnitSystem.IsReadOnly)
    def IsReadOnly(self) -> bool:
        return self._read_only

    @Implements(IUnitSystem.SetReadOnly)
    def SetReadOnly(self, read_only: bool) -> None:
        self._read_only = read_only

    # : duplicated signature to comply with Get/Set standard
    GetReadOnly = IsReadOnly
    read_only = property(GetReadOnly, SetReadOnly)

    @Implements(IUnitSystem.GetDefaultUnit)
    def GetDefaultUnit(self, category: str) -> Optional[str]:
        if not category:
            return None

        return self._units_mapping.get(category, None)

    @Implements(IUnitSystem.RemoveCategory)
    def RemoveCategory(self, category: str) -> None:
        try:
            del self._units_mapping[category]
            self.on_default_unit(category, None)
        except KeyError:
            # The category is not in the unit system, so there is nothing to do
            pass

    @Implements(IUnitSystem.SetDefaultUnit)
    def SetDefaultUnit(self, category: str, unit: str) -> None:
        self._units_mapping[category] = unit
        self.on_default_unit(category, unit)

    @Implements(IUnitSystem.__eq__)
    def __eq__(self, other: Any) -> bool:
        if not IsImplementation(other, IUnitSystem):
            return False

        return (
            self.GetId() == other.GetId()
            and self.GetCaption() == other.GetCaption()
            and self.GetUnitsMapping() == other.GetUnitsMapping()
            and self.IsReadOnly() == other.IsReadOnly()
        )
