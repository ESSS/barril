from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from coilib50.units import ObtainQuantity
from coilib50.units.temperature import (
    GetDeltaTemperatureQuantity, GetDeltaUnitForTemperatureUnit, GetTemperatureQuantity,
    GetTemperatureUnitForDeltaUnit, IsDeltaTemperatureQuantity, IsTemperatureQuantity)


@pytest.mark.parametrize('unit_pair', [('K', 'ddegK'), ('degC', 'ddegC'), ('degF', 'ddegF'), ('degR', 'ddegR')])
def testTemperatureQuantities(unit_pair):
    '''
    Test the free functions that convert between 'delta temperature' and 'thermodynamic temperature'.
    '''
    temperature_unit, delta_unit = unit_pair

    # Check the unit correspondence.
    assert GetDeltaUnitForTemperatureUnit(temperature_unit) == delta_unit
    assert GetTemperatureUnitForDeltaUnit(delta_unit) == temperature_unit

    temperature_quant = ObtainQuantity(temperature_unit, 'thermodynamic temperature')
    delta_quant = ObtainQuantity(delta_unit, 'delta temperature')

    # Check the functions that identify the quantities.
    assert IsTemperatureQuantity(temperature_quant)
    assert IsDeltaTemperatureQuantity(delta_quant)
    assert not IsTemperatureQuantity(delta_quant)
    assert not IsDeltaTemperatureQuantity(temperature_quant)

    # Check the quantities conversions.
    assert GetDeltaTemperatureQuantity(temperature_quant) == delta_quant
    assert GetTemperatureQuantity(delta_quant) == temperature_quant


def testTemperatureQuantitiesWrongType():
    '''
    Test that GetDeltaQuantity() and GetTemperatureQuantity() correctly raise ValueErrors when given
    quantities that are not temperatures.
    '''
    wrong = ObtainQuantity('m', 'length')

    with pytest.raises(ValueError):
        GetDeltaTemperatureQuantity(wrong)

    with pytest.raises(ValueError):
        GetTemperatureQuantity(wrong)
