from typing import Any
from typing import Dict
from typing import Optional

from oop_ext.foundation import callback
from oop_ext.interface import Attribute
from oop_ext.interface import Interface
from oop_ext.interface import TypeCheckingSupport


class IUnitSystem(Interface, TypeCheckingSupport):
    """
    Interface for unit systems. A unit system defines the default unit for all the categories in the
    application (a units mapping).

    :ivar Callback on_default_unit:
        Callback called when a default unit of the unit system changes.
        Signature: (category, unit).
    """

    on_default_unit: callback.Callback2[str, Optional[str]] = Attribute(
        callback.Callback2[str, Optional[str]]
    )

    def __init__(
        self, id: str, caption: str, units_mapping: Dict[str, str], read_only: bool = False
    ) -> None:
        """
        :param id:
            The ID for the unit system.

        :param caption:
            The name of the unit system.

        :param units_mapping:
            A dict that maps each category to a related unit (which will be set as default).
            The valid categories are defined by the coilib50.units.UnitDatabase.

            E.g.:
                units_mapping = {
                    'length' : 'm',
                    'time' : 's',
                    'weight' : 'kg',
                }

        :param read_only:
            Flag that indicates if the unit system will be read only. Default is False.
        """

    def GetCaption(self) -> str:
        """
        :returns:
            Returns a user-friendly caption.
        """

    def SetCaption(self, caption: str) -> None:
        """
        Sets the caption of the unit system.

        :param caption:
            The caption.
        """

    def GetId(self) -> Optional[str]:
        """
        :returns:
            Returns the ID of the unit system.
        """

    def GetUnitsMapping(self) -> Dict[str, str]:
        """
        :returns:
            Returns the units mapping set of the unit system.
        """

    def GetDefaultUnit(self, category: str) -> Optional[str]:
        """
        :returns:
            Gets the default unit for the given category. If it returns None, it should not change
            objects of that category.
        """

    def SetDefaultUnit(self, category: str, unit: str) -> None:
        """
        Changes the default unit for the given category.

        :param unicode category:
            The category which will have the default unit changed.

        :param unicode unit:
            The new default unit.
        """

    def IsReadOnly(self) -> bool:
        """
        Retrieves if the unit system is read-only or not.

        :returns:
            True or False indicating the read-only property of the unit system.
        """

    def SetReadOnly(self, read_only: bool) -> None:
        """
        Changes the read-only status of this unit system.

        :param bool read_only:
            Flag indicating if the unit system should be read-only.
        """

    def RemoveCategory(self, category: str) -> None:
        """
        Removes the given category from the categories map.

        :param category:
            The category to remove
        """

    def __eq__(self, other: Any) -> bool:
        """eq operator"""
