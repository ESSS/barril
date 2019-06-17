from oop_ext.foundation import callback
from oop_ext.interface import Attribute, Interface


class IUnitSystem(Interface):
    """
    Interface for unit systems. A unit system defines the default unit for all the categories in the
    application (a units mapping).

    :ivar Callback on_default_unit:
        Callback called when a default unit of the unit system changes.
        Signature: (category, unit).
    """

    on_default_unit = Attribute(callback.Callback)

    def __init__(self, id, caption, units_mapping, read_only=False):
        """
        :param unicode id:
            The ID for the unit system.

        :param unicode caption:
            The name of the unit system.

        :type units_mapping: dict( unicode, unicode )
        :param units_mapping:
            A dict that maps each category to a related unit (which will be set as default).
            The valid categories are defined by the coilib50.units.UnitDatabase.

            E.g.:
                units_mapping = {
                    'length' : 'm',
                    'time' : 's',
                    'weight' : 'kg',
                }

        :param bool read_only:
            Flag that indicates if the unit system will be read only. Default is False.
        """

    def GetCaption(self):
        """
        :rtype: unicode
        :returns:
            Returns a user-friendly caption.
        """

    def SetCaption(self, caption):
        """
        Sets the caption of the unit system.

        :param unicode caption:
            The caption.
        """

    def GetId(self):
        """
        :rtype: unicode
        :returns:
            Returns the ID of the unit system.
        """

    def GetUnitsMapping(self):
        """
        :rtype: dict( unicode, unicode )
        :returns:
            Returns the units mapping set of the unit system.
        """

    def GetDefaultUnit(self, category):
        """
        :rtype: unicode or None
        :returns:
            Gets the default unit for the given category. If it returns None, it should not change
            objects of that category.
        """

    def SetDefaultUnit(self, category, unit):
        """
        Changes the default unit for the given category.

        :param unicode category:
            The category which will have the default unit changed.

        :param unicode unit:
            The new default unit.
        """

    def IsReadOnly(self):
        """
        Retrieves if the unit system is read-only or not.

        :rtype: bool
        :returns:
            True or False indicating the read-only property of the unit system.
        """

    def SetReadOnly(self, read_only):
        """
        Changes the read-only status of this unit system.

        :param bool read_only:
            Flag indicating if the unit system should be read-only.
        """

    def RemoveCategory(self, category):
        """
        Removes the given category from the categories map.

        :param unicode category:
            The category to remove
        """

    def __eq__(self, other):
        """
        :param UnitSystem other:
            The other unit system we want to check the equality.
        """

    def __ne__(self, other):
        """
        :param UnitSystem other:
            The other unit system we want to check the differences.
        """
