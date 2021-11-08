from pytest import approx

from barril import units
from barril.units import ObtainQuantity
from barril.units.posc import CreateAreaQuantityFromLengthQuantity
from barril.units.posc import CreateVolumeQuantityFromLengthQuantity
from barril.units.unit_database import UnitDatabase


def testPoscFrequency(unit_database_posc) -> None:
    u1 = units.Scalar("frequency", 1, "Hz")
    assert u1.GetValue("GHz") == 1.0e-9

    u1 = units.Scalar("frequency", 1, "GHz")
    assert u1.GetValue("Hz") == 1e9


def testPoscTime(unit_database_posc) -> None:
    """
    These are the time-units available on posc.
    """
    units.Scalar("time", 100, "s")
    units.Scalar("time", 100, "min")
    hs = units.Scalar("time", 24, "h")
    d = units.Scalar("time", 1, "d")
    units.Scalar("time", 100, "wk")

    assert hs.GetValue("d") == d.GetValue("d")


def testPoscTemperature(unit_database_posc) -> None:
    u1 = units.Scalar("thermodynamic temperature", 100, "degC")
    u2 = units.Scalar("thermodynamic temperature", 100, "degF")
    u3 = units.Scalar("thermodynamic temperature", 0, "degC")
    u4 = units.Scalar("thermodynamic temperature", 0, "degC")
    u5 = units.Scalar("thermodynamic temperature", 235, "degF")
    u6 = units.Scalar("thermodynamic temperature", 64, "degC")
    assert u1.GetQuantityType() == u2.GetQuantityType()
    assert "temperature" == u2.GetQuantityType()
    assert u1.unit != u2.unit
    assert u3 == u4
    # u1.unit = 'K'  # from C to K
    assert approx(abs(u1.GetValue("K") - 373.15), 7) == 0
    # u2.unit = 'K'  # from F to K
    assert approx(abs(u2.GetValue("K") - 310.927777777), 7) == 0
    # u3.unit = 'degF'  # from C to F
    assert u3.GetValue("degF") == 32.0
    # C to F, F to C
    assert approx(abs(u5.GetValue("degC") - 112.7777777777), 7) == 0
    assert approx(abs(u6.GetValue("degF") - 147.2), 7) == 0
    # now return u3.unit from F to C and compare u3.value with u4.value
    # sanity-check
    assert u3.GetValue("degC") == u4.value


def testPoscRankine(unit_database_posc) -> None:
    rankine = [0.0, 100, 550, 1300]
    kelvin = [0.0, 55.55555, 305.55555, 722.22222]
    unit_database = unit_database_posc

    obtained = unit_database.Convert("thermodynamic temperature", "degR", "K", rankine)
    assert approx(obtained) == kelvin


def testPoscLength(unit_database_posc) -> None:
    # 'length'
    u1 = units.Scalar("length", 10, "ft")
    u2 = units.Scalar("length", 100, "km")
    u3 = units.Scalar("length", 15, "yd")
    u4 = units.Scalar("length", 15, "yd")
    assert u1.GetQuantityType() == u2.GetQuantityType()
    assert u1.unit != u2.unit
    assert u3 == u4
    # u1.unit = 'm'  # from feet to metres
    assert approx(abs(u1.GetValue("m") - 3.048), 7) == 0
    # u2.unit = 'm'  # from kilometres to metres
    assert approx(abs(u2.GetValue("m") - 100000.0), 7) == 0
    # u3.unit = 'ft'  # from yd to ft
    assert approx(abs(u3.GetValue("ft") - 45.0), 7) == 0
    # now return u3.unit from feet to yards and compare u3.value with u4.value
    # sanity-check
    assert u3.GetValue("yd") == u4.value


def testPoscVolume(unit_database_posc) -> None:
    million_cubic_meters = units.Scalar("volume", 1, "M(m3)")
    assert million_cubic_meters.value == 1.0
    assert million_cubic_meters.GetValue("m3") == 1.0e6
    assert million_cubic_meters.GetValue("1000m3") == 1.0e3

    cubic_meters = units.Scalar("volume", 1.0e6, "m3")
    assert cubic_meters.value == 1.0e6
    assert cubic_meters.GetValue("M(m3)") == 1.0
    assert cubic_meters.GetValue("1000m3") == 1.0e3


def testPoscVolumeFlowRate(unit_database_posc) -> None:
    million_cubic_meters = units.Scalar("volume flow rate", 1, "M(m3)/d")
    assert million_cubic_meters.value == 1.0
    assert million_cubic_meters.GetValue("m3/d") == 1.0e6
    assert million_cubic_meters.GetValue("1000m3/d") == 1.0e3

    cubic_meters = units.Scalar("volume flow rate", 1.0e6, "m3/d")
    assert cubic_meters.value == 1.0e6
    assert cubic_meters.GetValue("M(m3)/d") == 1.0
    assert cubic_meters.GetValue("1000m3/d") == 1.0e3


def testPoscPermeabilityLength(unit_database_posc) -> None:
    unit_database = UnitDatabase.GetSingleton()
    assert "volume" == unit_database.GetQuantityType("mD.ft")
    assert "permeability length" == unit_database.GetDefaultCategory("mD.ft")


def testPoscPermeability(unit_database_posc) -> None:
    # 'length'
    u1 = units.Scalar("permeability rock", 1, "D")
    u2 = units.Scalar("permeability rock", 1000, "mD")
    assert u1.GetQuantityType() == u2.GetQuantityType()
    assert u1.unit != u2.unit
    # u1.unit = 'mD'  # from darcy to milidarcy
    # u2.unit = 'D'  # from milidarcy to darcy

    assert approx(abs(u1.GetValue("mD") - 1000.0), 7) == 0
    assert approx(abs(u2.GetValue("D") - 1.0), 7) == 0


def testPoscMolePerTime(unit_database_posc) -> None:
    default = units.Scalar(1, "mol/s")
    assert default.GetQuantityType() == "mole per time"

    assert approx(abs(default.value - 1.0), 7) == 0
    assert approx(abs(default.GetValue("kmol/d") - 1.0 * 86400.0 / 1000.0), 7) == 0
    assert approx(abs(default.GetValue("mol/d") - 1.0 * 86400.0), 7) == 0


def testPoscRotationalFrequency(unit_database_posc) -> None:
    default = units.Scalar(1, "rad/s")
    assert default.GetQuantityType() == "frequency"

    assert approx(abs(default.value - 1.0), 7) == 0
    assert approx(abs(default.GetValue("dega/s") - 57.29578778556937), 7) == 0
    assert approx(abs(default.GetValue("rev/s") - 0.15915494309644432), 7) == 0


def testPoscAngularAcceleration(unit_database_posc) -> None:
    default = units.Scalar(1, "rad/s2")
    assert default.GetQuantityType() == "angular acceleration"

    assert approx(abs(default.value - 1.0), 7) == 0
    assert approx(abs(default.GetValue("dega/s2") - 57.29578778556937), 7) == 0
    assert approx(abs(default.GetValue("dega/min2") - (1.0 * 3600.0) * 57.29578778556937), 7) == 0

    assert approx(abs(default.GetValue("rev/s2") - 0.15915494309644432), 7) == 0
    assert approx(abs(default.GetValue("rev/min2") - 0.15915494309644432 * 3600.0), 7) == 0
    assert approx(abs(default.GetValue("rpm/s") - 9.549296585786658), 7) == 0


def testPoscDensity(unit_database_posc) -> None:
    default = units.Scalar(1, "kg/m3")
    assert default.GetQuantityType() == "density"

    assert approx(abs(default.value - 1.0), 7) == 0
    assert approx(abs(default.GetValue("mg/m3") - 1e6), 7) == 0
    assert approx(abs(default.GetValue("mg/cm3") - 1e6 / 1e6), 7) == 0


def testPoscSpecificEnergy(unit_database_posc) -> None:
    default = units.Scalar(1, "J/kg")
    assert default.GetQuantityType() == "specific energy"

    assert approx(abs(default.value - 1.0), 7) == 0
    assert approx(abs(default.GetValue("J/g") - 1.0 / 1e3), 7) == 0
    assert approx(abs(default.GetValue("kW.h/kg") - 2.7777777777777776e-07), 7) == 0
    assert approx(abs(default.GetValue("kW.h/t") - 2.7777777777777776e-07 * 1e3), 7) == 0

    assert approx(abs(default.GetValue("kW.h/tonUS") - 3.06197599869e-10), 20) == 0
    assert approx(abs(default.GetValue("kW.h/tonUK") - 2.73390677574e-10), 20) == 0


def testPoscMassPerEnergy(unit_database_posc) -> None:
    default = units.Scalar(1, "kg/J")
    assert default.GetQuantityType() == "mass per energy"

    assert approx(abs(default.value - 1.0), 7) == 0
    assert approx(abs(default.GetValue("lbm/Btu") - 1.0 / 0.0004299226139295), 7) == 0


def testKinematicViscosity(unit_database_posc) -> None:
    default = units.Scalar("kinematic viscosity", 1, "m2/s")
    assert default.GetQuantityType() == "volume per time per length"
    assert approx(abs(default.value - 1.0), 7) == 0
    assert approx(abs(default.GetValue("cm2/s") - 10000.0), 7) == 0
    assert approx(abs(default.GetValue("St") - 10000.0), 7) == 0
    assert approx(abs(default.GetValue("cSt") - 1000000.0), 7) == 0
    assert approx(abs(default.GetValue("ft2/h") - 318750.077500155), 7) == 0
    assert approx(abs(default.GetValue("ft2/s") - 10.763910416709722), 7) == 0
    assert approx(abs(default.GetValue("in2/s") - 1550.0031000062002), 7) == 0
    assert approx(abs(default.GetValue("m2/h") - 3600.0), 7) == 0
    assert approx(abs(default.GetValue("mm2/s") - 1000000.0), 7) == 0
    assert approx(abs(default.GetValue("m2/d") - 86400.0), 7) == 0
    assert approx(abs(default.GetValue("ft2/d") - 930001.8600037199), 7) == 0


def testCreateVolumeQuantityFromLengthQuantity(unit_database_posc) -> None:
    unit_database = unit_database_posc
    length_units = unit_database.GetValidUnits("length")
    convertable_length_units = ["m", "cm", "dm", "ft", "in", "km", "mi", "mm", "yd", "um"]

    for length_unit in length_units:
        length_quantity = ObtainQuantity(length_unit, "length")
        volume_quantity = CreateVolumeQuantityFromLengthQuantity(length_quantity)

        if length_unit in convertable_length_units:
            expected_volume_category = "volume"

        else:
            expected_volume_category = "(length) ** 3"

        assert volume_quantity.GetCategory() == expected_volume_category
        assert volume_quantity.GetUnit() == "%s3" % length_unit


def testCreateAreaQuantityFromLengthQuantity(unit_database_posc) -> None:
    unit_database = unit_database_posc
    length_units = unit_database.GetValidUnits("length")
    convertable_length_units = ["m", "cm", "ft", "in", "km", "mi", "miUS", "mm", "um", "yd"]

    for length_unit in length_units:
        length_quantity = ObtainQuantity(length_unit, "length")
        area_quantity = CreateAreaQuantityFromLengthQuantity(length_quantity)

        if length_unit in convertable_length_units:
            expected_volume_category = "area"

        else:
            expected_volume_category = "(length) ** 2"

        assert area_quantity.GetCategory() == expected_volume_category
        assert area_quantity.GetUnit() == "%s2" % length_unit


def testDefaultCategories(unit_database_posc) -> None:
    """
    Check all units with categories defined
    """
    unit_database = unit_database_posc
    categories = set()
    for unit in unit_database.GetUnits():
        category = unit_database.GetDefaultCategory(unit)
        assert category is not None, "All units MUST have a default category."
        quantity_type = unit_database.GetQuantityType(unit)

        if category != quantity_type:
            categories.add(category)

    assert sorted(categories) == [
        "amount of substance",
        "angle per time",
        "area per volume",
        "concentration",
        "delta temperature",
        "dynamic viscosity",
        "energy length per area",
        "energy length per time area temperature",
        "energy per area",
        "energy per length",
        "fluid gas concentration",
        "force length per length",
        "force per force",
        "heat flow rate",
        "index",
        "length per volume",
        "linear thermal expansion",
        "luminous exitance",
        "mass concentration",
        "mass per length",
        "mobility",
        "mole per mole",
        "multiplier",
        "operations per time",
        "permeability length",
        "permeability rock",
        "pressure squared per (dynamic viscosity)",
        "relative power",
        "relative time",
        "self inductance per length",
        "shear rate",
        "status",
        "volume per area",
        "volume per length",
        "volume per time per area",
        "volume per time per volume",
        "volume per volume",
    ]


def testPoscValidUnitsNotRepeated(unit_database_posc) -> None:
    unit_database = unit_database_posc
    for category in unit_database.IterCategories():
        valid_units = unit_database.GetValidUnits(category)
        assert len(valid_units) == len(
            set(valid_units)
        ), f'There is a duplicate unit defined in "{category}": {valid_units}'


def testPoscKVmm(unit_database_posc) -> None:
    """
    V/m to KV/mm (multiply by 1e6)
    """
    q = ObtainQuantity("V/m")
    assert q.ConvertScalarValue(1, "KV/mm") == 1e6


def testPoscBytes(unit_database_posc) -> None:
    """
    Bytes, kBytes, MBytes, ....
    """
    q = ObtainQuantity("Byte")
    assert q.ConvertScalarValue(1024, "kByte") == 1
    assert q.ConvertScalarValue(1024 * 1024, "MByte") == 1
    assert q.ConvertScalarValue(1024 * 1024 * 1024, "GByte") == 1
    assert q.ConvertScalarValue(1024 * 1024 * 1024 * 1024, "TByte") == 1


def testOhmUnits(unit_database_posc) -> None:
    q = ObtainQuantity("ohm/m")
    assert q.ConvertScalarValue(1, "ohm/km") == 1000


def testPower(unit_database_posc) -> None:
    unit_database = unit_database_posc
    assert "volt ampere" == ObtainQuantity("VA").GetQuantityType()
    assert "volt ampere reactive" == ObtainQuantity("VAr").GetQuantityType()

    assert unit_database.Convert("force", "N", "kN", 56.0) == 0.056
    assert (
        approx(
            abs(
                unit_database.Convert("force", [("N", 2)], [("kN", 2)], -(56.0 * 56))
                - -(0.056 * 0.056)
            ),
            7,
        )
        == 0
    )


def testFluidGasConcentration(unit_database_posc) -> None:
    """
    Total Gas Unit requested for PWDA as concentration
    """
    q = ObtainQuantity("tgu")

    assert "dimensionless" == q.GetQuantityType()

    assert approx(abs(q.ConvertScalarValue(1, "ppm") - 333.33), 7) == 0
    assert approx(abs(q.ConvertScalarValue(1, "%") - 0.033333), 7) == 0
    assert approx(abs(q.ConvertScalarValue(1, "Euc") - 0.00033333), 7) == 0


def testSpringDashpotUnits(unit_database_posc) -> None:
    """
    Units used to define Spring-Dashpot movements
    """

    q = ObtainQuantity("Ns/m")
    assert "force per velocity" == q.GetQuantityType()
    assert approx(abs(q.ConvertScalarValue(1, "lbf.s/ft") - 14.5939029372), 7) == 0

    q = ObtainQuantity("Nm/rad")
    assert "moment per angle" == q.GetQuantityType()
    assert approx(abs(q.ConvertScalarValue(1, "lbf.ft/dega") - 836.169044926), 7) == 0

    q = ObtainQuantity("Nms/rad")
    assert "moment per angular velocity" == q.GetQuantityType()
    assert approx(abs(q.ConvertScalarValue(1, "lbf.ft.s/dega") - 0.017453292519943), 7) == 0


def testConcentrationRatio(unit_database_posc) -> None:
    """
    Units used to express a ratio of concentrations
    """
    concentration_ratio_units = unit_database_posc.GetValidUnits("concentration ratio")
    assert concentration_ratio_units == ["mg/l/mg/l", "kg/m3/kg/m3"]


def testJouleThomsonCoefficientUnits() -> None:
    """
    Results gathered from NIST.
    """
    joule_thomson_si_units = units.Scalar("joule-thomson coefficient", 1, "K/Pa")
    assert joule_thomson_si_units.value == 1.0
    assert joule_thomson_si_units.GetValue("degC/Pa") == 1.0
    assert joule_thomson_si_units.GetValue("degC/MPa") == 1e-6
    assert joule_thomson_si_units.GetValue("degC/bar") == 1e-5
    assert joule_thomson_si_units.GetValue("K/MPa") == 1e-6
    assert joule_thomson_si_units.GetValue("K/bar") == 1e-5
    assert joule_thomson_si_units.GetValue("degF/Pa") == approx(9 / 5)
    assert joule_thomson_si_units.GetValue("degF/MPa") == approx(9 / 5 * 1e-6)
    assert joule_thomson_si_units.GetValue("degF/bar") == approx(9 / 5 * 1e-5)
    assert joule_thomson_si_units.GetValue("degR/Pa") == approx(9 / 5)
    assert joule_thomson_si_units.GetValue("degR/MPa") == approx(9 / 5 * 1e-6)
    assert joule_thomson_si_units.GetValue("degR/bar") == approx(9 / 5 * 1e-5)

    joule_thomson_si_units_mega = units.Scalar("joule-thomson coefficient", 1, "K/MPa")
    assert joule_thomson_si_units_mega.GetValue("K/Pa") == 1e6
    assert joule_thomson_si_units_mega.GetValue("K/bar") == 1e1
    assert joule_thomson_si_units_mega.GetValue("degC/Pa") == 1e6
    assert joule_thomson_si_units_mega.GetValue("degC/bar") == 1e1
    assert joule_thomson_si_units_mega.GetValue("degF/Pa") == approx(9 / 5 * 1e6)
    assert joule_thomson_si_units_mega.GetValue("degF/bar") == approx(9 / 5 * 1e1)


def testDensityDerivativePerTemperatureUnitConversion() -> None:
    density_derivative_per_temperature = units.Scalar(
        "density derivative in respect to temperature", 1, "kg/m3.degC"
    )
    assert density_derivative_per_temperature.value == 1.0
    assert density_derivative_per_temperature.GetValue("kg/m3.K") == 1.0

    density_derivative_per_temperature = units.Scalar(
        "density derivative in respect to temperature", 1, "kg/m3.K"
    )
    assert density_derivative_per_temperature.GetValue("kg/m3.degC") == 1.0


def testStandardVolumePerStandardVolumeSmoke() -> None:
    standard_per_standard = units.Scalar(
        "standard volume per standard volume", 1, "scm(15C)/scm(15C)"
    )
    assert standard_per_standard.GetValue("scm(15C)/scm(15C)") == approx(1.0)
    assert standard_per_standard.GetValue("scf(60F)/stb") == approx(5.625408383313)
    assert standard_per_standard.GetValue("scf(60F)/scf") == approx(1.001928010069)
    assert standard_per_standard.GetValue("stb(60F)/stb") == approx(1.0)
    assert standard_per_standard.GetValue("sm3/sm3") == approx(1.0)
    assert standard_per_standard.GetValue("scm3/scm3") == approx(1.0)
    assert standard_per_standard.GetValue("stb/stb") == approx(1.0)
    assert standard_per_standard.GetValue("Mscf/stb") == approx(0.0056254083833)
    assert standard_per_standard.GetValue("MMscf/stb") == approx(0.0000056254083833)
    assert standard_per_standard.GetValue("scf/stb") == approx(5.62540838331)
    assert standard_per_standard.GetValue("stb/scf") == approx(0.17776487178535644)
    assert standard_per_standard.GetValue("stb/MMscf") == approx(177764.87178535643)


def testHeatTransferCoefficient() -> None:
    default = units.Scalar("heat transfer coefficient", 1, "W/m2.K")
    assert default.value == 1.0
    assert default.GetValue("Btu/hr.ft2.degF") == approx(0.17611019426187197)
    assert default.GetValue("Btu/hr.ft2.degR") == approx(0.17611019426187197)
    assert default.GetValue("Btu/hr.m2.degC") == approx(3.412141285851795)
    assert default.GetValue("Btu/s.ft2.degF") == approx(4.891949074810131e-05)
    assert default.GetValue("cal/h.cm2.degC") == approx(0.08604208146120104)
    assert default.GetValue("cal/s.cm2.degC") == approx(2.390057361376673e-05)
    assert default.GetValue("J/s.m2.degC") == approx(1.0)
    assert default.GetValue("kcal/h.m2.degC") == approx(0.8604208146120104)
    assert default.GetValue("cal/h.m2.degC") == approx(860.4208146120104)
    assert default.GetValue("kJ/h.m2.K") == approx(3.6)
    assert default.GetValue("kW/m2.K") == approx(0.001)


def testProductivityIndex() -> None:
    default = units.Scalar("productivity index", 1, "m3/Pa.s")
    assert default.value == 1.0
    assert default.GetValue("Mcf/psi.d") == approx(21037191.806292012)
    assert default.GetValue("ft3/psi.d") == approx(21037191806.292012)
    assert default.GetValue("bbl/d.psi") == approx(3746884212.8623204)
    assert default.GetValue("bbl/kPa.d") == approx(543439633.228566)
    assert default.GetValue("bbl/psi.d") == approx(3746884215.280088)
    assert default.GetValue("L/bar.min") == approx(6000000000.0)
    assert default.GetValue("m3/bar.d") == approx(8640000000.0)
    assert default.GetValue("m3/bar.h") == approx(360000000.0)
    assert default.GetValue("m3/bar.min") == approx(6000000.0)
    assert default.GetValue("m3/d.kPa") == approx(86400000.0)
    assert default.GetValue("m3/kPa.d") == approx(86400000.0)
    assert default.GetValue("m3/kPa.h") == approx(3600000.0)
    assert default.GetValue("m3/psi.d") == approx(595707004.8)


def testThermalConductivity() -> None:
    default = units.Scalar("thermal conductivity", 1, "W/m.K")
    assert default.GetValue("Btu/hr.ft.degF") == approx(0.5777892051642799)
    assert default.GetValue("cal/h.cm.degC") == approx(8.604208146120104)
    assert default.GetValue("cal/s.cm.degC") == approx(0.002390057361376673)
    assert default.GetValue("cal/m.h.degC") == approx(860.4208146120104)
    assert default.GetValue("kcal/h.m.degC") == approx(0.8604208146120104)
    assert default.GetValue("Btu/d.ft.degF") == approx(13.867702121758425)
    assert default.GetValue("kJ/d.m.K") == approx(86.4304235090752)
    assert default.GetValue("W/m.degC") == approx(1.0)


def testStandardVolumePerTime() -> None:
    default = units.Scalar("standard volume per time", 1, "scm(15C)/s")
    assert default.GetValue("ksm3/d") == approx(86.4)
    assert default.GetValue("MMscf(60F)/d") == approx(3.0570698685888087)
    assert default.GetValue("MMscm(15C)/d") == approx(0.0864)
    assert default.GetValue("MMstb(60F)/d") == approx(0.5434396332285661)
    assert default.GetValue("Mscf(60F)/d") == approx(3057.0698685888087)
    assert default.GetValue("Mscm(15C)/d") == approx(86.4)
    assert default.GetValue("Mstb(60F)/d") == approx(543.4396332285661)
    assert default.GetValue("scf(60F)/d") == approx(3057069.868588809)
    assert default.GetValue("scm(15C)/d") == approx(86400.0)
    assert default.GetValue("stb(60F)/d") == approx(543439.6332285661)
    assert default.GetValue("MMscf/d") == approx(3.0570698685888087)
    assert default.GetValue("MMsm3/d") == approx(0.0864)
    assert default.GetValue("MMstb/d") == approx(0.5434396332285661)
    assert default.GetValue("Mscf/d") == approx(3057.069868588809)
    assert default.GetValue("Msm3/d") == approx(0086.4)
    assert default.GetValue("Mstb/d") == approx(543.4396332285661)
    assert default.GetValue("scf/d") == approx(3057069.868588809)
    assert default.GetValue("sm3/d") == approx(86400.0)
    assert default.GetValue("stb/d") == approx(543439.6332285661)
    assert default.GetValue("sm3/s") == approx(1.0)
