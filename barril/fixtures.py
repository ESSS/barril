# coding: UTF-8
from __future__ import absolute_import, unicode_literals

import pytest

from barril import units

def CreateUnitDatabaseLenTime():
    '''
    :rtype: UnitDatabase
    :returns:
        Returns a unit database with length and time quantity types
    '''
    unit_database = units.UnitDatabase()
    unit_database.AddUnit('length', 'milimeters', 'mm', '%f * 1000.0', '%f / 1000.0')
    unit_database.AddUnit('length', 'centimeters', 'cm', '%f * 100.0', '%f / 100.0')
    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddUnit('length', 'kilometers', 'km', '%f / 1000.0', '%f * 1000.0')
    unit_database.AddUnitBase('time', 'seconds', 's')
    unit_database.AddUnit('time', 'minutes', 'minutes', '%f / 60.0', '%f * 60.0')

    unit_database.AddCategory(category='Table size', quantity_type='length', valid_units=['m', 'cm'], default_unit='m')
    unit_database.AddCategory(category='City size', quantity_type='length', valid_units=['km', 'm'], default_unit='km')
    unit_database.AddCategory(category='Time', quantity_type='time', default_unit='s')

    return unit_database

def CreateUnitDatabaseStartUnits():
    '''
    :rtype: UnitDatabase
    :returns:
        Returns a unit database with length and time quantity types
    '''
    unit_database = units.UnitDatabase()

    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddUnit('length', 'kilometers', 'km', '%f / 1000.0', '%f * 1000.0')
    unit_database.AddUnit('length', 'centimeters', 'cm', '%f * 100.0', '%f / 100.0')
    unit_database.AddCategory('length', 'length')

    return unit_database

def CreateUnitDatabaseWellLength():
    '''
    :rtype: UnitDatabase
    :returns:
        Returns a unit database with length and time quantity types
    '''
    unit_database = units.UnitDatabase()

    unit_database.AddUnit('length', 'milimeters', 'mm', '%f * 1000.0', '%f / 1000.0')
    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddUnit('length', 'centimeters', 'cm', '%f * 100.0', '%f / 100.0')
    unit_database.AddUnit('length', 'kilometers', 'km', '%f / 1000.0', '%f * 1000.0')
    unit_database.AddUnit('length', 'miles', 'mi', '%f / 1609.347', '%f * 1609.347')
    unit_database.AddUnit('length', 'inches', 'in', '%f / 0.0254', '%f * 0.0254')
    unit_database.AddUnit('length', 'micrometers', 'um', '%f * 1000000.0', '%f / 1000000.0')
    unit_database.AddCategory('length', 'length')
    unit_database.AddCategory('well-length', 'length')
    unit_database.AddCategory('well-length-with-min-and-max', 'length', min_value=0.0)
    
    return unit_database
    
def CreateUnitDatabasePoscLen(fill_categories=True):
    '''
    :rtype: UnitDatabase
    :returns:
        Returns a unit database with "length" quantity type only

    :param bool fill_categories:
        If a category "length" should also be created
    '''
    unit_database = units.UnitDatabase()
    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddUnit('length', 'kilometers', 'km', '%f / 1000.0', '%f * 1000.0')

    if fill_categories:
        unit_database.AddCategory(category='length', quantity_type='length')
    return unit_database


def CreateUnitDatabaseLenTemp():
    '''
    :rtype: UnitDatabase
    :returns:
        Returns a unit database with length and time quantity types
    '''
    unit_database = units.UnitDatabase()

    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddUnit('length', 'kilometers', 'km', '%f / 1000.0', '%f * 1000.0')
    unit_database.AddUnitBase('temperature', 'degC', 'degC')
    unit_database.AddUnit('temperature', 'Kelvin', 'K', '%f + 270', '%f - 270')  # not correct convertion on purpose (for testing only)
    
    unit_database.AddCategory('length', 'length')
    unit_database.AddCategory('temperature', 'temperature')

    return unit_database


def CreateUnitDatabaseLenPressure():
    '''
    :rtype: UnitDatabase
    :returns:
        Returns a unit database with length and time quantity types
    '''
    unit_database = units.UnitDatabase()

    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddUnit('length', 'kilometers', 'km', '%f / 1000.0', '%f * 1000.0')
    unit_database.AddUnitBase('pressure', 'pascal', 'Pa')
    unit_database.AddUnit('pressure', 'pounds/square inch', 'psi', '%f / 6894.757', '%f * 6894.757')
    
    unit_database.AddCategory('length', 'length')
    unit_database.AddCategory('pressure', 'pressure')

    return unit_database

def CreateUnitDatabaseCustomConversion():
    from barril.units import (UNKNOWN_QUANTITY_TYPE, UNKNOWN_UNIT)

    unit_database = units.UnitDatabase()
    # add some units for testing
    unit_database.AddUnit(UNKNOWN_QUANTITY_TYPE, UNKNOWN_UNIT, UNKNOWN_UNIT, '%f', '%f')
    unit_database.AddUnit('length', 'milimeters', 'mm', '%f * 1000.0', '%f / 1000.0')
    unit_database.AddUnitBase('length', 'meters', 'm')
    unit_database.AddUnit('length', 'centimeters', 'cm', '%f * 100.0', '%f / 100.0')
    unit_database.AddUnit('length', 'kilometers', 'km', '%f / 1000.0', '%f * 1000.0')
    unit_database.AddUnit('length', 'miles', 'mi', '%f / 1609.347', '%f * 1609.347')
    unit_database.AddUnit('length', 'inches', 'in', '%f / 0.0254', '%f * 0.0254')
    unit_database.AddUnit('length', 'micrometers', 'µm', '%f * 1000000.0', '%f / 1000000.0')
    unit_database.AddUnitBase('temperature', 'Celcius', 'ºC')
    unit_database.AddCategory('length', 'length', valid_units=['m', 'mm', 'cm', 'km'])

    def C_to_F(x):
        return x * 1.8 + 32

    def F_to_C(x):
        return (x - 32) / 1.8

    unit_database.AddUnit('temperature', 'Fahrenheit', 'F', C_to_F, F_to_C)

    def C_to_K(x):
        return x + 273.15

    def K_to_C(x):
        return x - 273.15

    unit_database.AddUnit('temperature', 'Kelvin', 'K', C_to_K, K_to_C)
    
    return unit_database


@pytest.yield_fixture
def unit_database():
    '''
    Fixture to be used whenever a test needs a clean UnitDatabase. When using this fixture, it's
    safe to call UnitDatabase.GetSingleton().
    '''
    from barril.units.unit_database import UnitDatabase
    yield UnitDatabase.PushSingleton()
    UnitDatabase.PopSingleton()


@pytest.yield_fixture
def unit_database_posc():
    '''
    Fixture to be used whenever a test needs a clean UnitDatabase. When using this fixture, it's
    safe to call UnitDatabase.GetSingleton().
    '''
    unit_database = units.UnitDatabase()
    unit_database.FillUnitDatabaseWithPosc(unit_database)
    units.UnitDatabase.PushSingleton(unit_database)

    yield unit_database

    units.UnitDatabase.PopSingleton()


@pytest.fixture
def unit_database_empty():
    database = units.UnitDatabase()
    units.UnitDatabase.PushSingleton(database)

    yield database

    units.UnitDatabase.PopSingleton()


@pytest.fixture
def unit_database_len():
    database = units.UnitDatabase()
    units.UnitDatabase.PushSingleton(database)
    database.AddUnitBase('length', 'meters', 'm')
    database.AddUnit('length', 'kilometers', 'km', '%f / 1000.0', '%f * 1000.0')
    database.AddUnitBase('temperature', 'degC', 'degC')
    database.AddUnitBase('flow rate', 'm3/s', 'm3/s')
    database.AddCategory('length', 'length')
    database.AddCategory('temperature', 'temperature')
    database.AddCategory('flow rate', 'flow rate', min_value=0.0)

    yield database

    units.UnitDatabase.PopSingleton()


@pytest.fixture
def unit_database_len_time():
    database = CreateUnitDatabaseLenTime()
    units.UnitDatabase.PushSingleton(database)

    yield database

    units.UnitDatabase.PopSingleton()

    
@pytest.fixture
def unit_database_start_units():
    database = CreateUnitDatabaseStartUnits()
    units.UnitDatabase.PushSingleton(database)

    yield database

    units.UnitDatabase.PopSingleton()


@pytest.fixture
def unit_database_well_length():
    database = CreateUnitDatabaseWellLength()
    units.UnitDatabase.PushSingleton(database)

    yield database

    units.UnitDatabase.PopSingleton()


@pytest.fixture
def unit_database_len_temp():
    database = CreateUnitDatabaseLenTemp()
    units.UnitDatabase.PushSingleton(database)

    yield database

    units.UnitDatabase.PopSingleton()


@pytest.fixture
def unit_database_len_pressure():
    database = CreateUnitDatabaseLenPressure()
    units.UnitDatabase.PushSingleton(database)

    yield database

    units.UnitDatabase.PopSingleton()


@pytest.fixture
def unit_database_custom_conversion():
    database = CreateUnitDatabaseCustomConversion()
    units.UnitDatabase.PushSingleton(database)

    yield database

    units.UnitDatabase.PopSingleton()

@pytest.fixture
def unit_database_posc_len_no_category():
    database = CreateUnitDatabasePoscLen(fill_categories=False)
    units.UnitDatabase.PushSingleton(database)

    yield database

    units.UnitDatabase.PopSingleton()


@pytest.fixture
def unit_database_posc_len():
    database = CreateUnitDatabasePoscLen(fill_categories=True)
    units.UnitDatabase.PushSingleton(database)

    yield database

    units.UnitDatabase.PopSingleton()

