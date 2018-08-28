from __future__ import absolute_import, division, unicode_literals

from coilib50.units import Scalar
from coilib50.units.unit_system import UnitSystem
from coilib50.units.unit_system_manager import UnitSystemManager


def testGetFormattedValue(unit_system_manager):
    scalar1 = Scalar('length', 10, 'm')
    assert scalar1.GetUnitSystemFormatted() == '10 [m]'

    # Check that squared works
    scalar2 = scalar1 * scalar1

    assert scalar2.GetUnitSystemFormatted() == '100 [m2]'

    units_mapping = {'length' : 'km', 'viscosity' : 'cP'}

    unit_system_manager = UnitSystemManager.GetSingleton()
    current = unit_system_manager.current = UnitSystem('system1', 'My System', units_mapping)
    assert current.GetDefaultUnit('length') == 'km'

    assert scalar2.GetUnitSystemFormatted() == '0.0001 [km2]'

    scalar3 = Scalar('pressure', 10, 'psi')
    scalar4 = scalar1 / scalar3
    assert scalar4.GetUnitSystemFormatted() == "1 [m/psi]"
