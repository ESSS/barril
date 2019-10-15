import weakref
from copy import deepcopy

from oop_ext.foundation import callback
from oop_ext.foundation.decorators import Override
from collections import OrderedDict
from oop_ext.foundation.singleton import Singleton
from oop_ext.interface import AssertImplements

from .unit_database import UnitDatabase
from .unit_system import UnitSystem
from .unit_system_interface import IUnitSystem


class NoTemplateError(RuntimeError):
    """
    Error raised when trying to create a new unit system and no template was defined.
    """

    def __init__(self):
        msg = "Error creating unit system. There is no template defined."
        RuntimeError.__init__(self, msg)


class InvalidTemplateError(RuntimeError):
    """
    Error raised when a template is set in a manager that has at least one unit system that does not
    match the given template
    """

    def __init__(self, invalid_unit_system_ids=None):
        """
        :param iterable(unicode) invalid_unit_system_ids:
            The ids of the unit system that do not match a given template
        """
        if invalid_unit_system_ids:
            msg = "The unit systems %s do not match the given template" % str(
                invalid_unit_system_ids
            )
        else:
            msg = "At least one of the current unit systems does not match the given template"
        RuntimeError.__init__(self, msg)


class UnitSystemCategoriesError(KeyError):
    """
    Error raised when the categories defined in a new unit system differ from those define in the
    template.
    """

    def __init__(self, default_categories, current_categories):
        msg = "Error creating new unit system. The default categories are %s but %s were defined."
        KeyError.__init__(self, msg % (default_categories, current_categories))


class UnitSystemIDError(KeyError):
    """
    Error raised when trying to create a new unit system given an already used ID.
    """

    def __init__(self, id):
        msg = "Error creating new unit system. The ID %s is already in use."
        KeyError.__init__(self, msg % (id))


class UnitSystemManager(Singleton):
    """
    A service that manages the unit systems. It handles the unit system objects creation and
    selection.

    :ivar list _object_refs:
        List of weakref for all objects which represents a value+unit.

    :type current: IUnitSystem instance
    :ivar current:
        The current unit system.

    :ivar Callback on_current:
        Callback called when the current unit system changes (the unit system is given as parameter).

    :ivar Callback on_unit_changed:
        Callback called when the the unit of a category changes (the category and unit is given as
        parameter).

    :type _unit_systems: dict(unicode, IUnitSystem instance)
    :ivar _unit_systems:
        A dict that holds the available unit systems.
    """

    def __init__(self):
        # list with valueable objects with a unit associated with
        self._object_refs = set()

        # someone would want to listen to changes in the current unit system
        self.on_current = callback.Callback()

        # someone would want to listen to changes in unit system categories unit.
        self.on_unit_changed = callback.Callback()

        # the current unit system which is being used by the application
        self._current = None

        # container for registered unit systems (strong references)
        self._unit_systems = OrderedDict()

        # unit system template.
        self._unit_system_template = None

        # default unit system class.
        self._default_unit_system_class = UnitSystem

        # This unit system is returned when no current unit system is selected
        self.__null_unit_system = UnitSystem(
            id=None, caption="Null", units_mapping={}, read_only=True
        )

    @Override(Singleton.ResetInstance)
    def ResetInstance(self):
        self.on_current.UnregisterAll()
        self.on_unit_changed.UnregisterAll()

    def SetDefaultUnitSystemClass(self, class_):
        """
        Set the default unit system class.

        :type class_: IUnitSystem class
        :param class_:
            The unit system class that wiil be used when creating new unit systems.
        """
        AssertImplements(class_, IUnitSystem)
        self._default_unit_system_class = class_

    def SetTemplateUnitSystemByUnitsMapping(self, units_mapping):
        """
        Set the unit system template based on the given units mapping.

        This template will be used to validate new unit systems.

        :type units_mapping: dict( unicode, unicode )
        :param units_mapping:
            A dict that maps each category to a related unit (which will be set as default).
            The valid categories are defined by the coilib50.units.UnitDatabase.

        @raise: TemplateDefinedAfterUnitSystemError
            See TemplateDefinedAfterUnitSystemError documentation.
        """
        template_categories = list(units_mapping.keys())
        invalid_unit_systems = []

        # Check if existing unit systems match the given template
        for unit_system in list(self._unit_systems.values()):
            current_units_mapping = unit_system.GetUnitsMapping()
            match = self._CheckUnitSystemMapping(current_units_mapping, template_categories)

            if not match:
                invalid_unit_systems.append(unit_system.GetId())

        if invalid_unit_systems:
            # At least one of the existing unit system is not valid for this template. Notify that
            # the template is invalid
            raise InvalidTemplateError(invalid_unit_systems)

        # NOTE: 'tr' for the caption (Unit system template) was removed.
        self._unit_system_template = self._default_unit_system_class(
            "template", "Unit system template", units_mapping, True
        )

    def GetUnitSystemTemplate(self):
        """
        :rtype: IUnitSystem instance
        :returns:
            Return the template unit system.
        """
        return self._unit_system_template

    def _CheckUnitSystemMapping(self, units_mapping, required_categories):
        """
        Checks if the given units mapping have a default unit for all required categories

        :type units_mapping: dict( unicode, unicode )
        :param units_mapping units_mapping:
            A dict that maps each category to a related unit. the dict should contain mapping for
            each category defined in the template.

        :param required_categoris list(unicode)
            The categories required in the given unit system.
        """
        required_categories_set = set(required_categories)

        current_categories = list(units_mapping.keys())
        current_categories = set(current_categories)

        return current_categories.issuperset(required_categories_set)

    def AddUnitSystem(self, id, caption, units_mapping=None, read_only=False):
        """
        Create a new unit system based on the given parameters.

        When creating a unit system it will be kept internally at the manager in a unit systems
        list and set as current right after the creation.

        It is expected that a unit system template is already set. The template will be used to
        validate the categories from the given units mapping.

        :param unicode id:
            The unique id of the unit system.

        :param unicode caption:
            The user-friendly name of the unit system.

        :type units_mapping: dict( unicode, unicode ) or None
        :param units_mapping:
            A dict that maps each category to a related unit (which will be set as default).
            The valid categories are defined by the coilib50.units.UnitDatabase.
            If None is given the units mapping from the template will be taken.

        :param bool read_only:
            Flag that sets the read-only state of the new unit system.

        :raises NoTemplateError:
            See NoTemplateError documentation.

        :raises UnitSystemIDError:
            See UnitSystemIDError documentation.

        :raises UnitSystemCategoriesError:
            See UnitSystemCategoriesError documentation.

        :rtype: IUnitSystem instance
        :returns:
            The created unit system.
        """
        if id in self._unit_systems:
            raise UnitSystemIDError(id)

        if self._unit_system_template is not None:
            template_units_mapping = self._unit_system_template.GetUnitsMapping()

            # If a unit map was passed we need to check it, otherwise just copy the template into
            # the new system
            if units_mapping is None:
                units_mapping = deepcopy(template_units_mapping)

            else:
                template_categories = list(template_units_mapping.keys())
                match = self._CheckUnitSystemMapping(units_mapping, template_categories)

                if not match:
                    raise UnitSystemCategoriesError(template_categories, list(units_mapping.keys()))

        else:
            # No template to check
            if units_mapping is None:
                # If not template was given, and not unit mapping was provided, let us create
                # an empty unit system.
                units_mapping = {}

        unit_system = self._default_unit_system_class(id, caption, units_mapping, read_only)
        self._unit_systems[id] = unit_system

        if self._current is None:
            self.SetCurrent(unit_system)

        return unit_system

    def _CategoryUnitChange(self, category, unit):
        """
        Triggers on_unit_changed callback when default unit change on a category in a unit system.

        :param unicode category:
            The changed category.

        :param unicode unit:
            The new unit.
        """
        self.on_unit_changed(category, unit)

    def RemoveUnitSystem(self, unit_system_id):
        """
        Remove the unit system with the given id.

        :param unicode unit_system_id:
            The id of the unit system to be removed.
        """
        del self._unit_systems[unit_system_id]

        # If the current unit system was removed, set another system as current
        if self._current.GetId() == unit_system_id:
            available = list(self.GetUnitSystems().values())

            if available:
                self.SetCurrent(available[0])
            else:
                self.SetCurrent(None)

    def GetUnitSystems(self):
        """
        :rtype: dict{unicode, IUnitSystem instance)
        :returns:
            The dict containing all the registered unit systems indexed by their ids.
        """
        return self._unit_systems

    # Current --------------------------------------------------------------------------------------

    def SetCurrent(self, unit_system):
        """
        Sets a new current unit system, updating all registered objects. If None, no object is changed.

        :type unit_system: IUnitSystem instance
        :param unit_system:
            The new current unit system.
        """
        if self._current is not None:
            self._current.on_default_unit.Unregister(self._CategoryUnitChange)

        self._current = unit_system

        if self._current is not None:
            self._current.on_default_unit.Register(self._CategoryUnitChange)
            self.on_current(unit_system)
        else:
            # Notifying that an empty unit system was set for the clients
            self.on_current(self.__null_unit_system)

        self.UpdateObjects()

    def GetCurrent(self):
        """
        Retrieves the unit system currently in use.

        :rtype: IUnitSystem instance
        :returns:
            The currently used unit system.
        """
        result = self._current

        if result is None:
            # If no system is set as current, we will return a null unit system just to keep the
            # interface (so that clients do not need to keep checking if the received system is null)
            result = self.__null_unit_system
        return result

    current = property(GetCurrent, SetCurrent)

    # Objects --------------------------------------------------------------------------------------

    def UpdateObjects(self):
        """
        Updates the units of all the registered objects. Also, remove dead objects from the list
        """
        current = self._current
        if current is not None:
            # remove dead references
            GetDefaultUnit = current.GetDefaultUnit
            for wrap in set(
                self._object_refs
            ):  # Note: iterate in a copy (just in case gc is triggered).
                obj = wrap.ref()
                if obj is not None:
                    # Update the object to match the current unit-system.
                    unit = GetDefaultUnit(obj.GetCategory())
                    if unit is not None:
                        obj.unit = unit

    class IdentityWrap:
        """
        Helper class to remove an object from the unit system references.

        It's used so that we create a wrapper that'll give the __hash__ and __eq__ based on
        the object id.
        """

        __slots__ = ["unit_system", "ref"]

        def __init__(self, obj, unit_system):
            """
            :param object obj:
                The object we'll be wrapping.

            :param UnitSystem unit_system:
                The unit system with the tracked object.
            """
            self.unit_system = unit_system
            self.ref = weakref.ref(obj, self._OnRefKilled)

        def _OnRefKilled(self, ref):
            """
            Called when a reference to an object with a unit is killed.

            :param weakref ref:
                The weak-ref that was killed
            """
            self.unit_system._object_refs.remove(self)

    def Register(self, obj):
        """
        Keeps a weak reference to the object in an internal list.
        Whatever change in the unit system will be propagated for all objects in the list.

        :param AbstractValueWithQuantityObject obj:
            An object which represents a value associated with a unit.

        .. note:: This code should in general only be called from the constructor of an object to be
        tracked and only once (although adding an object more than once won't give any errors, it'll
        incur in more overhead because the object will be added more than once to the internal list).
        """
        self._object_refs.add(self.IdentityWrap(obj, self))
        current = self._current
        if current is not None:
            # Update the object to match the current unit-system.
            unit = current.GetDefaultUnit(obj.GetCategory())
            if unit is not None:
                obj.unit = unit

    def GetUnitSystemById(self, id):
        """
        Returns the UnitSystem with the given id.

        :param unicode id:
            The wished unit system id.

        :rtype: IUnitSystem instance
        :returns:
            The unit system with the given id.

        :raises ValueError:
            If no unit system with that id was found.
        """
        if id in self._unit_systems:
            return self._unit_systems[id]
        else:
            raise ValueError("No UnitSystem with id %r found" % id)

    def GetNewId(self):
        """
        Returns an unit system id that is not being used.

        :rtype: unicode
        :returns:
            The available id.
        """
        ids = {id for id in self._unit_systems}
        count = 1
        new_id = "%s %d" % ("system", count)
        while new_id in ids:
            count += 1
            new_id = "%s %d" % ("system", count)
        return new_id

    def ConvertToCurrent(self, category, unit, value, unit_database=None):
        """
        Converts the given value from the given unit to the default unit of the current unit system.
        If there is no current unit system, no conversion is performed.

        :param unicode category:
            The unit's category.

        :param unicode unit:
            The source unit.

        :param float value:
            The value to convert.

        :param UnitDatabase unit_database:
            The unit database to perform the conversion. If not given, use the singleton.

        :rtype: (float, unicode)
        :returns:
            The pair (value, unit), containing the converted value and target unit. Note that
            if there is no current unit system, the returned value and unit are the same as
            the input.
        """
        if unit_database is None:
            unit_database = UnitDatabase.GetSingleton()

        current = self.current
        if current is None or current.GetDefaultUnit(category) is None:
            return (value, unit)

        to_unit = current.GetDefaultUnit(category)
        converted_value = unit_database.Convert(category, unit, to_unit, value)
        return converted_value, to_unit

    def GetCategoryDefaultUnit(self, category):
        """
        :param unicode category:
            The category to obtain the default unit

        :rtype: unicode or None
        :returns:
            The default unit to display the given category or None if there is no default unit set.
        """
        current_system = self.GetCurrent()

        result = None
        if current_system is not None:
            default_unit = current_system.GetDefaultUnit(category)

            if default_unit is not None:
                result = default_unit

        return result

    def GetQuantityDefaultUnit(self, quantity):
        """
        Get the default unit to use with a given quantity. If there is any map explictly defined for
        the quantity category, then that map will be used. Otherwise we will use the quantity default
        unit.

        :param IQuantity quantity:
            The quantity to obtain the default unit

        :return unicode
            The default unit to use with the given quantity
        """
        current_system = self.GetCurrent()

        # If no unit system was provided then let us use the quantity default unit
        result = quantity.GetUnit()

        if current_system is not None:
            default_unit = current_system.GetDefaultUnit(quantity.GetCategory())

            if default_unit is not None:
                result = default_unit

        return result

    def ConvertScalarToCurrent(self, scalar, unit_database=None):
        """
        Same as ConvertToCurrent but receives and returns a scalar instead of category, unit and value

        :param Scalar scalar:
            The scalar to be converted

        :param UnitDatabase unit_database:
            The unit database to perform the conversion. If not given, use the singleton.

        :rtype: Scalar
        :returns:
            A Scalar containing the converted value and target unit. Note that
            if there is no current unit system, the returned value and unit are the same as
            the input.
        """
        from barril.units import Scalar

        ret_tuple = self.ConvertToCurrent(
            scalar.GetCategory(), scalar.GetUnit(), scalar.GetValue(), unit_database
        )
        return Scalar(*ret_tuple)
