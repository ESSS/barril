from __future__ import absolute_import, division, unicode_literals

import attr
import copy
import math
import traceback

import six
from six.moves import zip  # @UnresolvedImport

from barril._foundation.singleton import Singleton
from barril._foundation.types_ import CheckType

# Contains the registry for all the avaiable unit types.
__all__ = [
    "UnitsError",
    "InvalidQuantityTypeError",
    "InvalidUnitError",
    "UnitDatabase",
    "InvalidOperationError",
]


#===================================================================================================
# UnitsError
#===================================================================================================
class UnitsError(RuntimeError):
    '''
    Base class for errors related to units.
    '''


#===================================================================================================
# InvalidQuantityTypeError
#===================================================================================================
class InvalidQuantityTypeError(UnitsError):
    '''
    Error raised when an invalid quantity type is found
    '''

    def __init__(self, quantity_type, available=None):
        msg = 'Invalid quantity_type: %s' % (quantity_type,)
        if available is not None:
            msg += '\nAvailable:\n%s' % available
        UnitsError.__init__(self, msg)


#===================================================================================================
# InvalidUnitError
#===================================================================================================
class InvalidUnitError(UnitsError):
    '''
    Error raised when an invalid unit is found
    '''

    def __init__(self, unit, quantity_type=None, category=None, valid_units=None):
        if quantity_type is not None:
            msg = 'Invalid unit for quantity_type %s: %s' % (quantity_type, unit)

        elif category is not None:
            msg = 'Invalid unit for category %s: %s' % (category, unit)

        else:
            msg = 'Invalid unit:%s' % (unit,)

        if valid_units is not None:
            msg += ' [Valid Units: %s]' % valid_units

        UnitsError.__init__(self, msg)


#===================================================================================================
# InvalidOperationError
#===================================================================================================
class InvalidOperationError(UnitsError):
    '''
    Error raised when some operation but couldn't actually be performed with the given units.
    E.g.: Summing meters + seconds is not valid (while meters + centimeters would be)
    '''


#===================================================================================================
# ComposedUnitException
#===================================================================================================
class ComposedUnitError(UnitsError):
    '''
    Error raised when a composed unit conversion is performed
    E.g.: Velocity_Array * Concentration_Array = m/s.g/cm3
    '''


#===================================================================================================
# UnitInfo
#===================================================================================================
class UnitInfo(object):
    '''
    Holds information about a unit type
    '''

    ADD_STR_INFO_TO_UNIT_INFO = False

    def __init__(self, quantity_type, name, unit, frombase, tobase, default_category=None):
        '''
        :param unicode name:
            Name of the unit (e.g.: meter, millimiter).

        :param unicode unit:
            String that represents the unit (symbol - e.g.: m, mm).

        :type frombase: callable or unicode
        :param frombase:
            the formula to convert from the base to this unit.

        :param  tobase:
            The formula to convert from the this unit to the base.

        .. note:: frombase or tobase must be defined having the part that should be transformed as
            a %f, %s or just x
        '''

        def MakeLambda(s):
            s = s.replace('%s', 'x').replace('%f', 'x')
            assert 'x' in s
            s.replace('x', 'float(x)')
            ret = eval('lambda x:%s' % s)
            ret.__has_conversion__ = True
            return ret

        if isinstance(frombase, six.text_type):
            frombase_func = MakeLambda(frombase)
        else:
            frombase_func = frombase

        if isinstance(tobase, six.text_type):
            tobase_func = MakeLambda(tobase)
        else:
            tobase_func = tobase

        # The functions added to the UnitInfo must say whether they actually have some
        # conversion. If they do, and it's value is True, they may also have
        # __a__, __b__, __c__, __d__ identifying the posc convertions
        # (used for doing conversions for sci20 grid functions in C++)
        # If it's False, that means that the function will have no actual conversion.

        # If not identified, that means that they do have conversions associated
        if not hasattr(tobase_func, '__has_conversion__'):
            tobase_func.__has_conversion__ = True

        if not hasattr(frombase_func, '__has_conversion__'):
            frombase_func.__has_conversion__ = True

        self.name = name
        self.unit = unit
        self.frombase = frombase_func
        self.tobase = tobase_func
        self.quantity_type = quantity_type
        self.default_category = default_category

        if UnitInfo.ADD_STR_INFO_TO_UNIT_INFO:
            # must be added for the generation of the c++ version of the conversion
            self.frombase_str = frombase
            self.tobase_str = tobase

    def __hash__(self):
        return hash(self.unit)

    def __eq__(self, other):
        return self.unit == other.unit

    def __ne__(self, other):
        return not self == other


#===================================================================================================
# CategoryInfo
#===================================================================================================
@attr.s
class CategoryInfo(object):
    '''
    Holds information about a category
    '''
    category = attr.ib(default='')
    quantity_type = attr.ib(default='')
    valid_units = attr.ib(factory=list)
    valid_units_set = attr.ib(factory=set)
    default_unit = attr.ib(default='')
    default_value = attr.ib(default=0.0)
    min_value = attr.ib(default=None)
    max_value = attr.ib(default=None)
    is_min_exclusive = attr.ib(default=False)
    is_max_exclusive = attr.ib(default=False)
    caption = attr.ib(default='')


#===================================================================================================
# UnitDatabase
#===================================================================================================
class UnitDatabase(Singleton):
    '''
    Registry with all the available quantity types and units that represent the physical units.

    Quantity Types represent the type of the unit, for instance length or temperature, as strings.
    Every quantity type has one or more units associated with it.

    Units represent one specific unit inside a quantity_type, for instance meters and centimeters
    for length.
    '''

    PREPOSITIONS_IN_CATEGORY_NAME = ['per', 'of']

    @classmethod
    def CreateDefaultSingleton(cls):
        result = cls(default_singleton=True)
        cls.FillUnitDatabaseWithPosc(result)
        return result

    # Some aliases to some quantity types
    _ADDITIONAL_CATEGORY_ALIASES = {
        'liquid volume flow rate' : 'volume flow rate',
        'gas volume flow rate' : 'volume flow rate',
        'liquid volume' : 'volume',
        'gas volume' : 'volume',
        'liquid volume per standard volume' : 'volume per standard volume',
        'gas volume per standard volume' : 'volume per standard volume',
        'date' : 'time',
    }

    @classmethod
    def FillUnitDatabaseWithPosc(cls, unit_database, fill_categories=True):
        '''
        Fills a unit database with the posc values.

        :param UnitDatabase unit_database:
            The unit database to be filled.

        :param bool fill_categories:
            Indicates whether for each quantity type a category with the same name should be created.

        :rtype: UnitDatabase
        :returns:
            The unit database passed as a parameter.
        '''
        from .posc import FillUnitDatabaseWithPosc

        unit_database.Clear()
        FillUnitDatabaseWithPosc(unit_database, fill_categories=fill_categories, override_categories=True)

        if fill_categories:
            for quantity_alias, quantity_type in six.iteritems(cls._ADDITIONAL_CATEGORY_ALIASES):
                unit_database.AddCategory(quantity_alias, quantity_type)

        return unit_database

    def CheckValueForCategory(self, category, value, unit=None):
        '''
        :param unicode category:
            The category to be checked.

        :param float value:
            The value to be checked for the given category.

        :param unicode unit:
            The unit of the value passed (if not available, the default value is considered).
        '''
        from ._quantity import ObtainQuantity
        quantity = ObtainQuantity(unit, category)
        quantity.CheckValue(value)

    def CheckDefaultUnitDatabase(self):
        '''
        Checks if this is the default unit-database. If it's not a 'default' unit-database, an
        error is raised together with the stack trace from where it was originally created.

        :raises AssertionError:
            raises error if this was not created as the default unit database.
        '''
        if hasattr(self, '_database_created_from'):
            raise AssertionError('Not default unit-database. Creation: \n-------\n%s\n-------\n' % (
                self._database_created_from,))

    # Additional conversions stored at the class (no point in storing them only in an instance,
    # even if it's a singleton). This is done because if a new database is created (say to support just
    # some specific units) it would be painfull to have to register all conversion functions manually.
    # This way we have a singleton that have the application units, other databases can be created
    # but all databases share the same conversion functions.
    #
    # dict of class supported -> conversion function
    # see RegisterAdditionalConversionType
    _additional_conversions = {}

    def __init__(self, default_singleton=False):
        '''
        Initializes the unit manager without any quantity types.

        :param bool default_singleton:
            If True, this is the unit database that's created through the CreateDefaultSingleton
            method. This is needed because any constants created a module or class level must have a
            reference to the default unit-database and not for some other database created in tests
            (so, this flag is used together with CheckDefaultUnitDatabase later on).
        '''
        if not default_singleton:
            # If this is not the default singleton, mark from where was it created if we need
            # to check later on.
            if six.PY2:
                # unfortunately functions from 'traceback' WILL mix bytes and unicode, so we have
                # to use the more permissive StringIO module from PY2
                from cStringIO import StringIO
            else:
                from io import StringIO
            s = StringIO()
            traceback.print_stack(file=s)
            self._database_created_from = s.getvalue()

        # Quantities must be cached accordingly to the current unit-database.
        self.quantities_cache = {}

        # Dictionary to cache whether a unit is valid in a category.
        # dict(tuple(unicode, unicode) -> bool)
        # dict(tuple(category, unit) -> is_valid)
        self._category_unit_valid = {}

        # dict of quantity_type => list of UnitInfo (the first unit in this list is the base unit for
        # the given quantity type)
        self.quantity_types = {}

        # dict of unit name => UnitInfo
        self.unit_to_unit_info = {}
        self.categories_to_quantity_types = {}

    #----------------------------------------------- The interfaces below all work with the category

    @classmethod
    def FillSimple(cls, unit_database):
        unit_database.AddUnitBase('length', 'meters', 'm')
        unit_database.AddUnit('length', 'milimeters', 'mm', '%f * 1000.0', '%f / 1000.0')
        unit_database.AddUnit('length', 'centimeters', 'cm', '%f * 100.0', '%f / 100.0')
        unit_database.AddUnit('length', 'kilometers', 'km', '%f / 1000.0', '%f * 1000.0')

        unit_database.AddUnitBase('time', 'seconds', 's')
        unit_database.AddUnit('time', 'minutes', 'min', '%f * 60.0', ' %f * 60.0')
        unit_database.AddUnit('time', 'hours', 'h', '%f * 3600.0', ' %f * 3600.0')
        unit_database.AddUnit('time', 'days', 'd', '%f * 86400.0', ' %f * 86400.0')

        unit_database.AddCategory('length', 'length')
        unit_database.AddCategory('time', 'time')

    def AddCategory(
        self,
        category,
        quantity_type=None,
        valid_units=None,
        override=False,
        default_unit=None,
        default_value=None,
        min_value=None,
        max_value=None,
        is_min_exclusive=False,
        is_max_exclusive=False,
        caption='',
        from_category=None,
        ):
        '''Adds a category to the unit-management. If it already exists, throws an error
        if override is not set to True

        :param unicode category:
            The category to be added to the unit-management.

        :param unicode quantity_type:
            The quantity type that this category maps to.

        :param set(unicode) valid_units:
            A set of the valid units for the given category.

        :param bool override:
            Whether to replace the quantity type for the category.

        :param unicode default_unit:
            The default unit for the category

        :param float default_value:
            The default value for the category

        :param float min_value:
            Minimum value acceptable. If None, any value can be set.

        :param float max_value:
            Maximum value acceptable. If None, any value can be set.

        :param bool is_min_exclusive:
            If the min_value given is exclusive.

        :param bool is_max_exclusive:
            If the max_value given is exclusive.

        :param unicode caption:
            User friendly caption for this category.

        :param unicode from_category:
            Category to copy other parameters from.

        :raises UnitsError:
            If the category was already added and override is not set to True
        '''
        CheckType(category, six.text_type)

        if from_category and quantity_type:
            raise ValueError('cannot pass both quantity_type and from_category')

        if not override and category in self.categories_to_quantity_types:
            raise UnitsError('category %r already registered' % category)

        if min_value is not None and max_value is not None:
            if max_value < min_value:
                raise ValueError('min_value (%s) must be >= than min_value (%s)' % (min_value, max_value))

        if from_category:
            category_info = self.GetCategoryInfo(from_category)
            quantity_type = category_info.quantity_type
            if valid_units is None:
                valid_units = category_info.valid_units
            if default_unit is None:
                default_unit = category_info.default_unit
            if default_value is None:
                default_value = category_info.default_value
            if min_value is None:
                min_value = category_info.min_value
            if max_value is None:
                max_value = category_info.max_value
            if is_min_exclusive is None:
                is_min_exclusive = category_info.is_min_exclusive
            if is_max_exclusive is None:
                is_max_exclusive = category_info.is_max_exclusive
            if caption is None:
                caption = category_info.caption

        # check if valid_units should inherit from the quantity_type
        if valid_units is not None:
            # valid units given: check if all the given units are valid
            quantity_units = set(self.GetUnits(quantity_type))
            for unit in valid_units:
                if unit not in quantity_units:
                    msg = 'unit %r is not valid for quantity type %r.\nQuantity units: %r'
                    raise ValueError(msg % (unit, quantity_type, sorted(quantity_units)))

        # if (min_value is not None or max_value is not None) and default_unit is None:
        if default_unit is None:
            default_unit = self.GetBaseUnit(quantity_type)
            if valid_units and default_unit not in valid_units:
                default_unit = valid_units[0]
        else:
            quantity_units = set(self.GetUnits(quantity_type))
            if default_unit not in quantity_units:
                raise ValueError('unit %r is not valid for default quantity type %r' % (default_unit, quantity_type))

        # caption
        if not caption:
            caption = category.title()
            # Do not Title prepositions
            for word in self.PREPOSITIONS_IN_CATEGORY_NAME:
                caption = caption.replace(word.title() + ' ', word + ' ')

        # if the default_value has not been passed
        #   1) min_value defined? ---> min_value
        #   else
        #   2) max_value defined? ---> max_value
        #   else
        #   3) zero
        if default_value is None:
            if is_min_exclusive or is_max_exclusive:
                raise RuntimeError('default_value must be supplied')
            elif min_value is not None:
                default_value = min_value
            elif max_value is not None:
                default_value = max_value
            else:
                default_value = 0.0

        else:  # the default_value is defined

            msg = 'Error while adding category %s: default_value %f %s %f'

            if min_value is not None:
                if is_min_exclusive:
                    assert default_value > min_value, msg % (category, default_value, 'must be >', min_value)
                else:
                    assert default_value >= min_value, msg % (category, default_value, 'must be >=', min_value)

            if max_value is not None:
                if is_max_exclusive:
                    assert default_value < max_value, msg % (category, default_value, 'must be <', max_value)
                else:
                    assert default_value <= max_value, msg % (category, default_value, 'must be <=', max_value)

        valid_units_set = set()
        if valid_units is not None:
            valid_units_set = set(valid_units)

        info = CategoryInfo(
            category=category,
            quantity_type=quantity_type,
            valid_units=valid_units,
            valid_units_set=valid_units_set,
            default_unit=default_unit,
            default_value=default_value,
            min_value=min_value,
            max_value=max_value,
            is_min_exclusive=is_min_exclusive,
            is_max_exclusive=is_max_exclusive,
            caption=caption,
        )

        self.categories_to_quantity_types[category] = info
        return info

    def IsValidCategory(self, category):
        '''
        Check if the given category is valid into the unit database.

        :param unicode category:
            The category to check the validity.

        :rtype: bool
        :returns:
            True is it is a valid category; otherwise False.
        '''
        return category in self.categories_to_quantity_types

    def IterCategories(self):
        '''
        Iterator for all the categories.

        :rtype: iter(unicode)
        :returns:
            An iterator that'll provide all the categories.
        '''
        return six.iterkeys(self.categories_to_quantity_types)

    def GetCategoryInfo(self, category):
        '''
        :param unicode category:
            The category we're interested in.

        :rtype: CategoryInfo
        :returns:
            The category info for the category passed.
        '''
        try:
            return self.categories_to_quantity_types[category]
        except KeyError:
            categories_str = ''
            for cat in sorted(six.iterkeys(self.categories_to_quantity_types)):
                if cat is None:
                    cat = 'None'
                categories_str += (cat + '\n')
            raise InvalidQuantityTypeError('The category: "%s" is not added to the unit manager.\n'
                                           '--- Available ---:\n%s' % (category, categories_str))

    def GetCategoryQuantityType(self, category):
        '''
        :rtype: unicode
        :returns:
            The quantity type of some category.
        '''
        return self.GetCategoryInfo(category).quantity_type

    def FindUnitCase(self, category, unit):
        '''
        Given a unit in any case, returns a unit that is a match with the correct case within
        the unit-database.

        :param unicode category:
            The category for the given unit

        :param unicode unit:
            The unit that should be used to match the case.

        :rtype: unicode
        :returns:
            the unit considering the actual case used within the unit database.

        :raises AssertionError:
            if no unit could be found or more than one was found (there should be
            only 1 match considering it in a case-insensitive way).
        '''
        category_info = self.GetCategoryInfo(category)
        infos = self.GetInfos(category_info.quantity_type)

        matched = []

        unit_lower = unit.lower()
        for info in infos:
            if info.unit.lower() == unit_lower:
                matched.append(info.unit)

        if len(matched) == 1:
            return matched[0]
        else:
            raise AssertionError('Expected 1 match not considering case for: \'%s\'. Found: %s' %
                (unit, [u for u in matched]))

    def CheckCategoryUnit(self, category, unit):
        '''
        Check if the given category accepts the passed unit.

        :raises InvalidUnitError:
            if the unit provided is not accepted for this category
        '''
        assert category.__class__ == six.text_type, 'Expected unicode. Found: %s' % (category,)
        assert unit.__class__ == six.text_type, 'Expected unicode. Found: %s' % (unit,)

        key = (category, unit)
        try:
            # i.e.: if not valid (valid = self._category_unit_valid[key])
            if not self._category_unit_valid[key]:
                raise InvalidUnitError(unit, None, category)
        except KeyError:
            if category.__class__ != six.text_type:
                raise TypeError('Only unicode is accepted. %s is not.' % category.__class__)

            try:
                category_info = self.GetCategoryInfo(category)
                # When setting a unit, leave the user set any unit from the quantity type, even if there's
                # a subset for the category (the idea is that the units for the category are only used to
                # filter them in the UI, not really to do internal validations).
                self.CheckQuantityTypeUnit(category_info.quantity_type, unit)
                valid = True
            except UnitsError:
                valid = False

            self._category_unit_valid[key] = valid
            if not valid:
                raise InvalidUnitError(unit, None, category)

    def GetValidUnits(self, category):
        '''
        :rtype: list(unicode)
        :returns:
            The valid units for a given category. If the valid categories weren't given uses the valid units from
            quantity type.
        '''
        # Special case: the empty category, as generated by Quantity.CreateEmpty(), has no valid units.
        if category == '':
            return []

        category_info = self.GetCategoryInfo(category)
        if category_info.valid_units is not None:
            return category_info.valid_units
        else:
            if category_info.quantity_type != category:
                return self.GetValidUnits(category_info.quantity_type)

            # the valid units have not been specified for the given category (so, let's return
            # the units for the quantity type)
            return self.GetUnits(category_info.quantity_type)

    def GetDefaultValue(self, category):
        '''
        :rtype: float
        :returns:
            The default value for the given category.
        '''
        category_info = self.GetCategoryInfo(category)
        return category_info.default_value

    def GetDefaultUnit(self, category):
        '''
        :rtype: unicode
        :returns:
            The default unit for the given category.

        .. note:: This method shouldn't return None, when the default_unit isn't defined for the category
        the quantity type base unit is used.
        '''
        category_info = self.GetCategoryInfo(category)
        return category_info.default_unit

    #--------------------- The interfaces below all work with the quantity type and not the category

    def AddUnit(self, quantity_type, name, unit, frombase, tobase, default_category=None):
        '''
        Registers a new unit type.

        :param unicode quantity_type:
            The quantity type for the added unit.

        :param unicode name:
            A user-friendly name for this unit.

        :param unicode unit:
            The unit to be added.

        :type  frombase: string or callable
            If string, an expression to convert from the base unit of this quantity_type to this
            unit. If callable, must accept a float value that applies the conversion.

        :type  tobase: string or callable
            If a string, an expression to convert from this unit to the base unit. If callable, must
            accept a float value that applies the conversion.

        .. note:: Each expression must refer to %f or x as the current value of the unit.

        :param Union(unicode, None) default_category:
            The default category for the added unit (if any).
        '''
        assert quantity_type is not None
        if unit.__class__ != six.text_type:
            raise TypeError('Only unicode is accepted. %s is not.' % unit.__class__)

        if unit is None:
            unit = name
        info = UnitInfo(quantity_type, name, unit, frombase, tobase, default_category=default_category)
        if unit in self.unit_to_unit_info:
            raise RuntimeError(
                'Unit: %s already added to the unit database for the quantity type: %s (trying to add to: %s)' %
                (unit, self.unit_to_unit_info[unit].quantity_type, quantity_type,)
            )
        else:
            self.unit_to_unit_info[unit] = info
        quantity_type_list = self.quantity_types.setdefault(quantity_type, [])

        if unit in [q.unit for q in quantity_type_list]:
            raise RuntimeError('Unit already registered: %s (%s)') % (name, unit)

        quantity_type_list.append(info)

    def AddUnitBase(self, quantity_type, name, unit):
        '''
        Add a base unit type. Inside each quantity_type, there must be at least one Base unit.

        Parameters have the same meaning as in AddUnit().
        '''
        identity = lambda x : x
        identity.__has_conversion__ = False
        self.AddUnit(quantity_type, name, unit, identity, identity)
        # move the base info to the first position
        # (that's a convention: the base is always in the first position)
        infos = self.quantity_types[quantity_type]
        base = infos[-1]  # was appended to the end in Units.Add
        del infos[-1]
        infos.insert(0, base)

    def GetBaseUnit(self, quantity_type):
        '''
        :param unicode quantity_type:
            The quantity type for which we want a base unit.

        :rtype: unicode
        :returns:
            The base unit of the given quantity_type.

        :raises InvalidQuantityTypeError:
            if the quantity type is not valid
        '''
        try:
            infos = self.quantity_types[quantity_type]
            return infos[0].unit
        except KeyError:
            self.CheckQuantityType(quantity_type)

    def GetDefaultCategory(self, unit):
        '''
        :param unicode unit:
            The unit for which we want the category.

        :rtype: unicode or None
        :returns:
            The default category for the passed unit.
        '''
        try:
            unit_info = self.unit_to_unit_info[unit]
        except KeyError:
            return None
        else:
            category = unit_info.default_category
            if category:
                return category
            category = unit_info.quantity_type
            if category in self.categories_to_quantity_types:
                return category

    def GetQuantityType(self, unit):
        '''
        :rtype: unicode
        :returns:
            A quantity_type that contains the respective unit.
        '''
        try:
            return self.unit_to_unit_info[unit].quantity_type
        except KeyError:
            return None

    def FindSimilarUnitMatches(self, unit):
        '''
        This function will use heuristics to find similar units in the unit database to the
        passed unit.

        :param unicode unit:
            The unit which doesn't have a direct match in the unit dabatase.

        :rtype: list(unicode)
        :returns:
            Returns a list with possible matches for the passed unit, sorted.
        '''
        import re

        compiled = re.compile(r'[\./]')
        unit_split = compiled.split(unit.lower())

        close_match = []
        for existing_unit in six.iterkeys(self.unit_to_unit_info):
            existing_unit_split = compiled.split(existing_unit.lower())
            if len(existing_unit_split) == len(unit_split):
                for a, b in zip(existing_unit_split, unit_split):
                    if not a.startswith(b) and not b.startswith(a):
                        # Print left for debugging purposes.
                        # print 'skip', unit, '!=', existing_unit
                        break
                else:
                    close_match.append(existing_unit)

        return sorted(close_match)

    def GetQuantityTypes(self):
        '''
        :rtype: list(unicode)
        :returns:
            A list of the available categories, sorted.
        '''
        return sorted(six.iterkeys(self.quantity_types))

    def GetUnits(self, quantity_type=None):
        """
        @return: list(string)
            The units of that quantity_type (if quantity_type is given) otherwise, returns all
            available units.

        @raise InvalidQuantityTypeError:
        """
        return [x.unit for x in self.GetInfos(quantity_type)]

    def GetUnitName(self, quantity_type, unit):
        '''
        :rtype: unicode
        :returns:
            The user-friendly name for the given unit.
        '''
        info = self.GetInfo(quantity_type, unit)
        return info.name

    def GetUnitNames(self, quantity_type):
        '''
        :rtype: list(string)
        :returns:
            The user-friendly names for all the units in the given quantity_type.

        :raises InvalidQuantityTypeError:
        '''
        return [x.name for x in self.GetInfos(quantity_type)]

    def GetInfo(self, quantity_type, unit, fix_unknown=False):
        '''
        :param bool fix_unknown:
            If True won't raise error if quantity_type is unkwnown (and unit may be anything).
            Returns the unknown unit info in this situation.

        :rtype: UnitInfo
        :returns:
            The unit object registered with the given unit

        @raise InvalidQuantityTypeError
        @raise InvalidUnitError
        '''
        try:
            # Common case: unit matches the quantity type registered.
            unit_info = self.unit_to_unit_info[unit]
            if quantity_type == unit_info.quantity_type:
                return unit_info
        except KeyError:
            pass  # Just ignore and go through the 'uncommon' case.

        # First check if the quantity_type is a registered category
        try:
            category_info = self.categories_to_quantity_types[quantity_type]
        except KeyError:
            pass
        else:
            quantity_type = category_info.quantity_type

        try:
            quantity_types = self.quantity_types[quantity_type]
        except KeyError:
            raise InvalidQuantityTypeError(quantity_type, sorted(six.iterkeys(self.quantity_types)))
        else:
            for info in quantity_types:
                if info.unit == unit:
                    return info
            else:
                if fix_unknown:
                    # Before actually triggering the error, handle the unknown case:
                    # We can have an unknown quantity type with a 'known' unit (i.e.: the reader
                    # says it's unknwon, but we get a proper label for it in the UI, thus, it's a
                    # known 'unkwon' quantity). So, in this case, proceed returning the unknown
                    # quantity unit information.
                    from ._unit_constants import UNKNOWN_QUANTITY_TYPE, UNKNOWN_UNIT
                    if quantity_type == UNKNOWN_QUANTITY_TYPE:
                        quantity_types = self.quantity_types[quantity_type]
                        for info in quantity_types:
                            if info.unit == UNKNOWN_UNIT:
                                return info

                raise InvalidUnitError(
                    unit,
                    quantity_type,
                    valid_units=sorted([info.unit for info in quantity_types]))

    def GetInfos(self, quantity_type=None):
        '''
        :rtype: list(UnitInfo)
        :returns:
            All UnitInfos from that quantity_type (if quantity_type is given), otherwise return all
            UnitInfos.

        @raise InvalidQuantityTypeError
        '''
        if quantity_type is None:
            all_infos = []
            for infos in six.itervalues(self.quantity_types):
                all_infos.extend(infos)
            return all_infos
        else:
            try:
                return self.quantity_types[quantity_type]
            except KeyError:
                raise InvalidQuantityTypeError(quantity_type, '\n'.join(list(self.quantity_types.keys())))

    def CheckQuantityType(self, quantity_type):
        '''
        Checks if the quantity type is valid. If it is not, raise an InvalidQuantityTypeError.

        @raise InvalidQuantityTypeError
        @raise InvalidUnitError
        '''
        if quantity_type not in self.quantity_types:
            raise InvalidQuantityTypeError(quantity_type, '\n'.join(sorted(self.quantity_types)))

    def CheckQuantityTypeUnit(self, quantity_type, unit):
        '''
        Check if the given quantity type has the given unit.

        @raise InvalidUnitError
        '''
        self.GetInfo(quantity_type, unit)

    def _ConvertWithExp(self, quantity_type, from_unit, to_unit, value):
        '''
        Converts a value from one unit to another unit considering that the units from and
        to have exponents.

        :param unicode quantity_type:
            The quantity type that has the from and to units.

        :type from_unit: unicode or list(tuple(unicode, int))
        :param from_unit:
            The unit we're converting from or the string and exponent from the unit.

        :type to_unit: unicode or list(tuple(unicode, int))
        :param to_unit:
            The unit we're converting to or the string and exponent from the unit.

        :param float value:
            The value to be converted.

        :rtype: float
        :returns:
            Returns the converted value.
        '''
        len_to_unit = len(to_unit)
        len_from_unit = len(from_unit)

        if len_to_unit == 0 or len_from_unit == 0:
            return value

        if len_from_unit != 1:
            raise ComposedUnitError(
                'Can only convert one unit to another (not a composed unit at this point)')

        if len_to_unit != 1:
            raise ComposedUnitError(
                'Can only convert one unit to another (not a composed unit at this point)')

        from_unit, from_exp = from_unit[0]
        to_unit, to_exp = to_unit[0]

        if from_exp != to_exp:
            raise ValueError('Cannot convert among different exponents (%s) to (%s)' %
                ((from_unit, from_exp), (to_unit, to_exp)))

        if from_exp == to_exp == 1:
            # Special case handling
            return self.Convert(quantity_type, from_unit, to_unit, value)

        negative = False
        if value < 0.0:
            negative = True
            value = abs(value)

        value = math.pow(value, 1.0 / from_exp)  # Convert from the exponent
        value = self.Convert(quantity_type, from_unit, to_unit, value)
        ret = math.pow(value, to_exp)
        if negative:
            return -ret
        return ret

    @classmethod
    def RegisterAdditionalConversionType(cls, class_, func):
        '''
        This function may be used to register conversions for additional classes, not originally
        treated (e.g.: IGridFunction)

        :param type class_:
            This is the class that should be treated. So, when a conversion is requested,
            if a class is an instance of the class passed, it'll be used to do the conversions.

        :param callable func:
            The function that should do the conversion. It'll be called as
            func(unit_database, quantity_type, from_unit_info, to_unit_info, value)
        '''
        if class_ not in cls._additional_conversions:
            cls._additional_conversions[class_] = func
        else:
            assert cls._additional_conversions[class_] == func, \
                'The class %s already has a convertion function registered' % (six.text_type(class_))

    def Convert(self, category_or_quantity_type, from_unit, to_unit, value):
        '''
        Converts a value from one unit to another unit (given the quantity type that contains
        both units), so, note that the quantity type at this point is always the same (can't convert
        units with quantity types that don't match).

        :param unicode category_or_quantity_type:
            The category or quantity type for doing the conversion (if it's a category it's
            converted into the quantity type inside this method).

        :param unicode from_unit:
            A string determining the unit from the value we want to convert or a dict
            with the units with their given exponents to convert.

        :param unicode to_unit:
            A string determining the unit to which the value should be converted or a dict with the
            units with their given exponents to convert.

        :param object value:
            The object that should be converted.

        .. note:: that from_unit and to_unit must only have 1 key if they are a dict pointing to
            exponents.

        :rtype: object
        :returns:
            The converted value
        '''
        supported_types = tuple(self._additional_conversions)
        if isinstance(value, supported_types):
            for key, convert_function in six.iteritems(self._additional_conversions):
                if isinstance(value, key):
                    break  # keep convert_function for later use
            else:
                assert False
        else:
            convert_function = None
        # operations with exponents...
        from_is_list = from_unit.__class__ in (list, tuple)
        to_is_list = to_unit.__class__ in (list, tuple)

        if from_is_list or to_is_list:
            if not from_is_list:
                from_unit = ((from_unit, 1))
            if not to_is_list:
                to_unit = ((to_unit, 1))

            # same unit: no conversion needed
            if from_unit == to_unit:
                return value

            if category_or_quantity_type.__class__ in (list, tuple) and len(category_or_quantity_type) == 1:
                category_or_quantity_type = category_or_quantity_type[0]
            return self._ConvertWithExp(category_or_quantity_type, from_unit, to_unit, value)

        # same unit: no conversion needed
        if from_unit == to_unit:
            return value

        # simple operations (same exponent)
        try:
            quantity_type = self.categories_to_quantity_types[
                category_or_quantity_type].quantity_type
        except KeyError:
            self.CheckQuantityType(category_or_quantity_type)
            quantity_type = category_or_quantity_type

        if convert_function is not None:
            return convert_function(self, quantity_type, from_unit, to_unit, value)

        this = self.GetInfo(quantity_type, from_unit, fix_unknown=True)
        other = self.GetInfo(quantity_type, to_unit, fix_unknown=True)

        if isinstance(value, (float,) + six.integer_types):  # , numpy.ndarray)):
            return other.frombase(this.tobase(value))
        else:  # list / tuple
            frombase = other.frombase
            tobase = this.tobase
            class_ = list
            if isinstance(value, tuple):
                class_ = tuple

            return class_(frombase(tobase(v)) for v in value)

    def Clear(self):
        '''
        Removes all the quantity types registered.
        '''
        self.quantity_types.clear()
        self.categories_to_quantity_types.clear()
        self.unit_to_unit_info.clear()
        self.quantities_cache.clear()
        self._category_unit_valid.clear()

    # Operations with different quantities ---------------------------------------------------------
    def _DoOperationWithSameQuantity(self, quantity1, quantity2, value1, value2, operation):
        '''
        Given 2 quantities, do an operation that DOES NOT accept the creation of a new composed
        quantity (e.g.: sum, subtraction)
        '''
        if quantity1 == quantity2:
            return quantity1, operation(value1, value2)

        else:
            # otherwise, we must transform the units in the quantity1 to their counterparts
            # in the quantity2 (without changing anything in the categories at this time)
            category_to_unit_and_exp1 = copy.deepcopy(quantity1.GetCategoryToUnitAndExps())
            category_to_unit_and_exp2 = copy.deepcopy(quantity2.GetCategoryToUnitAndExps())

            category_to_unit_and_exp1, category_to_unit_and_exp2, value1, value2 = \
                self._MatchQuantities(category_to_unit_and_exp1, category_to_unit_and_exp2, value1, value2)

            # at this point the quantity types and units must be the same (the categories may actually
            # be different)
            quantity1 = quantity1.CreateCopyInstance(category_to_unit_and_exp1)
            quantity2 = quantity2.CreateCopyInstance(category_to_unit_and_exp2)

            composing_units1 = set(quantity1.GetComposingUnitsJoiningExponents())
            composing_units2 = set(quantity2.GetComposingUnitsJoiningExponents())
            if composing_units1 != composing_units2:
                if len(composing_units1) == 0:
                    # no unit in the 1st part (just take the 2nd as the correct one)
                    quantity1 = quantity2

                elif len(composing_units2) == 0:
                    pass  # ok, no units in the second part...

                else:
                    raise InvalidOperationError("Error. Can't do operation because units don't match: (%s != %s)" %
                        (composing_units1, composing_units2))

            return quantity1, operation(value1, value2)

    def Sum(self, quantity1, quantity2, value1, value2):
        return self._DoOperationWithSameQuantity(quantity1, quantity2, value1, value2,
            lambda a, b: a + b)

    def Subtract(self, quantity1, quantity2, value1, value2):
        return self._DoOperationWithSameQuantity(quantity1, quantity2, value1, value2,
            lambda a, b: a - b)

    def Divide(self, quantity1, quantity2, value1, value2):
        return self._DoOperationResultingInNewQuantity(quantity1, quantity2, value1, value2,
            lambda a, b: a - b, lambda a, b: a / b)

    def Multiply(self, quantity1, quantity2, value1, value2):
        '''
        Multiplication with different quantities.

        Rationale:
            - the multiplication of different quantities can result in a derived quantity type.
            - the quantities / values should be transformed if there are quantity types that are
            equal in bot quantities (e.g.: if there's cm in the quantity1 and m in the quantity2,
            the value1 and the quantity1 must be converted to m before proceeding with the
            actual multiplication)
            - note that if a given quantity type has different units in the quantity1 or in
            the quantity2, they must 1st be converted to have the same unit in a given quantity type.
            - after the quantities are compatible, it's just a matter of creating a join of
            the available units and summing the expoents to create the resulting quantity
            (and multiplying the actual values).

        :type quantity1: IQuantity (related to value1)
        :param quantity1:
        :type quantity2: IQuantity (related to value2)
        :param quantity2:
        :type value1: iterable or number
        :param value1:
        :type value2: iterable or number
        :param value2:
        :rtype: tuple(IQuantity, value)
        '''
        return self._DoOperationResultingInNewQuantity(quantity1, quantity2, value1, value2,
            lambda a, b: a + b, lambda a, b: a * b)

    def _MatchQuantities(self, category_to_unit_and_exp1, category_to_unit_and_exp2, value1, value2):
        '''
        Matches all the units for a given quantity type (so, if a unit 'm' is found, if
        a 'cm' is later found, convert it to 'm' -- as well as it's composing value).

        :rtype: the dicts passed with the quantity types matched to the same units and the corresponding
        values converted to match those changes.
        '''
        quantity_types_found_to_used_unit = {}

        # 1st thing is putting the same unit for a given quantity type (both sides)
        for c in (category_to_unit_and_exp1, category_to_unit_and_exp2):
            for category, unit_exp in list(c.items()):
                unit, _exp = unit_exp
                quantity_type = self.GetCategoryQuantityType(category)
                used_unit_for_quantity_type = quantity_types_found_to_used_unit.get(quantity_type)
                if used_unit_for_quantity_type is None:
                    quantity_types_found_to_used_unit[quantity_type] = unit
                else:
                    # don't worry about the exponent at this time, just update the unit and the related value.
                    if c is category_to_unit_and_exp1:
                        value1 = self.Convert(quantity_type, unit, used_unit_for_quantity_type, value1)
                    else:
                        value2 = self.Convert(quantity_type, unit, used_unit_for_quantity_type, value2)
                    unit_exp[0] = used_unit_for_quantity_type
        return category_to_unit_and_exp1, category_to_unit_and_exp2, value1, value2

    def _DoOperationResultingInNewQuantity(self, quantity1, quantity2, value1, value2, operation_exp, operation):
        '''
        Given 2 quantities, do an operation that accepts the creation of a new quantity that is
        composed of the quantities passed (e.g.: division, multiplication).
        '''
        from ._quantity import Quantity

        # otherwise, we must transform the units in the quantity1 to their counterparts
        # in the quantity2 (without changing anything in the categories at this time)
        category_to_unit_and_exp1 = quantity1.GetCategoryToUnitAndExpsCopy()
        category_to_unit_and_exp2 = quantity2.GetCategoryToUnitAndExpsCopy()

        category_to_unit_and_exp1, category_to_unit_and_exp2, value1, value2 = \
            self._MatchQuantities(category_to_unit_and_exp1, category_to_unit_and_exp2, value1, value2)

        # add the categories to the resulting one
        for category2, (unit2, exp2) in list(category_to_unit_and_exp2.items()):
            if category2 not in category_to_unit_and_exp1:
                exp1 = 0
                category_to_unit_and_exp1[category2] = [unit2, operation_exp(exp1, exp2)]
            else:
                unit_exp1 = category_to_unit_and_exp1[category2]
                unit1, exp1 = unit_exp1
                if unit1 == unit2:
                    unit_exp1[1] = operation_exp(exp1, exp2)
                else:
                    raise RuntimeError("This should've been covered already (%s != %s)." % (unit1, unit2))

        # unit -> expoent
        only_units_expoents = {}
        for c, (unit, exp) in list(category_to_unit_and_exp1.items()):
            existing = only_units_expoents.get(unit, 0)
            only_units_expoents[unit] = existing + exp

        # remove the ones that have exponent = 0
        for c, (unit, exp) in list(category_to_unit_and_exp1.items()):
            if exp == 0 or only_units_expoents[unit] == 0:
                # that's ok, it's been removed from the expression...
                del category_to_unit_and_exp1[c]

        result = Quantity.CreateDerived(category_to_unit_and_exp1)
        return result, operation(value1, value2)


#===================================================================================================
# RegisterConversion
#===================================================================================================
class RegisterConversion(object):

    _registered = False

    @classmethod
    def RegisterNumpyConversion(cls):
        '''
        Register a special unit conversion for numpy arrays.

        :param UnitDatabase db:
            The unit-database instance to register the conversion into.
        '''
        import numpy

        def ConvertNumpyArray(db, quantity_type, from_unit, to_unit, array):
            '''
            Converts the given numpy array by applying the conversion as if it was a scalar,
            since arrays support the numeric operators, which are applied element-wise.
            '''
            from_unit_info = db.GetInfo(quantity_type, from_unit, fix_unknown=True)
            to_unit_info = db.GetInfo(quantity_type, to_unit, fix_unknown=True)

            to_base = from_unit_info.tobase
            from_base = to_unit_info.frombase
            return from_base(to_base(array))

        UnitDatabase.RegisterAdditionalConversionType(numpy.ndarray, ConvertNumpyArray)


RegisterConversion.RegisterNumpyConversion()
