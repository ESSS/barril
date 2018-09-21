# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from barril import units
from barril.units import ObtainQuantity
from barril.units.posc import (
    CreateAreaQuantityFromLengthQuantity, CreateVolumeQuantityFromLengthQuantity)
from barril.units.unit_database import UnitDatabase

from pytest import approx

def testPoscFrequency(unit_database_posc):
    u1 = units.Scalar('frequency', 1, 'Hz')
    assert u1.GetValue('GHz') == 1.0E-9

    u1 = units.Scalar('frequency', 1, 'GHz')
    assert u1.GetValue('Hz') == 1E9


def testPoscTime(unit_database_posc):
    '''
        These are the time-units available on posc.
    '''
    units.Scalar('time', 100, 's')
    units.Scalar('time', 100, 'min')
    hs = units.Scalar('time', 24, 'h')
    d = units.Scalar('time', 1, 'd')
    units.Scalar('time', 100, 'wk')

    assert hs.GetValue('d') == d.GetValue('d')

def testPoscTemperature(unit_database_posc):
    u1 = units.Scalar('thermodynamic temperature', 100, 'degC')
    u2 = units.Scalar('thermodynamic temperature', 100, 'degF')
    u3 = units.Scalar('thermodynamic temperature', 0, 'degC')
    u4 = units.Scalar('thermodynamic temperature', 0, 'degC')
    u5 = units.Scalar('thermodynamic temperature', 235, 'degF')
    u6 = units.Scalar('thermodynamic temperature', 64, 'degC')
    assert u1.GetQuantityType() == u2.GetQuantityType()
    assert 'temperature' == u2.GetQuantityType()
    assert u1.unit != u2.unit
    assert u3 == u4
    # u1.unit = 'K'  # from C to K
    assert approx(abs(u1.GetValue('K')-373.15), 7) == 0
    # u2.unit = 'K'  # from F to K
    assert approx(abs(u2.GetValue('K')-310.927777777), 7) == 0
    # u3.unit = 'degF'  # from C to F
    assert u3.GetValue('degF') == 32.0
    # C to F, F to C
    assert approx(abs(u5.GetValue('degC')-112.7777777777), 7) == 0
    assert approx(abs(u6.GetValue('degF')-147.2), 7) == 0
    # now return u3.unit from F to C and compare u3.value with u4.value
    # sanity-check
    assert u3.GetValue('degC') == u4.value

def testPoscRankine(unit_database_posc):
    rankine = [0.0, 100, 550, 1300]
    kelvin = [0.0, 55.55555, 305.55555, 722.22222]
    unit_database = unit_database_posc

    obtained = unit_database.Convert('thermodynamic temperature', 'degR', 'K', rankine)
    assert approx(obtained) == kelvin

def testPoscLength(unit_database_posc):
    # 'length'
    u1 = units.Scalar('length', 10, 'ft')
    u2 = units.Scalar('length', 100, 'km')
    u3 = units.Scalar('length', 15, 'yd')
    u4 = units.Scalar('length', 15, 'yd')
    assert u1.GetQuantityType() == u2.GetQuantityType()
    assert u1.unit != u2.unit
    assert u3 == u4
    # u1.unit = 'm'  # from feet to metres
    assert approx(abs(u1.GetValue('m')-3.048), 7) == 0
    # u2.unit = 'm'  # from kilometres to metres
    assert approx(abs(u2.GetValue('m')-100000.0), 7) == 0
    # u3.unit = 'ft'  # from yd to ft
    assert approx(abs(u3.GetValue('ft')-45.0), 7) == 0
    # now return u3.unit from feet to yards and compare u3.value with u4.value
    # sanity-check
    assert u3.GetValue('yd') == u4.value

def testPoscVolume(unit_database_posc):
    million_cubic_meters = units.Scalar('volume', 1, 'M(m3)')
    assert million_cubic_meters.value == 1.0
    assert million_cubic_meters.GetValue('m3') == 1.0e6
    assert million_cubic_meters.GetValue('1000m3') == 1.0e3

    cubic_meters = units.Scalar('volume', 1.0e6, 'm3')
    assert cubic_meters.value == 1.0e6
    assert cubic_meters.GetValue('M(m3)') == 1.0
    assert cubic_meters.GetValue('1000m3') == 1.0e3

def testPoscVolumeFlowRate(unit_database_posc):
    million_cubic_meters = units.Scalar('volume flow rate', 1, 'M(m3)/d')
    assert million_cubic_meters.value == 1.0
    assert million_cubic_meters.GetValue('m3/d') == 1.0e6
    assert million_cubic_meters.GetValue('1000m3/d') == 1.0e3

    cubic_meters = units.Scalar('volume flow rate', 1.0e6, 'm3/d')
    assert cubic_meters.value == 1.0e6
    assert cubic_meters.GetValue('M(m3)/d') == 1.0
    assert cubic_meters.GetValue('1000m3/d') == 1.0e3

def testPoscPermeabilityLength(unit_database_posc):
    unit_database = UnitDatabase.GetSingleton()
    assert 'volume' == unit_database.GetQuantityType('mD.ft')
    assert 'permeability length' == unit_database.GetDefaultCategory('mD.ft')

def testPoscPermeability(unit_database_posc):
    # 'length'
    u1 = units.Scalar('permeability rock', 1, 'D')
    u2 = units.Scalar('permeability rock', 1000, 'mD')
    assert u1.GetQuantityType() == u2.GetQuantityType()
    assert u1.unit != u2.unit
    # u1.unit = 'mD'  # from darcy to milidarcy
    # u2.unit = 'D'  # from milidarcy to darcy

    assert approx(abs(u1.GetValue('mD')-1000.0), 7) == 0
    assert approx(abs(u2.GetValue('D')-1.0), 7) == 0

def testPoscMolePerTime(unit_database_posc):
    default = units.Scalar(1, 'mol/s')
    assert default.GetQuantityType() == 'mole per time'

    assert approx(abs(default.value-1.0), 7) == 0
    assert approx(abs(default.GetValue('kmol/d')-1.0 * 86400.0 / 1000.0), 7) == 0
    assert approx(abs(default.GetValue('mol/d')-1.0 * 86400.0), 7) == 0

def testPoscRotationalFrequency(unit_database_posc):
    default = units.Scalar(1, 'rad/s')
    assert default.GetQuantityType() == 'frequency'

    assert approx(abs(default.value-1.0), 7) == 0
    assert approx(abs(default.GetValue('dega/s')-57.29578778556937), 7) == 0
    assert approx(abs(default.GetValue('rev/s')-0.15915494309644432), 7) == 0

def testPoscAngularAcceleration(unit_database_posc):
    default = units.Scalar(1, 'rad/s2')
    assert default.GetQuantityType() == 'angular acceleration'

    assert approx(abs(default.value-1.0), 7) == 0
    assert approx(abs(default.GetValue('dega/s2')-57.29578778556937), 7) == 0
    assert approx(abs(default.GetValue('dega/min2')-(1.0 * 3600.0) * 57.29578778556937), 7) == 0

    assert approx(abs(default.GetValue('rev/s2')-0.15915494309644432), 7) == 0
    assert approx(abs(default.GetValue('rev/min2')-0.15915494309644432 * 3600.0), 7) == 0
    assert approx(abs(default.GetValue('rpm/s')-9.549296585786658), 7) == 0

def testPoscDensity(unit_database_posc):
    default = units.Scalar(1, 'kg/m3')
    assert default.GetQuantityType() == 'density'

    assert approx(abs(default.value-1.0), 7) == 0
    assert approx(abs(default.GetValue('mg/m3')-1e6), 7) == 0
    assert approx(abs(default.GetValue('mg/cm3')-1e6 / 1e6), 7) == 0

def testPoscSpecificEnergy(unit_database_posc):
    default = units.Scalar(1, 'J/kg')
    assert default.GetQuantityType() == 'specific energy'

    assert approx(abs(default.value-1.0), 7) == 0
    assert approx(abs(default.GetValue('J/g')-1.0 / 1e3), 7) == 0
    assert approx(abs(default.GetValue('kW.h/kg')-2.7777777777777776e-07), 7) == 0
    assert approx(abs(default.GetValue('kW.h/t')-2.7777777777777776e-07 * 1e3), 7) == 0

    assert approx(abs(default.GetValue('kW.h/tonUS')-3.06197599869e-10), 20) == 0
    assert approx(abs(default.GetValue('kW.h/tonUK')-2.73390677574e-10), 20) == 0

def testPoscMassPerEnergy(unit_database_posc):
    default = units.Scalar(1, 'kg/J')
    assert default.GetQuantityType() == 'mass per energy'

    assert approx(abs(default.value-1.0), 7) == 0
    assert approx(abs(default.GetValue('lbm/Btu')-1.0 / 0.0004299226139295), 7) == 0

def testCreateVolumeQuantityFromLengthQuantity(unit_database_posc):
    unit_database = unit_database_posc
    length_units = unit_database.GetValidUnits('length')
    convertable_length_units = ['m', 'cm', 'dm', 'ft', 'in', 'km', 'mi', 'mm', 'yd', 'um']

    for length_unit in length_units:
        length_quantity = ObtainQuantity(length_unit, 'length')
        volume_quantity = CreateVolumeQuantityFromLengthQuantity(length_quantity)

        if length_unit in convertable_length_units:
            expected_volume_category = 'volume'

        else:
            expected_volume_category = '(length) ** 3'

        assert volume_quantity.GetCategory() == expected_volume_category
        assert volume_quantity.GetUnit() == '%s3' % length_unit

def testCreateAreaQuantityFromLengthQuantity(unit_database_posc):
    unit_database = unit_database_posc
    length_units = unit_database.GetValidUnits('length')
    convertable_length_units = ['m', 'cm', 'ft', 'in', 'km', 'mi', 'miUS', 'mm', 'um', 'yd']

    for length_unit in length_units:
        length_quantity = ObtainQuantity(length_unit, 'length')
        area_quantity = CreateAreaQuantityFromLengthQuantity(length_quantity)

        if length_unit in convertable_length_units:
            expected_volume_category = 'area'

        else:
            expected_volume_category = '(length) ** 2'

        assert area_quantity.GetCategory() == expected_volume_category
        assert area_quantity.GetUnit() == '%s2' % length_unit

def testDefaultCategories(unit_database_posc):
    '''
    Check all units with categories defined
    '''
    unit_database = unit_database_posc
    categories = set()
    for unit in unit_database.GetUnits():
        category = unit_database.GetDefaultCategory(unit)
        assert category is not None, 'All units MUST have a default category.'
        quantity_type = unit_database.GetQuantityType(unit)

        if category != quantity_type:
            categories.add(category)

    assert sorted(categories) == \
        [
            'amount of substance',
            'angle per time',
            'area per volume',
            'concentration',
            'delta temperature',
            'dynamic viscosity',
            'energy length per area',
            'energy length per time area temperature',
            'energy per area',
            'energy per length',
            'fluid gas concentration',
            'force length per length',
            'force per force',
            'heat flow rate',
            'index',
            'length per volume',
            'linear thermal expansion',
            'luminous exitance',
            'mass concentration',
            'mass per length',
            'mobility',
            'mole per mole',
            'multiplier',
            'operations per time',
            'permeability length',
            'permeability rock',
            'pressure squared per (dynamic viscosity)',
            'relative power',
            'relative time',
            'self inductance per length',
            'shear rate',
            'status',
            'thermodynamic temperature',
            'volume per area',
            'volume per length',
            'volume per time per area',
            'volume per time per volume',
            'volume per volume',
        ]

def testPoscValidUnitsNotRepeated(unit_database_posc):
    unit_database = unit_database_posc
    for category in unit_database.IterCategories():
        valid_units = unit_database.GetValidUnits(category)
        assert len(valid_units) == len(set(valid_units)), \
            'There is a duplicate unit defined in "%s": %s' % (category, valid_units,)

def testPoscKVmm(unit_database_posc):
    '''
    V/m to KV/mm (multiply by 1e6)
    '''
    q = ObtainQuantity('V/m')
    assert q.ConvertScalarValue(1, 'KV/mm') == 1e6

def testPoscBytes(unit_database_posc):
    '''
    Bytes, kBytes, MBytes, ....
    '''
    q = ObtainQuantity('Byte')
    assert q.ConvertScalarValue(1024, 'kByte') == 1
    assert q.ConvertScalarValue(1024 * 1024, 'MByte') == 1
    assert q.ConvertScalarValue(1024 * 1024 * 1024, 'GByte') == 1
    assert q.ConvertScalarValue(1024 * 1024 * 1024 * 1024, 'TByte') == 1

def testOhmUnits(unit_database_posc):
    q = ObtainQuantity('ohm/m')
    assert q.ConvertScalarValue(1, 'ohm/km') == 1000

def testPower(unit_database_posc):
    unit_database = unit_database_posc
    assert 'volt ampere' == ObtainQuantity('VA').GetQuantityType()
    assert 'volt ampere reactive' == ObtainQuantity('VAr').GetQuantityType()

    assert unit_database.Convert(u'force', 'N', 'kN', 56.) == 0.056
    assert approx(abs(unit_database.Convert(
        u'force', [(u'N', 2)], [(u'kN', 2)], -(56. * 56))--(0.056 * 0.056)), 7) == 0

def testFluidGasConcentration(unit_database_posc):
    '''
    Total Gas Unit requested for PWDA as concentration
    '''
    q = ObtainQuantity('tgu')

    assert 'dimensionless' == q.GetQuantityType()

    assert approx(abs(q.ConvertScalarValue(1, 'ppm')-333.33), 7) == 0
    assert approx(abs(q.ConvertScalarValue(1, '%')-0.033333), 7) == 0
    assert approx(abs(q.ConvertScalarValue(1, 'Euc')-0.00033333), 7) == 0

