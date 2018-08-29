# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import pytest
from pytest import approx

from barril import units

@pytest.fixture
def db():
    db = units.UnitDatabase.GetSingleton()
    yield db

def testTransmissibility(db):
    converted = db.Convert('transmissibility', 'cp.m3/day/bar', 'cp.bbl/day/psi', 1.0)
    assert approx(converted) == 0.433667315

def testIndex(db):
    category = db.GetCategoryInfo('index')
    db.CheckQuantityTypeUnit(category.quantity_type, '<ind>')

def testAdsorptionRate(db):
    db.CheckQuantityTypeUnit('adsorption rate', 'mg/kg/d')
    assert approx(db.Convert('adsorption rate', 'mg/kg/d', 'kg/kg/d', 1.0)) == 1.0e-6

def testSolubilityProduct(db):
    db.CheckQuantityTypeUnit('solubility product', '(mol/m3)^2')
    assert approx(db.Convert('solubility product', '(mol/L)^2', '(mol/m3)^2', 1.0)) == 1.0e6

def testMassConsumptionEfficiency(db):
    db.CheckQuantityTypeUnit('mass consumption efficiency', 'mg/l/mg/l')
    db.CheckQuantityTypeUnit('mass consumption efficiency', 'kg/m3/kg/m3')

def testDensityGeneration(db):
    db.CheckQuantityTypeUnit('density generation', 'mg/l/d')
    assert approx(db.Convert('density generation', 'mg/l/d', 'kg/m3/d', 1.0)) == 0.001

def testMolarDensity(db):
    db.CheckQuantityTypeUnit('amount of a substance', 'gmole/m3')
    db.CheckQuantityTypeUnit('concentration of B', 'gmole/m3')

def testPartsPerMillionByVolumeConcentration(db):
    assert approx(db.Convert('parts per million by volume per concentration', 'ppmv/mg/l', 'ppmv/kg/m3', 1.0)) == 1000

def testKPaPerSecond(db):
    assert approx(db.Convert('dynamic viscosity', 'Pa.s', 'kPa.s', 1000.0)) == 1

def testPartsPerMillionVolume(db):
    quantity_type = db.GetCategoryInfo('relative proportion').quantity_type
    db.CheckQuantityTypeUnit(quantity_type, 'ppmv')

def testPerTimeSquared(db):
    quantity_type = db.GetCategoryInfo('per time squared').quantity_type
    db.CheckQuantityTypeUnit(quantity_type, '1/d^2')

def testNoUnit(db):
    db.CheckQuantityTypeUnit('dimensionless', '-')

def testFluidConsistencyQuantityAndConversions(db):
    # Checking the quantity type.
    db.CheckQuantityType('fluid consistency')

    # Checking the units on quantity type.
    db.CheckQuantityTypeUnit('fluid consistency', 'Pa.s^n')
    db.CheckQuantityTypeUnit('fluid consistency', 'lbf.s^n/ft2')
    db.CheckQuantityTypeUnit('fluid consistency', 'eq.cp')

    # Let's do some conversions.
    def DoConversion(from_unit, to_unit, value):
        return db.Convert('fluid consistency', from_unit, to_unit, value)

    assert approx(DoConversion('Pa.s^n', 'lbf.s^n/ft2', 1.0)) == 0.02088543
    assert approx(DoConversion('Pa.s^n', 'lbf.s^n/ft2', 5.0)) == 0.10442717
    assert approx(DoConversion('Pa.s^n', 'lbf.s^n/ft2', 5.5)) == 0.11486989
    assert approx(DoConversion('Pa.s^n', 'lbf.s^n/ft2', 250.0)) == 5.221358447

    assert approx(DoConversion('Pa.s^n', 'lbf.s^n/100ft2', 1.0)) == 2.08854338
    assert approx(DoConversion('Pa.s^n', 'lbf.s^n/100ft2', 5.0)) == 10.44271689
    assert approx(DoConversion('Pa.s^n', 'lbf.s^n/100ft2', 5.5)) == 11.48698858
    assert approx(DoConversion('Pa.s^n', 'lbf.s^n/100ft2', 250.0)) == 522.1358447

    assert approx(DoConversion('Pa.s^n', 'eq.cp', 1.0)) == 994.5238095
    assert approx(DoConversion('Pa.s^n', 'eq.cp', 5.0)) == 4972.6190475
    assert approx(DoConversion('Pa.s^n', 'eq.cp', 5.5)) == 5469.8809522
    assert approx(DoConversion('Pa.s^n', 'eq.cp', 250.0)) == 248630.952375

    assert approx(DoConversion('lbf.s^n/ft2', 'Pa.s^n', 1.0)) == 47.88026
    assert approx(DoConversion('lbf.s^n/ft2', 'Pa.s^n', 5.0)) == 239.4013
    assert approx(DoConversion('lbf.s^n/ft2', 'Pa.s^n', 5.5)) == 263.34143
    assert approx(DoConversion('lbf.s^n/ft2', 'Pa.s^n', 250.0)) == 11970.065

    assert approx(DoConversion('lbf.s^n/ft2', 'lbf.s^n/100ft2', 1.0)) == 100
    assert approx(DoConversion('lbf.s^n/ft2', 'lbf.s^n/100ft2', 5.0)) == 500
    assert approx(DoConversion('lbf.s^n/ft2', 'lbf.s^n/100ft2', 5.5)) == 550
    assert approx(DoConversion('lbf.s^n/ft2', 'lbf.s^n/100ft2', 250.0)) == 25000

    assert approx(DoConversion('lbf.s^n/ft2', 'eq.cp', 1.0)) == 47618.058575050469

    assert approx(DoConversion('eq.cp', 'Pa.s^n', 1.0), abs=1e7) == 0.0010055
    assert approx(DoConversion('eq.cp', 'Pa.s^n', 5.0), abs=1e7) == 0.0050275
    assert approx(DoConversion('eq.cp', 'Pa.s^n', 5.5), abs=1e7) == 0.0055303
    assert approx(DoConversion('eq.cp', 'Pa.s^n', 250.0)) == 0.2513766

    assert approx(DoConversion('eq.cp', 'lbf.s^n/ft2', 1.0), abs=1e6) == 0.000021
    assert approx(DoConversion('eq.cp', 'lbf.s^n/ft2', 5.0), abs=1e6) == 0.000105
    assert approx(DoConversion('eq.cp', 'lbf.s^n/ft2', 5.5), abs=1e6) == 0.0001155
    assert approx(DoConversion('eq.cp', 'lbf.s^n/ft2', 250.0)) == 0.00525011

    assert approx(DoConversion('eq.cp', 'lbf.s^n/100ft2', 1.0), abs=1e7) == 0.0021
    assert approx(DoConversion('eq.cp', 'lbf.s^n/100ft2', 5.0)) == 0.01050021
    assert approx(DoConversion('eq.cp', 'lbf.s^n/100ft2', 5.5)) == 0.011550239
    assert approx(DoConversion('eq.cp', 'lbf.s^n/100ft2', 250.0)) == 0.5250109

def testBblPerMeters(db):
    assert approx(db.Convert('volume per length', 'bbl/ft', 'bbl/m', 1)) == 1 / 0.3048

def testConcentration(db):
    assert approx(db.Convert('concentration', 'g/L', 'mg/L', 1)) == 1000.0

def testVolumeFractionPerTemperature(db):
    expected_result = db.Convert('volumetric thermal expansion', '1/degC', '1/degF', 1)
    obtained_result = db.Convert('volume fraction per temperature', '(m3/m3)/degC', '(m3/m3)/degF', 1)
    assert approx(obtained_result) == expected_result

    expected_units = ['(m3/m3)/K', '(m3/m3)/degC', '(m3/m3)/degF']
    obtained_result = sorted(db.GetValidUnits('volume fraction per temperature'))
    assert obtained_result == expected_units

def testVolumePerWtpercent(db):
    ft3_wtpercent_to_m3_wtpercent = db.Convert('volume per wtpercent', 'ft3/wtpercent', 'm3/wtpercent', 25 / 1)
    m3_to_wtpercent_to_ft3_to_wtpercent = db.Convert('volume per wtpercent', 'm3/wtpercent', 'ft3/wtpercent', 0.70792125)

    assert approx(ft3_wtpercent_to_m3_wtpercent) == 0.70792125
    assert approx(m3_to_wtpercent_to_ft3_to_wtpercent) == 25

def testMassPerMol(db):
    gpermol_to_kgpermol = db.Convert('mass per mol', 'g/mol', 'kg/mol', 1000 / 1)
    kgpermol_to_gpermol = db.Convert('mass per mol', 'kg/mol', 'g/mol', 1)

    assert approx(gpermol_to_kgpermol, 1)
    assert approx(kgpermol_to_gpermol, 1000)
    assert approx(db.Convert('mass per mol', 'g/mol', 'lb/lbmole', 1)) == 1

def testInjectivityFactor(db):
    quantity_type = db.GetCategoryInfo('injectivity factor').quantity_type

    db.CheckQuantityType(quantity_type)
    db.CheckQuantityTypeUnit(quantity_type, 'm3/s.Pa')

    expected_units = ['m3/s.Pa', 'bbl/min.psi', '(m3/d)/(kgf/cm2)']

    assert db.GetValidUnits('injectivity factor') == expected_units

    converted_value = db.Convert('injectivity factor', 'bbl/min.psi', 'm3/s.Pa', 1)
    assert approx(converted_value) == 0.002649 / 6894.757  #  (from bbl/min to m3/s) / (from psi to Pa)

    converted_value = db.Convert('injectivity factor', '(m3/d)/(kgf/cm2)', 'm3/s.Pa', 1)
    assert approx(converted_value) == 1.1802270983e-10

def testTemperaturePerLengthdegCP30m():
    u1 = units.Scalar('temperature per length', 1.0, 'K/m')
    u2 = units.Scalar('temperature per length', 30.0, 'degC/30m')

    assert approx(u1.GetValue('degC/30m')) == 30.0
    assert approx(u2.GetValue('K/m')) == 1.0

def testMassPerTimePerArea(db):
    secs_to_days = 60 * 60 * 24
    assert approx(db.Convert('mass per time per area', 'kg/m2.s', 'kg/m2.d', 1)) == 1 * secs_to_days

def testAccelerationLinearMetersPerMin2(db):
    assert approx(db.Convert('acceleration linear', 'm/s2', 'm/min2', 2)) == 7200
    assert approx(db.Convert('acceleration linear', 'm/min2', 'm/s2', 10800)) == 3

def testAccelerationLinearFeetPerMin2(db):
    assert approx(db.Convert('acceleration linear', 'ft/s2', 'ft/min2', 2)) == 7200
    assert approx(db.Convert('acceleration linear', 'ft/min2', 'ft/s2', 10800)) == 3

def testMassConcentration(db):
    assert approx(db.Convert('mass concentration', 'Euc', 'g/g', 2)) == 2
    assert approx(db.Convert('mass concentration', 'Euc', 'g/100g', 2)) == 200
    assert approx(db.Convert('mass concentration', 'Euc', 'lbm/lbm', 2)) == 2

def testSpecificVolume(db):
    assert approx(db.Convert('specific volume', 'm3/kg', 'l/mg', 1.0)) == 0.001

def testViscosityPerPressure(db):
    assert approx(
        db.Convert('viscosity per pressure', 'cP/kPa', 'cP/psi', 10.0)) == 68.9475729

    assert approx(
        db.Convert('viscosity per pressure', 'cP/kPa', 'cP/(kgf/cm2)', 10.0)) == 980.665

    assert approx(
        db.Convert('viscosity per pressure', 'cP/(kgf/cm2)', 'cP/psi', 0.102), abs=1e7) == 0.0071713

    # maybe it's from this wrong conversion where IMEX limit of 0.102 comes from:
    assert approx(
        db.Convert('viscosity per pressure', 'cP/(kgf/cm2)', 'cP/kPa', 10.0)) == 0.1019716

def testForcePerLength(db):
    assert approx(db.Convert('force per length', 'N/m', 'kgf/m', 1.0)) == 0.101971621

def testMiligramPerGram(db):
    assert approx(db.Convert('mass concentration', 'mg/g', 'g/g', 2.0)) == 0.002

def testGramsPerBarrel(db):
    db.CheckQuantityTypeUnit('concentration', 'g/bbl')

def testSiemens(db):
    assert approx(db.Convert('conductivity', 'S/m', 'uS/m', 1.0)) == 1000000.0

def testStrokeFrequency(db):
    db.CheckQuantityTypeUnit('stroke frequency', 'spm')
    assert approx(db.Convert('stroke frequency', 'spm', 'sps', 150.0)) == 2.5

def testPowerPerWeight(db):
    db.CheckQuantityTypeUnit('power per mass', 'W/kg')
    db.CheckQuantityTypeUnit('power per weight', 'W/kg')

    assert approx(db.Convert('power per weight', 'W/kg', 'kW/kg', 1.0)) == 1.0 / 1000.0
    assert approx(db.Convert('power per weight', 'kW/kg', 'W/kg', 1.0)) == 1000.0

def testSelfInductance(db):
    assert approx(db.Convert(
        'self inductance per length', 'H/m', 'H/km', 1.0), rel=0.01) == 1000

    assert approx(db.Convert(
        'self inductance per length', 'H/m', 'mH/km', 1.0), rel=0.01) == 1000000

    assert approx(db.Convert(
        'self inductance per length', 'H/m', 'uH/km', 1.0), rel=0.01) == 1000000000

    assert approx(db.Convert(
        'self inductance per length', 'H/m', 'nH/km', 1.0), rel=0.01) == 1000000000000

    assert approx(db.Convert(
        'self inductance per length', 'H/m', 'mH/m', 1.0), rel=0.01) == 1000

    assert approx(db.Convert(
        'self inductance per length', 'H/m', 'uH/m', 1.0), rel=0.01) == 1000000

    assert approx(db.Convert(
        'self inductance per length', 'H/m', 'nH/m', 1.0), rel=0.01) == 1000000000

def testConcentrationPerSquareTime(db):
    db.CheckQuantityTypeUnit('concentration per square time', 'mg/l/d2')
    db.CheckQuantityTypeUnit('concentration per square time', 'kg/m3/d2')

    assert approx(db.Convert('concentration per square time', 'mg/l/d2', 'kg/m3/d2', 1.0)) == 1.0 / 1000.0
    assert approx(db.Convert('concentration per square time', 'kg/m3/d2', 'mg/l/d2', 1.0)) == 1000.0

def testVolumeInCubicMicrometres(db):
    obtained = db.Convert('volume', 'm3', 'um3', 1.0)
    expected = 1e18
    assert approx(obtained, rel=1e-12) == expected

def testVolumeFlowRateInCubicMicrometresPerSecond(db):
    obtained = db.Convert('volume flow rate', 'm3/s', 'um3/s', 1.0)
    expected = 1e18
    assert approx(obtained, rel=1e-12) == expected

def testFlowCoefficient(db):
    obtained = db.Convert('flow coefficient', '(galUS/min)/(psi^0.5)', '(m3/s)/(Pa^0.5)', 1.0)
    expected = 7.59805421208337e-07
    assert approx(obtained, rel=1e-12) == expected

    obtained = db.Convert('flow coefficient', '(m3/h)/(bar^0.5)', '(m3/s)/(Pa^0.5)' , 1.0)
    expected = 8.784104611578831e-07
    assert approx(obtained, rel=1e-12) == expected

def testHertzPerSecond():
    from barril.units import Scalar
    assert approx(Scalar(1, 'rpm').GetValue('Hz')) == 1 / 60.
    assert approx(Scalar(1, 'Hz').GetValue('rpm')) == 60.
    assert approx(Scalar(1, 'Hz/s').GetValue('rpm/s')) == 60.
    assert approx(Scalar(1, 'rpm/s').GetValue('Hz/s')) == 1 / 60.

def testFluidGasConcentration():
    from barril.units import Scalar
    assert approx(Scalar(1, 'tgu').GetValue('ppm')) == 333.33
    assert approx(Scalar(1, 'tgu').GetValue('%')) == 0.033333

