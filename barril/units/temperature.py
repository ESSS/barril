from __future__ import absolute_import, division, print_function, unicode_literals

'''
temperature.py: Specialized functions to deal with temperature units/quantities.

The main motivation for this module is the special handling of unit conversions for variations
of temperature: A variation of 10 degrees Celsius is equal to a variation of 10 Kelvin (and not
283 K). In most cases this doesn't matter, but the category 'delta temperature' exists to perform
the correct conversion for variations.
'''

# The categories that have special handling for unit conversions in some cases.
TEMPERATURE_CATEGORY = 'thermodynamic temperature'
DELTA_TEMPERATURE_CATEGORY = 'delta temperature'

# Dicts to match units between the two categories.
_TEMPERATURE_TO_DELTA = {
    'K': 'ddegK',
    'degC': 'ddegC',
    'degF': 'ddegF',
    'degR': 'ddegR',
    }

_DELTA_TO_TEMPERATURE = {
    'ddegK': 'K',
    'ddegC': 'degC',
    'ddegF': 'degF',
    'ddegR': 'degR',
    }


def IsTemperatureQuantity(quantity):
    '''
    Whether `quantity` has the 'thermodynamic temperature' category.

    :param IQuantity quantity:
    :rtype: bool
    '''
    return quantity.GetCategory() == TEMPERATURE_CATEGORY


def IsDeltaTemperatureQuantity(quantity):
    '''
    Whether `quantity` has the 'delta temperature' category.

    :param IQuantity quantity:
    :rtype: bool
    '''
    return quantity.GetCategory() == DELTA_TEMPERATURE_CATEGORY


def GetDeltaUnitForTemperatureUnit(temperature_unit):
    '''
    Get the 'delta temperature' unit that corresponds to the given 'thermodynamic temperature' unit.
    For instance, 'degF' will return 'ddegF' (delta F).

    :param six.text_type temperature_unit:
    :rtype: six.text_type
    '''
    return _TEMPERATURE_TO_DELTA[temperature_unit]


def GetTemperatureUnitForDeltaUnit(delta_unit):
    '''
    Get the 'thermodynamic temperature' unit that corresponds to the given 'delta temperature' unit.
    For instance, 'ddegF' will return 'degF'.

    :param six.text_type delta_unit:
    :rtype: six.text_type
    '''
    return _DELTA_TO_TEMPERATURE[delta_unit]


def GetDeltaTemperatureQuantity(temperature_quantity):
    '''
    Get the 'delta temperature' quantity with an appropriate unit to correspond to the passed
    temperature quantity.

    The 'delta temperature' quantity type exists to represent variations in temperature, because
    the unit conversions when dealing with variations in temperature is different. For example,
    a value of 10 K corresponds to -263 C, but a variation of temperature of 10 K corresponds to a
    variation of 10 C (and not of -263 C).

    :param IQuantity temperature_quantity:
    :rtype: IQuantity
    '''
    from coilib50.units import ObtainQuantity

    if not IsTemperatureQuantity(temperature_quantity):
        raise ValueError('Input quantity is not temperature: {}'.format(temperature_quantity))

    new_unit = GetDeltaUnitForTemperatureUnit(temperature_quantity.GetUnit())
    return ObtainQuantity(new_unit, DELTA_TEMPERATURE_CATEGORY)


def GetTemperatureQuantity(delta_quantity):
    '''
    Get the temperature quantity with an appropriate unit to correspond to the passed 'delta
    temperature' quantity.

    See `GetDeltaTemperatureQuantity()` for the motivation.

    :param IQuantity delta_quantity:
    :rtype: IQuantity
    '''
    from coilib50.units import ObtainQuantity

    if not IsDeltaTemperatureQuantity(delta_quantity):
        raise ValueError('Input quantity is not delta temperature: {}'.format(delta_quantity))

    new_unit = GetTemperatureUnitForDeltaUnit(delta_quantity.GetUnit())
    return ObtainQuantity(new_unit, TEMPERATURE_CATEGORY)
