from typing import Any
from typing import Optional

from ._quantity import ObtainQuantity
from ._quantity import Quantity
from barril.units.unit_database import UnaryConversionFunc
from barril.units.unit_database import UnitDatabase


def MakeCustomaryToBase(a: Any, b: Any, c: Any, d: Any) -> UnaryConversionFunc:
    """
    Formula to convert some value from Customary Unit to Base Unit
    (A + BX) / (C + DX)
    X can be any single numeric value or a numpy array
    Integer values are correctly handled, once a, b, c and d parameters
    are always floats

    :rtype: callable
    :returns:
        Returns a callable with the conversion to the base.
    """

    def ret(x: Any) -> Any:
        return (a + b * x) / (c + d * x)

    ret.__a__ = a  # type:ignore[attr-defined]
    ret.__b__ = b  # type:ignore[attr-defined]
    ret.__c__ = c  # type:ignore[attr-defined]
    ret.__d__ = d  # type:ignore[attr-defined]
    ret.__has_conversion__ = True  # type:ignore[attr-defined]

    return ret


def MakeBaseToCustomary(a: Any, b: Any, c: Any, d: Any) -> UnaryConversionFunc:
    """
     Formula to convert some value from Derivate Unit to Base Unit
    (A - CY) / (DY - B)
    Y can be any single numeric value or a numpy array
    Integer values are correctly handled, once a, b, c and d parameters
    are always floats

     :rtype: callable
     :returns:
         Returns a callable with the conversion from the base to a unit (depending on the
         coefficients).
    """

    def ret(y: Any) -> Any:
        return (a - c * y) / (d * y - b)

    ret.__a__ = a  # type:ignore[attr-defined]
    ret.__b__ = b  # type:ignore[attr-defined]
    ret.__c__ = c  # type:ignore[attr-defined]
    ret.__d__ = d  # type:ignore[attr-defined]
    ret.__has_conversion__ = True  # type:ignore[attr-defined]

    return ret


def FillUnitDatabaseWithPosc(
    db: Optional[UnitDatabase] = None,
    fill_categories: bool = True,
    override_categories: bool = False,
) -> UnitDatabase:
    """
    Fills the given database with the posc units and the additional units defined in barril.

    :type db: UnitDatabase or None
    :param db:
        The database to fill. If none is given, an empty one is created.

    :param bool fill_categories:
        If a category corresponding to each quantity type should also be created.

    :param bool override_categories:
        If the categories being created by "fill_categories" should overwrite any existing categories.

    :rtype: UnitDatabase
    :returns:
        The unitdatabase filled.
    """
    if db is None:
        db = UnitDatabase()

    db.AddUnitBase("reluctance", "inverse henry", "1/H")
    db.AddUnitBase("volumetric thermal expansion", "per Kelvin", "1/K")
    db.AddUnitBase("per mass", "per kilogram", "1/kg")
    db.AddUnitBase("per length", "per metre", "1/m")
    db.AddUnitBase("per area", "per square metre", "1/m2")
    db.AddUnitBase("per volume", "per cubic metre", "1/m3")
    db.AddUnitBase("per force", "per Newton", "1/N")
    db.AddUnitBase("compressibility", "per Pascal", "1/Pa")
    db.AddUnitBase("per time", "per second", "1/s")
    db.AddUnitBase("per electric potential", "per Volt", "1/V")
    db.AddUnitBase("electric current", "ampere", "A")
    db.AddUnitBase("electromagnetic moment", "amperes metres squared", "A.m2")
    db.AddUnitBase("magnetization", "amperes/metre", "A/m")
    db.AddUnitBase("current density", "amperes/square metre", "A/m2")
    db.AddUnitBase("level of power intensity", "bel", "B")
    db.AddUnitBase("attenuation per length", "bels/metre", "B/m")
    db.AddUnitBase("attenuation", "bels/octave", "B/O")
    db.AddUnitBase("data transmission speed", "bits per second", "bps")
    db.AddUnitBase("activity (of radioactivity)", "becquerel", "Bq")
    db.AddUnitBase("specific activity (of radioactivity)", "becquerel per kilogram", "Bq/kg")
    db.AddUnitBase("digital storage", "byte", "byte")
    db.AddUnitBase("electric capacity", "coulomb", "C")
    db.AddUnitBase("electric dipole moment", "coulomb metres", "C.m")
    db.AddUnitBase("exposure (radioactivity)", "coulomb per kilogram", "C/kg")
    db.AddUnitBase("electric polarization", "coulombs/square metre", "C/m2")
    db.AddUnitBase("charge density", "coulombs/cubic metre", "C/m3")
    db.AddUnitBase("luminous intensity", "candela", "cd")
    db.AddUnitBase("luminance", "candelas/square metre", "cd/m2")
    db.AddUnitBase("electrochemical equivalent", "equivalent", "eq")
    db.AddUnitBase("equivalent per mass", "equivalent per kilogram", "eq/kg")
    db.AddUnitBase("equivalent per volume", "equivalents per cubic metre", "eq/m3")
    db.AddUnitBase("dimensionless", "euclid", "Euc")
    db.AddUnitBase("capacitance", "farad", "F")
    db.AddUnitBase("permittivity", "farads/metre", "F/m")
    db.AddUnitBase("gamma ray API unit", "API gamma ray units", "gAPI")
    db.AddUnitBase("absorbed dose", "gray", "Gy")
    db.AddUnitBase("self inductance", "henry", "H")
    db.AddUnitBase("magnetic permeability", "henries/metre", "H/m")
    db.AddUnitBase("moment of force", "joule", "J")
    db.AddUnitBase("heat capacity", "joules per delta kelvin", "J/K")
    db.AddUnitBase("specific energy", "joules/kilogram", "J/kg")
    db.AddUnitBase("specific heat capacity", "joules/kilogram degree kelvin", "J/kg.K")
    db.AddUnitBase("normal stress", "joules/cubic metre", "J/m3")
    db.AddUnitBase("molar thermodynamic energy", "joules/mole", "J/mol")
    db.AddUnitBase("molar heat capacity", "joules/mole degree kelvin", "J/mol.K")
    db.AddUnitBase("temperature", "kelvin", "K")
    db.AddUnitBase("thermal insulance", "kelvin metres squared/watt", "K.m2/W")
    db.AddUnitBase("temperature per length", "degrees kelvin/metre", "K/m")
    db.AddUnitBase("temperature per time", "kelvin per second", "K/s")
    db.AddUnitBase("thermal resistance", "delta kelvin per watt", "K/W")
    db.AddUnitBase("mass", "kilogram", "kg")
    db.AddUnitBase("mass length", "meter-kilogram", "kg.m")
    db.AddUnitBase("momentum", "kilogram metres/second", "kg.m/s")
    db.AddUnitBase("moment of inertia", "kilogram metres squared", "kg.m2")
    db.AddUnitBase("mass per energy", "kilograms/joule", "kg/J")
    db.AddUnitBase("linear density", "kilograms/metre", "kg/m")
    db.AddUnitBase("surface density", "kilograms/square metre", "kg/m2")
    db.AddUnitBase("mass per time per area", "kilograms/square metre seconds", "kg/m2.s")
    db.AddUnitBase("density", "kilograms/cubic metre", "kg/m3")
    db.AddUnitBase("mass per volume per length", "kilogram/metre fourth", "kg/m4")
    db.AddUnitBase("mass flow rate", "kilograms/second", "kg/s")
    db.AddUnitBase("luminous flux", "lumen", "lm")
    db.AddUnitBase("quantity of light", "lumen second", "lm.s")
    db.AddUnitBase("luminous efficacy", "lumens/watt", "lm/W")
    db.AddUnitBase("illuminance", "lux", "lx")
    db.AddUnitBase("light exposure", "lux seconds", "lx.s")
    db.AddUnitBase("length", "metre", "m")
    db.AddUnitBase("length per temperature", "metres/degree kelvin", "m/K")
    db.AddUnitBase("velocity", "metres/second", "m/s")
    db.AddUnitBase("acceleration linear", "metres/second squared", "m/s2")
    db.AddUnitBase("area", "square metres", "m2")
    db.AddUnitBase("mass attenuation coefficient", "square metres/kilogram", "m2/kg")
    db.AddUnitBase("cross section absorption", "square metres/mol", "m2/mol")
    db.AddUnitBase("unit productivity index", "square metres/second Pascal", "m2/Pa.s")
    db.AddUnitBase("volume per time per length", "square metres/second", "m2/s")
    db.AddUnitBase("volume", "cubic metres", "m3")
    db.AddUnitBase("isothermal compressibility", "cubic metres/joule", "m3/J")
    db.AddUnitBase("specific volume", "cubic metres/kilogram", "m3/kg")
    db.AddUnitBase("molar volume", "cubic metres/mole", "m3/mol")
    db.AddUnitBase("productivity index", "cubic metres/second pascal", "m3/Pa.s")
    db.AddUnitBase(
        "forchheimer linear productivity index",
        "square pascal second/standard cubic metres",
        "Pa2.s/scm",
    )
    db.AddUnitBase(
        "forchheimer quadratic productivity index",
        "square pascal square second/square standard cubic metres",
        "Pa2.s2/scm2",
    )
    db.AddUnitBase("specific productivity index", "cubic metres/pascal second squared", "m3/Pa2.s2")
    db.AddUnitBase("volume flow rate", "cubic metres/second", "m3/s")
    db.AddUnitBase("volume per time per time", "cubic metres/seconds squared", "m3/s2")
    db.AddUnitBase(
        "volume per standard volume", "cubic metres/std cubic metres, 15 deg C", "m3/scm(15C)"
    )
    db.AddUnitBase("second moment of area", "metres fourth", "m4")
    db.AddUnitBase("volume length per time", "metres fourth/second", "m4/s")
    db.AddUnitBase("molar mass", "mole", "mol")
    db.AddUnitBase("mole per area", "moles/square metre", "mol/m2")
    db.AddUnitBase("mole per time per area", "moles/square metre second", "mol/m2.s")
    db.AddUnitBase("concentration of B", "moles/cubic metre", "mol/m3")
    db.AddUnitBase("mole per time", "moles/second", "mol/s")
    db.AddUnitBase("force", "newton", "N")
    db.AddUnitBase("force area", "newton square metres", "N.m2")
    db.AddUnitBase("force per length", "newtons/metre", "N/m")
    db.AddUnitBase("force per volume", "newtons/cubic metre", "N/m3")
    db.AddUnitBase("parachor", "newtons fourth metres/kilogram", "N4/kg.m7")
    db.AddUnitBase("neutron API unit", "API neutron units", "nAPI")
    db.AddUnitBase("frequency interval", "octave", "O")
    db.AddUnitBase("resistance", "ohm", "ohm")
    db.AddUnitBase("electrical resistivity", "ohm metre", "ohm.m")
    db.AddUnitBase("resistivity per length", "ohm per metre", "ohm/m")
    db.AddUnitBase("pressure", "pascal", "Pa")
    db.AddUnitBase("mass per time per length", "pascal seconds", "Pa.s")
    db.AddUnitBase("pressure time per volume", "pascal seconds/cubic metre", "Pa.s/m3")
    db.AddUnitBase("nonDarcy flow coefficient", "pascal second /cubic metre squared", "Pa.s/m6")
    db.AddUnitBase("pressure per length", "pascals/metre", "Pa/m")
    db.AddUnitBase("Darcy flow coefficient", "pascals/cubic metre", "Pa/m3")
    db.AddUnitBase("pressure per time", "pascal/ second", "Pa/s")
    db.AddUnitBase("pressure squared", "pascal squared", "Pa2")
    db.AddUnitBase("pH", "pH", "pH")
    db.AddUnitBase("plane angle", "radian", "rad")
    db.AddUnitBase("angle per length", "radians/metre", "rad/m")
    db.AddUnitBase("angle per volume", "radians per cubic metre", "rad/m3")
    db.AddUnitBase("frequency", "radians/second", "rad/s")
    db.AddUnitBase("angular acceleration", "radians/second squared", "rad/s2")
    db.AddUnitBase("electric conductance", "siemens", "S")
    db.AddUnitBase("time", "second", "s")
    db.AddUnitBase("conductivity", "siemens/metre", "S/m")
    db.AddUnitBase("time per length", "seconds/metre", "s/m")
    db.AddUnitBase("time per volume", "seconds/cubic metre", "s/m3")
    db.AddUnitBase("standard volume", "standard cubic metres at 15 deg Celsius", "scm(15C)")
    db.AddUnitBase(
        "standard volume per area", "std cubic metres, 15 deg C/square metre", "scm(15C)/m2"
    )
    db.AddUnitBase(
        "standard volume per volume", "std cubic metres, 15 deg C/cubic metre", "scm(15C)/m3"
    )
    db.AddUnitBase(
        "standard volume per standard volume",
        "std cubic metres, 15 deg C/std cubic metres, 15 deg C",
        "scm(15C)/scm(15C)",
    )
    db.AddUnitBase("standard volume per time", "std cubic metres, 15 deg C/second", "scm(15C)/s")
    db.AddUnitBase("solid angle", "steradian", "sr")
    db.AddUnitBase("dose equivalent", "sievert", "Sv")
    db.AddUnitBase("dose equivalent rate", "sievert per second", "Sv/s")
    db.AddUnitBase("magnetic induction", "tesla", "T")
    db.AddUnitBase("electric potential", "volt", "V")
    db.AddUnitBase("potential difference per per power drop", "volts/Bel", "V/B")
    db.AddUnitBase("electric field strength", "volts/metre", "V/m")
    db.AddUnitBase("power", "watt", "W")
    db.AddUnitBase("thermal conductance", "Watts per delta kelvin", "W/K")
    db.AddUnitBase("thermal conductivity", "watts/metre kelvin", "W/m.K")
    db.AddUnitBase("density of heat flow rate", "watts/square metre", "W/m2")
    db.AddUnitBase("heat transfer coefficient", "watts/square metre kelvin", "W/m2.K")
    db.AddUnitBase("radiance", "watts/square metre steradian", "W/m2.sr")
    db.AddUnitBase("power per volume", "watts/cubic metre", "W/m3")
    db.AddUnitBase("volumetric heat transfer coefficient", "watts/cubic metre kelvin", "W/m3.K")
    db.AddUnitBase("radiant intensity", "watts/steradian", "W/sr")
    db.AddUnitBase("magnetic flux", "weber", "Wb")
    db.AddUnitBase("magnetic dipole moment", "weber metres", "Wb.m")
    db.AddUnitBase("magnetic vector potential", "webers/metre", "Wb/m")
    db.AddUnitBase("injectivity factor", "injectivity factor", "m3/s.Pa")
    db.AddUnitBase("datetime", "datetime", "datetime")
    db.AddUnitBase("Unknown", "<unknown>", "<unknown>")
    db.AddUnitBase("dimensionless", "-", "-")
    db.AddUnitBase("transmissibility", "cp.m3/day/bar", "cp.m3/day/bar")
    db.AddUnitBase("solubility product", "squared mol/m3", "(mol/m3)^2")
    db.AddUnitBase("per time squared", "Per days squared", "1/d^2")
    db.AddUnitBase("adsorption rate", "mgrams per kg per day", "mg/kg/d")
    db.AddUnitBase(
        "mass consumption efficiency", "mgrams per liters per mgrams per liters", "mg/l/mg/l"
    )
    db.AddUnitBase("density generation", "kgram for cubic meter per day", "kg/m3/d")
    db.AddUnitBase("volumetric concentration", "concentration by kg by m3", "ppm/kg/m3")
    db.AddUnitBase(
        "efficiency of nutrient consumption for biomass building",
        "kilogram/cubic metre/days/kilogram/cubic metre",
        "kg/m3/d/kg/m3",
    )
    db.AddUnitBase(
        "parts per million by volume per concentration",
        "parts per million by volume per milligram per litre",
        "ppmv/mg/l",
    )
    db.AddUnitBase("fluid consistency", "pascal seconds to the power of n", "Pa.s^n")
    db.AddUnitBase("volume fraction per temperature", "(volume/volume)/temperature", "(m3/m3)/K")
    db.AddUnitBase("per weight percent", "per weight percent", "1/wtpercent")
    db.AddUnitBase(
        "per square weight percent", "per square weight percent", "1/wtpercent*wtpercent"
    )
    db.AddUnitBase(
        "per cubic weight percent", "per cubic weight percent", "1/wtpercent*wtpercent*wtpercent"
    )
    db.AddUnitBase("volume per equivalent", "milliliter/milliequivalents", "mL/meq")
    db.AddUnitBase("volume per wtpercent", "m3/wtpercent", "m3/wtpercent")
    db.AddUnitBase("mass per mol", "kg/mol", "kg/mol")
    db.AddUnitBase("mole per mass", "mol/kg", "mol/kg")
    db.AddUnitBase("viscosity per pressure", "pascal seconds per pascal", "Pa.s/Pa")
    db.AddUnitBase("stroke frequency", "strokes per minute", "spm")
    db.AddUnitBase("power per mass", "watts/kilogram", "W/kg")
    db.AddUnitBase("concentration per square time", "concentration per square time", "kg/m3/d2")
    db.AddUnitBase("power per length", "watt per metre", "W/m")
    db.AddUnitBase("volt ampere reactive", "volt ampere reactive", "VAr")
    db.AddUnitBase("volt ampere", "volt ampere", "VA")
    db.AddUnitBase(
        "density derivative in respect to pressure", "kilogram per cubic meter Pascal", "kg/m3.Pa"
    )
    db.AddUnitBase(
        "density derivative in respect to temperature",
        "kilogram per cubic meter degrees Celsius",
        "kg/m3.degC",
    )
    db.AddUnitBase("computer binary memory", "Byte", "Byte")
    db.AddUnitBase("flow coefficient", "flow rate per pressure power of 0.5 ", "(m3/s)/(Pa^0.5)")
    db.AddUnitBase("temperature per area", "degrees Celsius per square meter", "degC/m2")
    db.AddUnitBase("force per velocity", "Newton second per meter", "N.s/m")
    db.AddUnitBase("force per angle", "Newton per angle", "N/rad")
    db.AddUnitBase("force per angular velocity", "Newton second per angle", "Ns/rad")
    db.AddUnitBase("moment per angle", "Newton meter per angle", "Nm/rad")
    db.AddUnitBase("moment per angular velocity", "newton meter per angular velocity", "Nms/rad")
    db.AddUnitBase("mass temperature per mol", "kg.K/mol", "kg.K/mol")
    db.AddUnitBase("joule-thomson coefficient", "delta kelvin per pascal", "K/Pa")
    db.AddUnitBase(
        "force per velocity squared", "Newton second squared per meter squared", "N.s2/m2"
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6.283185307, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6.283185307, 1.0, 0.0)
    db.AddUnit("frequency", "hertz", "Hz", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "dimensionless", "percent", "%", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 31558150, 0.0)
    db.AddUnit(
        "per time", "per annum", "1/a", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10000000000, 1.0, 0.0)
    db.AddUnit(
        "per length",
        "per angstrom",
        "1/angstrom",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00001, 1.0, 0.0)
    db.AddUnit(
        "compressibility", "per bar", "1/bar", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.1589873, 0.0)
    db.AddUnit(
        "per volume", "per barrel", "1/bbl", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100, 1.0, 0.0)
    db.AddUnit(
        "per length",
        "per centimetre",
        "1/cm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "per length",
        "per micrometre",
        "1/um",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400, 0.0)
    db.AddUnit("per time", "per day", "1/d", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "volumetric thermal expansion",
        "per degree Celsius",
        "1/degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9, 5, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9, 5, 0.0)
    db.AddUnit(
        "volumetric thermal expansion",
        "per degree Fahrenheit",
        "1/degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9, 5, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9, 5, 0.0)
    db.AddUnit(
        "volumetric thermal expansion",
        "per degree Rankine",
        "1/degR",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.3048, 0.0)
    db.AddUnit(
        "per length", "per foot", "1/ft", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.09290304, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.09290304, 0.0)
    db.AddUnit(
        "per area",
        "per square foot",
        "1/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.02831685, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.02831685, 0.0)
    db.AddUnit(
        "per volume",
        "per cubic foot",
        "1/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit("per mass", "per gram", "1/g", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.00456092, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.00456092, 0.0)
    db.AddUnit(
        "per volume",
        "per UK gallon",
        "1/galUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.003785412, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.003785412, 0.0)
    db.AddUnit(
        "per volume",
        "per US gallon",
        "1/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit("per time", "per hour", "1/h", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.0254, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.0254, 0.0)
    db.AddUnit(
        "per length", "per inch", "1/in", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1000000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1000000, 0.0)
    db.AddUnit(
        "per area",
        "per square kilometre",
        "1/km2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "compressibility",
        "per kilopascal",
        "1/kPa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "per volume", "per litre", "1/L", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 4.448222, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 4.448222, 0.0)
    db.AddUnit(
        "per force",
        "per pound force",
        "1/lbf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.4535924, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.4535924, 0.0)
    db.AddUnit(
        "per mass", "per pound", "1/lbm", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1609.344, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1609.344, 0.0)
    db.AddUnit(
        "per length", "per mile", "1/mi", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 2589988.11, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 2589988.11, 0.0)
    db.AddUnit(
        "per area",
        "per square mile",
        "1/mi2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 60, 0.0)
    db.AddUnit(
        "per time", "per minute", "1/min", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "per length",
        "per millimetre",
        "1/mm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000, 1.0, 0.0)
    db.AddUnit(
        "per length", "per nanometre", "1/nm", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000000, 1.0, 0.0)
    db.AddUnit(
        "compressibility",
        "per pico pascal",
        "1/pPa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 6894.757, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 6894.757, 0.0)
    db.AddUnit(
        "compressibility",
        "per pounds/square inch",
        "1/psi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.006894757, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.006894757, 0.0)
    db.AddUnit(
        "compressibility",
        "per micro pounds per square inch",
        "1/upsi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "per electric potential",
        "per microvolt",
        "1/uV",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 604800, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 604800, 0.0)
    db.AddUnit(
        "per time", "per week", "1/wk", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.9144, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.9144, 0.0)
    db.AddUnit(
        "per length", "per yard", "1/yd", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28.316846592, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28.316846592, 1.0, 0.0)
    db.AddUnit(
        "volume",
        "thousand cubic feet",
        "Mcf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28.316846592, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28.316846592, 0.1589873, 0.0)
    db.AddUnit(
        "dimensionless",
        "thousand cubic feet per barrel",
        "Mcf/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 92.90304, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 92.90304, 86400, 0.0)
    db.AddUnit(
        "volume per time per length",
        "thousand cubic feet per day per foot",
        "Mcf/d.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28.31685, 595707004.8, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28.31685, 595707004.8, 0.0)
    db.AddUnit(
        "productivity index",
        "thousand cubic feet per day per psi",
        "Mcf/psi.d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 595707004.8, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 595707004.8, 0.0)
    db.AddUnit(
        "productivity index",
        "cubic feet per day per psi",
        "ft3/psi.d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 86400, 0.0)
    db.AddUnit(
        "volume flow rate",
        "thousand cubic metres per day",
        "Mm3/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 86400, 0.0)
    db.AddUnit(
        "volume per time per length",
        "thousand cubic meter per day per meter",
        "Mm3/d.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 3600, 0.0)
    db.AddUnit(
        "volume flow rate",
        "thousand cubic metres per hour",
        "Mm3/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 3600, 0.0)
    db.AddUnit(
        "volume per time per length",
        "thousand cubic meters per hour per meter",
        "Mm3/h.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 86400, 0.0)
    db.AddUnit(
        "volume length per time",
        "thousand (cubic meter per day)-meter",
        "1000m4/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3155815000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3155815000000, 1.0, 0.0)
    db.AddUnit(
        "time", "100000 years", "100ka", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10000, 1.0, 0.0)
    db.AddUnit(
        "density",
        "ten thousand kilograms per cubic metre",
        "10Mg/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 31558150, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 31558150, 1.0, 0.0)
    db.AddUnit("time", "annum", "a", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600, 1.0, 0.0)
    db.AddUnit(
        "electric capacity",
        "Ampere hour",
        "A.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10000, 1.0, 0.0)
    db.AddUnit(
        "current density",
        "ampere per square centimeter",
        "A/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.09290304, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.09290304, 0.0)
    db.AddUnit(
        "current density",
        "ampere per square foot",
        "A/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "magnetization",
        "Ampere/millimetre",
        "A/mm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "current density",
        "Ampere/square millimetre",
        "A/mm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4046.873, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4046.873, 1.0, 0.0)
    db.AddUnit("area", "acre", "acre", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1233.489, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1233.489, 1.0, 0.0)
    db.AddUnit(
        "volume", "acre foot", "acre.ft", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1233.489, 158987.3, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1233.489, 158987.3, 0.0)
    db.AddUnit(
        "volume per standard volume",
        "acre feet/million stbs, 60 deg F",
        "acre.ft/MMstb",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1e-021, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1e-021, 1.0, 0.0)
    db.AddUnit("mass", "attogram", "ag", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1e-018, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1e-018, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "attojoule", "aJ", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000000001, 1.0, 0.0)
    db.AddUnit(
        "length", "Angstrom", "angstrom", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 98066.5, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 98066.5, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "Technical atmosphere",
        "at",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 101325, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 101325, 1.0, 0.0)
    db.AddUnit(
        "pressure", "Atmosphere", "atm", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 101325, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 101325, 0.3048, 0.0)
    db.AddUnit(
        "pressure per length",
        "Atmospheres per ft",
        "atm/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 101325, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 101325, 3600, 0.0)
    db.AddUnit(
        "pressure per time",
        "atmosphere per hour",
        "atm/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 101325, 100, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 101325, 100, 0.0)
    db.AddUnit(
        "pressure per length",
        "Atmospheres per hundred metre",
        "atm/hm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 101325, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 101325, 1.0, 0.0)
    db.AddUnit(
        "pressure per length",
        "Atmospheres/metre",
        "atm/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1e028, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1e028, 1.0, 0.0)
    db.AddUnit("area", "barn", "b", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1e034, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1e034, 1.0, 0.0)
    db.AddUnit(
        "per length",
        "barns/cubic centimetre",
        "b/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="area per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00006023, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00006023, 1.0, 0.0)
    db.AddUnit(
        "cross section absorption",
        "barns/electron",
        "b/elec",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100000, 1.0, 0.0)
    db.AddUnit("pressure", "bar", "bar", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(101325.0, 100000.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(101325.0, 100000.0, 1.0, 0.0)
    db.AddUnit(
        "pressure", "bar gauge", "bar(g)", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100000, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100000, 3600, 0.0)
    db.AddUnit(
        "pressure per time",
        "bar per hour",
        "bar/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100, 1.0, 0.0)
    db.AddUnit(
        "pressure per length",
        "bar per kilometer",
        "bar/km",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100000, 1.0, 0.0)
    db.AddUnit(
        "pressure per length",
        "bar per meter",
        "bar/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10000000000, 1.0, 0.0)
    db.AddUnit(
        "pressure squared",
        "bar squared",
        "bar2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0e13, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0e13, 1.0, 0.0)
    db.AddUnit(
        "pressure per time",
        "bar squared per centipoise",
        "bar2/cP",
        f_base_to_unit,
        f_unit_to_base,
        default_category="pressure squared per (dynamic viscosity)",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 1.0, 0.0)
    db.AddUnit("volume", "barrel", "bbl", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "barrel per hundred barrel",
        "bbl/100bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 4046.879, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 4046.879, 0.0)
    db.AddUnit(
        "length",
        "barrels/acre",
        "bbl/acre",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 1233.489, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 1233.489, 0.0)
    db.AddUnit(
        "dimensionless",
        "barrel/acre foot",
        "bbl/acre.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "barrel/barrel",
        "bbl/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 595707, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 595707, 0.0)
    db.AddUnit(
        "specific productivity index",
        "barrels/centiPoise day psi",
        "bbl/cP.d.psi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 1.0, 0.0)
    db.AddUnit(
        "volume flow rate",
        "barrel/second",
        "bbl/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 86400, 0.0)
    db.AddUnit(
        "volume flow rate",
        "barrel/day",
        "bbl/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 106573450, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 106573450, 0.0)
    db.AddUnit(
        "per time",
        "barrels/day acre foot",
        "bbl/d.acre.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per time per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 26334.72, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 26334.72, 0.0)
    db.AddUnit(
        "volume per time per length",
        "barrels/day foot",
        "bbl/d.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000266888418, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000266888418, 0.3048, 0.0)
    db.AddUnit(
        "unit productivity index",
        "barrels/day foot pounds/sq in",
        "bbl/d.ft.psi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000266888418, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000266888418, 1.0, 0.0)
    db.AddUnit(
        "productivity index",
        "barrel/day pounds/square inch",
        "bbl/d.psi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000000000212978, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000000000212978, 1.0, 0.0)
    db.AddUnit(
        "volume per time per time",
        "barrels/day per day",
        "bbl/d2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 0.3048, 0.0)
    db.AddUnit(
        "area",
        "barrel/foot",
        "bbl/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 0.02831685, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 0.02831685, 0.0)
    db.AddUnit(
        "dimensionless",
        "barrel per cubic foot",
        "bbl/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 3600, 0.0)
    db.AddUnit(
        "volume flow rate",
        "barrel/hour",
        "bbl/hr",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 12960000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 12960000, 0.0)
    db.AddUnit(
        "volume per time per time",
        "barrels/hour/hour",
        "bbl/hr2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 0.0254, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 0.0254, 0.0)
    db.AddUnit(
        "area",
        "barrel/inch",
        "bbl/in",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 86400000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 86400000, 0.0)
    db.AddUnit(
        "productivity index",
        "barrel per day per kilopascal",
        "bbl/kPa.d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 8.64e4, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 8.64e4, 1.0, 0.0)
    db.AddUnit(
        "forchheimer linear productivity index",
        "square pascal day per standard cubic metres",
        "Pa2.d/scm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4107255390590.574957095427052896, 0.028316846592, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4107255390590.574957095427052896, 0.028316846592, 0.0)
    db.AddUnit(
        "forchheimer linear productivity index",
        "square psi day per standard cubic feet",
        "psi2.d/scf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4107255390590.574957095427052896, 28.316846592, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4107255390590.574957095427052896, 28.316846592, 0.0)
    db.AddUnit(
        "forchheimer linear productivity index",
        "square psi day per thousand standard cubic feet",
        "psi2.d/Mscf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 8.64e14, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 8.64e14, 1.0, 0.0)
    db.AddUnit(
        "forchheimer linear productivity index",
        "square bar day per standard cubic metres",
        "bar2.d/scm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 7.46496e9, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 7.46496e9, 1.0, 0.0)
    db.AddUnit(
        "forchheimer quadratic productivity index",
        "square pascal square day per standard cubic metres",
        "Pa2.d2/scm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(
        0.0, 354866865747025676.29304489737021, 8.01843800914862014464e-04, 0.0
    )
    f_base_to_unit = MakeBaseToCustomary(
        0.0, 354866865747025676.29304489737021, 8.01843800914862014464e-04, 0.0
    )
    db.AddUnit(
        "forchheimer quadratic productivity index",
        "square psi square day per square standard cubic feet",
        "psi2.d2/scf2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(
        0.0, 354866865747025676.29304489737021, 8.01843800914862014464e-01, 0.0
    )
    f_base_to_unit = MakeBaseToCustomary(
        0.0, 354866865747025676.29304489737021, 8.01843800914862014464e-01, 0.0
    )
    db.AddUnit(
        "forchheimer quadratic productivity index",
        "square psi square day per thousand square standard cubic feet",
        "psi2.d2/Mscf2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 7.46496e19, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 7.46496e19, 1.0, 0.0)
    db.AddUnit(
        "forchheimer quadratic productivity index",
        "square bar square day per square standard cubic metres",
        "bar2.d2/scm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 28316.85, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 28316.85, 0.0)
    db.AddUnit(
        "dimensionless",
        "barrel per million cubic feet",
        "bbl/MMcf",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 1609.344, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 1609.344, 0.0)
    db.AddUnit(
        "area",
        "barrel/mile",
        "bbl/mi",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 60, 0.0)
    db.AddUnit(
        "volume flow rate",
        "barrel per minute",
        "bbl/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 28262.357, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 28262.357, 0.0)
    db.AddUnit(
        "volume per standard volume",
        "barrels/million std cubic feet, 60 degF",
        "bbl/MMscf(60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 595707004.8, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 595707004.8, 0.0)
    db.AddUnit(
        "productivity index",
        "barrel per day per psi",
        "bbl/psi.d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "volume per standard volume",
        "barrels/stock tank barrel, 60 deg F",
        "bbl/stb(60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 156.4763, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 156.4763, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "barrel per U.K. ton",
        "bbl/tonUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 175.2535, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 175.2535, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "barrel per U.S. ton",
        "bbl/tonUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28316850, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28316850, 1.0, 0.0)
    db.AddUnit(
        "volume", "billion cubic feet", "bcf", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 8, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 8, 0.0)
    db.AddUnit(
        "digital storage", "bit", "bit", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1055.056, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1055.056, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "British thermal unit",
        "Btu",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1442279, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1442279, 1.0, 0.0)
    db.AddUnit(
        "thermal conductivity",
        "Btus/hour foot squared deg F per inch",
        "Btu.in/hr.ft2.F",
        f_base_to_unit,
        f_unit_to_base,
        default_category="energy length per time area temperature",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 293071.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 293071.1, 1.0, 0.0)
    db.AddUnit(
        "power",
        "million Btus/hour",
        "Btu(million)/hr",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1055.056, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1055.056, 0.1589873, 0.0)
    db.AddUnit(
        "normal stress",
        "British thermal units/barrel",
        "Btu/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0003930148, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0003930148, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "Btus/brake-horsepower hour",
        "Btu/bhp.hr",
        f_base_to_unit,
        f_unit_to_base,
        default_category="relative power",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 37258.95, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 37258.95, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "British thermal units/cubic foot",
        "Btu/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 232080, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 232080, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "British thermal units/U.K. gallon",
        "Btu/galUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 278716.3, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 278716.3, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "British thermal units/U.S. gallon",
        "Btu/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.2930711, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.2930711, 1.0, 0.0)
    db.AddUnit(
        "power",
        "British thermal unit/hour",
        "Btu/hr",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.730735, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.730735, 1.0, 0.0)
    db.AddUnit(
        "thermal conductivity",
        "British thermal units/hour foot deg F",
        "Btu/hr.ft.degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3.154591, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3.154591, 1.0, 0.0)
    db.AddUnit(
        "density of heat flow rate",
        "Btus/hour per square foot",
        "Btu/hr.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5.678263, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5.678263, 1.0, 0.0)
    db.AddUnit(
        "heat transfer coefficient",
        "Btus/hour foot squared deg F",
        "Btu/hr.ft2.degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5.678263, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5.678263, 1.0, 0.0)
    db.AddUnit(
        "heat transfer coefficient",
        "Btus/hour foot squared deg R",
        "Btu/hr.ft2.degR",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10.34971, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10.34971, 1.0, 0.0)
    db.AddUnit(
        "power per volume",
        "British thermal units/hour cubic foot",
        "Btu/hr.ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 18.62947, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 18.62947, 1.0, 0.0)
    db.AddUnit(
        "volumetric heat transfer coefficient",
        "Btus/hour foot cubed deg F",
        "Btu/hr.ft3.degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.2930711, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.2930711, 1.0, 0.0)
    db.AddUnit(
        "heat transfer coefficient",
        "Btus/hour metre squared deg C",
        "Btu/hr.m2.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 2326, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2326, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "British thermal units/pound mass",
        "Btu/lbm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4186.8, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4186.8, 1.0, 0.0)
    db.AddUnit(
        "specific heat capacity",
        "British thermal units/pound mass deg F",
        "Btu/lbm.degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4186.8, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4186.8, 1.0, 0.0)
    db.AddUnit(
        "specific heat capacity",
        "British thermal units/pound mass deg R",
        "Btu/lbm.degR",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 17.58427, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 17.58427, 1.0, 0.0)
    db.AddUnit(
        "power",
        "British thermal units/minute",
        "Btu/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 2.326, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2.326, 1.0, 0.0)
    db.AddUnit(
        "molar thermodynamic energy",
        "British thermal units/pound mass mol",
        "Btu/lbmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 2326, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2326, 1.0, 0.0)
    db.AddUnit(
        "molar thermodynamic energy",
        "British thermal units/pound mass mol",
        "Btu/mol(lbm)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.1868, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.1868, 1.0, 0.0)
    db.AddUnit(
        "molar heat capacity",
        "Btus/pound mass mol deg F",
        "Btu/lbmol.F",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4186.8, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4186.8, 1.0, 0.0)
    db.AddUnit(
        "molar heat capacity",
        "Btus/pound mass mol deg F",
        "Btu/mol(lbm).F",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1055.056, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1055.056, 1.0, 0.0)
    db.AddUnit(
        "power",
        "British thermal units/second",
        "Btu/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 11356.53, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 11356.53, 1.0, 0.0)
    db.AddUnit(
        "density of heat flow rate",
        "British thermal units/second square foot",
        "Btu/s.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 20441.75, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 20441.75, 1.0, 0.0)
    db.AddUnit(
        "heat transfer coefficient",
        "Btus/second per square foot deg F",
        "Btu/s.ft2.degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 37258.95, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 37258.95, 1.0, 0.0)
    db.AddUnit(
        "power per volume",
        "Btus/second per cubic foot",
        "Btu/s.ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 67066.11, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 67066.11, 1.0, 0.0)
    db.AddUnit(
        "volumetric heat transfer coefficient",
        "Btus/second per cubic foot deg F",
        "Btu/s.ft3.degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6.283185307, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6.283185307, 1.0, 0.0)
    db.AddUnit("plane angle", "cycle", "c", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.0001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.0001, 0.0)
    db.AddUnit(
        "electric polarization",
        "Coulombs/square centimetre",
        "C/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.000001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.000001, 0.0)
    db.AddUnit(
        "charge density",
        "Coulombs/cubic centimeter",
        "C/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "exposure (radioactivity)",
        "coulomb per gram",
        "C/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.000001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.000001, 0.0)
    db.AddUnit(
        "electric polarization",
        "Coulombs/square millimetre",
        "C/mm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.000000001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.000000001, 0.0)
    db.AddUnit(
        "charge density",
        "Coulombs/cubic millimetre",
        "C/mm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6.283185307, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6.283185307, 1.0, 0.0)
    db.AddUnit(
        "frequency", "cycles/second", "c/s", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.184, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.184, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "calorie", "cal", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.184, 0.000001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.184, 0.000001, 0.0)
    db.AddUnit(
        "normal stress",
        "calories/cubic centimetre",
        "cal/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "calories/gram",
        "cal/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184, 1.0, 0.0)
    db.AddUnit(
        "specific heat capacity",
        "calories/gram degree Kelvin",
        "cal/g.K",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1162222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1162222, 1.0, 0.0)
    db.AddUnit(
        "thermal conductivity",
        "calories/hour centimetre degree Celsius",
        "cal/h.cm.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 11.62222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 11.62222, 1.0, 0.0)
    db.AddUnit(
        "density of heat flow rate",
        "calories/hour centimetre squared",
        "cal/h.cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 11.62222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 11.62222, 1.0, 0.0)
    db.AddUnit(
        "heat transfer coefficient",
        "calories/hour square centimetre deg C",
        "cal/h.cm2.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1162.222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1162.222, 1.0, 0.0)
    db.AddUnit(
        "power per volume",
        "calories/hour cubic centimetre",
        "cal/h.cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.184, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.184, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "calories/kilogram",
        "cal/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.224141, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.224141, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "calories/pound mass",
        "cal/lbm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184000, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "calories/milliliter",
        "cal/mL",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.184, 0.000000001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.184, 0.000000001, 0.0)
    db.AddUnit(
        "normal stress",
        "calories/cubic millimetre",
        "cal/mm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.184, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.184, 1.0, 0.0)
    db.AddUnit(
        "molar heat capacity",
        "calories/gram mol degree celsius",
        "cal/mol.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184, 1.0, 0.0)
    db.AddUnit(
        "molar heat capacity",
        "calories/gram mol degree celsius",
        "cal/mol(g).degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 418.4, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 418.4, 1.0, 0.0)
    db.AddUnit(
        "thermal conductivity",
        "calories/second centimetre deg C",
        "cal/s.cm.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 41840, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 41840, 1.0, 0.0)
    db.AddUnit(
        "heat transfer coefficient",
        "calories/second square centimetre deg C",
        "cal/s.cm2.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184000, 1.0, 0.0)
    db.AddUnit(
        "power per volume",
        "calories/second cubic centimetre",
        "cal/s.cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3.1415926535898, 2000000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3.1415926535898, 2000000, 0.0)
    db.AddUnit(
        "plane angle",
        "centesimal second",
        "ccgr",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "centiEuclid",
        "cEuc",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3.1415926535898, 20000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3.1415926535898, 20000, 0.0)
    db.AddUnit(
        "plane angle",
        "centesimal minute",
        "cgr",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 735.499, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 735.499, 1.0, 0.0)
    db.AddUnit("power", "ch", "ch", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 2647796, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2647796, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "ch hours", "ch.h", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 20.1167824, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 20.1167824, 1.0, 0.0)
    db.AddUnit(
        "length",
        "Benoit chain (1895 A)",
        "chBnA",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 792, 39.370113, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 792, 39.370113, 0.0)
    db.AddUnit(
        "length",
        "Benoit chain (1895 B)",
        "chBnB",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 20.11661949, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 20.11661949, 1.0, 0.0)
    db.AddUnit(
        "length", "Clarke chain", "chCla", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 792, 39.370147, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 792, 39.370147, 0.0)
    db.AddUnit(
        "length", "Sears chain", "chSe", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1899.101, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1899.101, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "chus", "Chu", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 792, 39.37, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 792, 39.37, 0.0)
    db.AddUnit(
        "length", "US Survey chain", "chUS", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 37000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 37000000000, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "curie",
        "Ci",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit("length", "centimetre", "cm", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 31558150, 0.0)
    db.AddUnit(
        "velocity",
        "centimeter per year",
        "cm/a",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "centimetre/second",
        "cm/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "acceleration linear",
        "centimetre/second squared",
        "cm/s2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0001, 1.0, 0.0)
    db.AddUnit(
        "area", "square centimetre", "cm2", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "mass attenuation coefficient",
        "centimetres squared/gram",
        "cm2/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0001, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "centimetres squared/second",
        "cm2/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "volume", "cubic centimetre", "cm3", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1800, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1800, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic centimeter per thirty minutes",
        "cm3/30min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "cubic centimeters/ cubic centimetres",
        "cm3/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "cubic centimetres/gram",
        "cm3/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 3600, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic centimeter per hour",
        "cm3/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "cubic centimetre/cubic metre",
        "cm3/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 60, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic centimeter per minute",
        "cm3/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic centimeter per second",
        "cm3/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00000001, 1.0, 0.0)
    db.AddUnit(
        "second moment of area",
        "centimetres fourth",
        "cm4",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 98.0638, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 98.0638, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "cm of water at 4 degC.",
        "cmH2O(4degC)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "centipoise",
        "cP",
        f_base_to_unit,
        f_unit_to_base,
        default_category="dynamic viscosity",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "time", "ten milli second", "cs", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0001, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "Stoke",
        "St",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "centiStoke",
        "cSt",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0002, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0002, 1.0, 0.0)
    db.AddUnit("mass", "carat", "ct", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "per length",
        "capture unit",
        "cu",
        f_base_to_unit,
        f_unit_to_base,
        default_category="area per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 1.0, 0.0)
    db.AddUnit(
        "volume", "cubic feet", "cu ft", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00001638706, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00001638706, 1.0, 0.0)
    db.AddUnit(
        "volume", "cubic inch", "cu in", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.7645549, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.7645549, 1.0, 0.0)
    db.AddUnit(
        "volume", "cubic yard", "cu yd", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4168182000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4168182000, 1.0, 0.0)
    db.AddUnit(
        "volume", "cubic mile", "cubem", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 37000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 37000000000, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "curie",
        "curie",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 735.499, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 735.499, 1.0, 0.0)
    db.AddUnit(
        "power", "cheval vapeur", "CV", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 2647796, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2647796, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "CV hours", "CV.h", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 50.80235, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 50.80235, 1.0, 0.0)
    db.AddUnit(
        "mass", "UK hundredweight", "cwtUK", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 45.35924, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 45.35924, 1.0, 0.0)
    db.AddUnit(
        "mass", "US hundredweight", "cwtUS", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000000986923, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000000986923, 1.0, 0.0)
    db.AddUnit(
        "area", "darcy", "D", f_base_to_unit, f_unit_to_base, default_category="permeability rock"
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 86400, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 86400, 1.0, 0.0)
    db.AddUnit("time", "day", "d", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000000000003008141, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000000000003008141, 1.0, 0.0)
    db.AddUnit(
        "volume",
        "darcy foot",
        "D.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category="permeability length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000000986923, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000000986923, 1.0, 0.0)
    db.AddUnit(
        "volume",
        "darcy metre",
        "D.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="permeability length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 86400, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 86400, 0.1589873, 0.0)
    db.AddUnit(
        "time per volume",
        "day per barrel",
        "d/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 86400, 0.028316846592, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 86400, 0.028316846592, 0.0)
    db.AddUnit(
        "time per volume",
        "days/cubic foot",
        "d/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 86400, 28.316846592, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 86400, 28.316846592, 0.0)
    db.AddUnit(
        "time per volume",
        "day per thousand cubic feet",
        "d/Mcf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 86400, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 86400, 1.0, 0.0)
    db.AddUnit(
        "time per volume",
        "days/cubic metre",
        "d/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10, 1.0, 0.0)
    db.AddUnit("force", "decanewtons", "daN", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 10, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "decanewton metres",
        "daN.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "level of power intensity",
        "decibel",
        "dB",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 0.3048, 0.0)
    db.AddUnit(
        "attenuation per length",
        "decibels/foot",
        "dB/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "attenuation per length",
        "decibels/metre",
        "dB/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0001, 1.0, 0.0)
    db.AddUnit(
        "attenuation per length",
        "decibels/kilometre",
        "dB/km",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "attenuation",
        "decibels/octave",
        "dB/O",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "temperature",
        "change in degrees Celsius",
        "ddegC",
        f_base_to_unit,
        f_unit_to_base,
        default_category="delta temperature",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5, 9, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5, 9, 0.0)
    db.AddUnit(
        "temperature",
        "change in degrees Fahrenheit",
        "ddegF",
        f_base_to_unit,
        f_unit_to_base,
        default_category="delta temperature",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "temperature",
        "change in degrees Kelvin",
        "ddegK",
        f_base_to_unit,
        f_unit_to_base,
        default_category="delta temperature",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5, 9, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5, 9, 0.0)
    db.AddUnit(
        "temperature",
        "change in degrees Rankine",
        "ddegR",
        f_base_to_unit,
        f_unit_to_base,
        default_category="delta temperature",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01745329, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01745329, 1.0, 0.0)
    db.AddUnit(
        "plane angle",
        "degree of an angle",
        "dega",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01745329, 30.48, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01745329, 30.48, 0.0)
    db.AddUnit(
        "angle per length",
        "degrees of an angle/100 feet",
        "dega/100ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01745329, 9.144, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01745329, 9.144, 0.0)
    db.AddUnit(
        "angle per length",
        "degrees of an angle per thirty feet",
        "dega/30ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01745329, 30, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01745329, 30, 0.0)
    db.AddUnit(
        "angle per length",
        "degrees of an angle/30 metres",
        "dega/30m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01745329, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01745329, 0.3048, 0.0)
    db.AddUnit(
        "angle per length",
        "degrees of an angle/foot",
        "dega/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01745329, 30.48, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01745329, 30.48, 0.0)
    db.AddUnit(
        "angle per length",
        "degrees of an angle/100 feet",
        "dega/ft(100)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01745329, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01745329, 3600, 0.0)
    db.AddUnit(
        "frequency",
        "degrees of an angle per hour",
        "dega/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01745329, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01745329, 1.0, 0.0)
    db.AddUnit(
        "angle per length",
        "degrees of an angle/metre",
        "dega/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01745329, 30, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01745329, 30, 0.0)
    db.AddUnit(
        "angle per length",
        "degrees of an angle/30 metres",
        "dega/m(30)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01745329, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01745329, 60, 0.0)
    db.AddUnit(
        "frequency",
        "degrees of an angle/minute",
        "dega/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01745329, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01745329, 1.0, 0.0)
    db.AddUnit(
        "frequency",
        "degrees of an angle per second",
        "dega/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(273.15, 1, 1, 0)
    f_base_to_unit = MakeBaseToCustomary(273.15, 1, 1, 0)
    db.AddUnit(
        "temperature",
        "degrees Celsius",
        "degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.8604208, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.8604208, 1.0, 0.0)
    db.AddUnit(
        "thermal insulance",
        "degrees C square metres hours/kilocal",
        "degC.m2.h/kcal",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "temperature per length",
        "degrees Celsius per hundred metre",
        "degC/100m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.3048, 0.0)
    db.AddUnit(
        "temperature per length",
        "degrees Celsius per foot",
        "degC/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit(
        "temperature per time",
        "degrees Celsius per hour",
        "degC/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "temperature per length",
        "degrees Celsius/kilometre",
        "degC/km",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "temperature per length",
        "degrees Celsius/metre",
        "degC/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 60, 0.0)
    db.AddUnit(
        "temperature per time",
        "degrees Celsius per minute",
        "degC/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "temperature per time",
        "degrees Celsius per second",
        "degC/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(2298.35, 5, 9, 0)
    f_base_to_unit = MakeBaseToCustomary(2298.35, 5, 9, 0)
    db.AddUnit(
        "temperature",
        "degree Fahrenheit",
        "degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1761102, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1761102, 1.0, 0.0)
    db.AddUnit(
        "thermal insulance",
        "degrees F square feet hours/Btu",
        "degF.ft2.h/Btu",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01822689, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01822689, 1.0, 0.0)
    db.AddUnit(
        "temperature per length",
        "degrees Fahrenheit/100 feet.",
        "degF/100ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.822689, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.822689, 1.0, 0.0)
    db.AddUnit(
        "temperature per length",
        "degrees Fahrenheit/foot",
        "degF/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01822689, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01822689, 1.0, 0.0)
    db.AddUnit(
        "temperature per length",
        "degrees Fahrenheit/100 feet.",
        "degF/ft(100)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5, 32400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5, 32400, 0.0)
    db.AddUnit(
        "temperature per time",
        "degrees Fahrenheit per hour",
        "degF/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5, 9, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5, 9, 0.0)
    db.AddUnit(
        "temperature per length",
        "degrees Fahrenheit per meter",
        "degF/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5, 540, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5, 540, 0.0)
    db.AddUnit(
        "temperature per time",
        "degrees Fahrenheit per minute",
        "degF/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5, 9, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5, 9, 0.0)
    db.AddUnit(
        "temperature per time",
        "degrees Fahrenheit per second",
        "degF/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5, 9, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5, 9, 0.0)
    db.AddUnit(
        "temperature",
        "degrees Rankine",
        "degR",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit("length", "decimetre", "dm", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "decimeter per second",
        "dm/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "volume", "cubic decimetre", "dm3", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00000001, 1.0, 0.0)
    db.AddUnit(
        "area",
        "cubic decimetres/100 kilometres",
        "dm3/100km",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "cubic decimetres/kilogram",
        "dm3/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00000001, 1.0, 0.0)
    db.AddUnit(
        "area",
        "cubic decimetres/100 kilometres",
        "dm3/km(100)",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000000002777778, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000000002777778, 1.0, 0.0)
    db.AddUnit(
        "isothermal compressibility",
        "cubic decimetres/kilowatt hour",
        "dm3/kW.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "area",
        "cubic decimetres/metre",
        "dm3/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "cubic decimetres/cubic metre",
        "dm3/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "isothermal compressibility",
        "cubic decimetres/megajoule",
        "dm3/MJ",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "molar volume",
        "cubic decimetres/kilogram mole",
        "dm3/kmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "molar volume",
        "cubic decimetres/kilogram mole",
        "dm3/mol(kg)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic decimetres/second",
        "dm3/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "volume per time per time",
        "cubic decimetres/second/second",
        "dm3/s2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "cubic decimetres/ton",
        "dm3/t",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "decinewton metres",
        "dN.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00001, 1.0, 0.0)
    db.AddUnit("force", "dynes", "dyne", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "force area",
        "dyne centimetre squared",
        "dyne.cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "dyne seconds/square centimetre",
        "dyne.s/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="dynamic viscosity",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "force per length",
        "dynes/centimetre",
        "dyne/cm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "dynes/square centimetre",
        "dyne/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "parachor",
        "dynes/centimetre fourth/gram cm cubed",
        "(dyne/cm)4/gcm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "parachor",
        "newton/metre fourth/kilogram metre cubed",
        "(N/m)4/kg.m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 746, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 746, 1.0, 0.0)
    db.AddUnit(
        "power", "electric horsepower", "ehp", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1e018, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1e018, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "exajoule", "EJ", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 31687540000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 31687540000, 1.0, 0.0)
    db.AddUnit(
        "power",
        "exajoules/year",
        "EJ/a",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "equivalent per volume",
        "equivalents/ Liter",
        "eq/L",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000001, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "ergs", "erg", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000001, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000001, 31558150, 0.0)
    db.AddUnit(
        "power",
        "ergs/year",
        "erg/a",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "force per length",
        "ergs/square centimetre",
        "erg/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="energy per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "ergs/cubic centimetre",
        "erg/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0001, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "ergs/gram",
        "erg/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000001, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "ergs/kilogram",
        "erg/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000001, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "ergs/cubic metre",
        "erg/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.602177e-019, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.602177e-019, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "electron volts",
        "eV",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.8288, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.8288, 1.0, 0.0)
    db.AddUnit("length", "fathoms", "fathom", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1e-015, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1e-015, 1.0, 0.0)
    db.AddUnit(
        "electric capacity",
        "femtocoulomb",
        "fC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00002841308, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00002841308, 1.0, 0.0)
    db.AddUnit(
        "volume", "UK fluid ounce", "fl ozUK", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00002957353, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00002957353, 1.0, 0.0)
    db.AddUnit(
        "volume",
        "US fluid ounces",
        "fl ozUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "per time",
        "flops",
        "flops",
        f_base_to_unit,
        f_unit_to_base,
        default_category="operations per time",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00002841308, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00002841308, 1.0, 0.0)
    db.AddUnit(
        "volume", "UK fluid ounce", "flozUK", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00002957353, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00002957353, 1.0, 0.0)
    db.AddUnit(
        "volume", "US fluid ounces", "flozUS", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1e-015, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1e-015, 1.0, 0.0)
    db.AddUnit("length", "femtometer", "fm", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 10.76391, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10.76391, 1.0, 0.0)
    db.AddUnit(
        "illuminance",
        "footcandles",
        "footcandle",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10.76391, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10.76391, 1.0, 0.0)
    db.AddUnit(
        "light exposure",
        "footcandle seconds",
        "footcandle.s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.3048, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.3048, 1.0, 0.0)
    db.AddUnit("length", "foot", "ft", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.355818, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.355818, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "foot pounds force",
        "ft.lbf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.355818, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.355818, 0.1589873, 0.0)
    db.AddUnit(
        "normal stress",
        "foot pounds force/barrel",
        "ft.lbf/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 358.1692, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 358.1692, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "foot pounds force/US gallon",
        "ft.lbf/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.355818, 0.4535924, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.355818, 0.4535924, 0.0)
    db.AddUnit(
        "specific energy",
        "foot pounds force/pound mass",
        "ft.lbf/lbm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02259697, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02259697, 1.0, 0.0)
    db.AddUnit(
        "power",
        "foot pounds force/minute",
        "ft.lbf/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.355818, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.355818, 1.0, 0.0)
    db.AddUnit(
        "power",
        "foot pounds force/second",
        "ft.lbf/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1382549, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1382549, 1.0, 0.0)
    db.AddUnit(
        "mass length",
        "foot-pound mass",
        "ft.lbm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "feet per 100 feet",
        "ft/100ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.917134, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.917134, 1.0, 0.0)
    db.AddUnit(
        "per area",
        "feet/barrel",
        "ft/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="length per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.3048, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.3048, 86400, 0.0)
    db.AddUnit(
        "velocity", "feet/day", "ft/d", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.54864, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.54864, 1.0, 0.0)
    db.AddUnit(
        "length per temperature",
        "feet/degree Fahrenheit",
        "ft/degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "feet per feet",
        "ft/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10.76391, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10.76391, 1.0, 0.0)
    db.AddUnit(
        "per area",
        "feet/cubic foot",
        "ft/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="length per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 80.51964, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 80.51964, 1.0, 0.0)
    db.AddUnit(
        "per area",
        "feet/US gallon",
        "ft/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category="length per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.3048, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.3048, 3600, 0.0)
    db.AddUnit(
        "velocity", "feet/hour", "ft/h", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 12, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 12, 1.0, 0.0)
    db.AddUnit(
        "dimensionless", "feet/inch", "ft/in", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.3048, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.3048, 1.0, 0.0)
    db.AddUnit(
        "dimensionless", "feet/metre", "ft/m", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 5280, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 5280, 0.0)
    db.AddUnit(
        "dimensionless", "feet/mile", "ft/mi", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.3048, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.3048, 60, 0.0)
    db.AddUnit(
        "velocity", "feet/minute", "ft/min", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 304.8, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 304.8, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "foot per millisecond",
        "ft/ms",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.3048, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.3048, 1.0, 0.0)
    db.AddUnit(
        "velocity", "feet/second", "ft/s", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.3048, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.3048, 1.0, 0.0)
    db.AddUnit(
        "acceleration linear",
        "feet/second squared",
        "ft/s2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 304800, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 304800, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "foot per microsecond",
        "ft/us",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "meters per microsecond",
        "m/us",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.09290304, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.09290304, 1.0, 0.0)
    db.AddUnit("area", "square foot", "ft2", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.09290304, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.09290304, 3600, 0.0)
    db.AddUnit(
        "volume per time per length",
        "square feet/hour",
        "ft2/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5669.291, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5669.291, 1.0, 0.0)
    db.AddUnit(
        "per length",
        "square feet/cubic inch",
        "ft2/in3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="area per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.09290304, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.09290304, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "square feet/second",
        "ft2/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 1.0, 0.0)
    db.AddUnit("volume", "cubic feet", "ft3", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0011953, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0011953, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "cubic feet at standard conditions",
        "ft3(std,60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 0.1589873, 0.0)
    db.AddUnit(
        "dimensionless",
        "cubic feet/barrel",
        "ft3/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 86400, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic feet/day",
        "ft3/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.09290304, 5957067005, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.09290304, 5957067005, 0.0)
    db.AddUnit(
        "unit productivity index",
        "cubic feet/day foot psi",
        "ft3/d.ft.psi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 7464960000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 7464960000, 0.0)
    db.AddUnit(
        "volume per time per time",
        "cubic feet/day/day",
        "ft3/d2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.09290304, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.09290304, 1.0, 0.0)
    db.AddUnit(
        "area",
        "cubic feet/foot",
        "ft3/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "cubic feet/cubic foot",
        "ft3/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 3600, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic feet/hour",
        "ft3/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 12960000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 12960000, 0.0)
    db.AddUnit(
        "volume per time per time",
        "cubic feet/hour/hour",
        "ft3/h2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "cubic feet per kilogram",
        "ft3/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.06242796, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.06242796, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "cubic feet/pound mass",
        "ft3/lbm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 60, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic feet/minute",
        "ft3/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.3048, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.3048, 60, 0.0)
    db.AddUnit(
        "velocity",
        "cubic feet/min square foot",
        "ft3/min.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per time per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 3600, 0.0)
    db.AddUnit(
        "volume per time per time",
        "cubic feet/minute/minute",
        "ft3/min2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00006242796, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00006242796, 1.0, 0.0)
    db.AddUnit(
        "molar volume",
        "cubic feet/mole (pound mass)",
        "ft3/lbmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.06242796, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.06242796, 1.0, 0.0)
    db.AddUnit(
        "molar volume",
        "cubic feet/mole (pound mass)",
        "ft3/mol(lbm)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 1.0, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic feet/second",
        "ft3/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.3048, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.3048, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "cubic feet/second square foot",
        "ft3/s.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per time per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 1.0, 0.0)
    db.AddUnit(
        "volume per time per time",
        "cubic feet/second/second",
        "ft3/s2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 42.63769, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 42.63769, 0.0)
    db.AddUnit(
        "specific volume",
        "cubic feet per 94 pound sack",
        "ft3/sack94",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "volume per standard volume",
        "cubic feet/std cubic foot, 60 deg F",
        "ft3/scf(60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.9143992, 3, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.9143992, 3, 0.0)
    db.AddUnit(
        "length",
        "British Foot (Benoit 1895 A)",
        "ftBnA",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 12, 39.370113, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 12, 39.370113, 0.0)
    db.AddUnit(
        "length",
        "British Foot (Benoit 1895 B)",
        "ftBnB",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.9144025, 3, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.9144025, 3, 0.0)
    db.AddUnit(
        "length",
        "British Foot 1865",
        "ftBr(65)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.304797265, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.304797265, 1.0, 0.0)
    db.AddUnit(
        "length", "Imperial Foot", "ftCla", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6378300, 20926201, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6378300, 20926201, 0.0)
    db.AddUnit(
        "length", "Gold Coast Foot", "ftGC", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 12, 39.370142, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 12, 39.370142, 0.0)
    db.AddUnit(
        "length", "Indian Foot", "ftInd", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.30479841, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.30479841, 1.0, 0.0)
    db.AddUnit(
        "length",
        "Indian Foot, 1937",
        "ftInd(37)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.3047996, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.3047996, 1.0, 0.0)
    db.AddUnit(
        "length",
        "Indian Foot, 1962",
        "ftInd(62)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.3047995, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.3047995, 1.0, 0.0)
    db.AddUnit(
        "length",
        "Indian Foot, 1975",
        "ftInd(75)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.304812253, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.304812253, 1.0, 0.0)
    db.AddUnit(
        "length",
        "Modified American Foot",
        "ftMA",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 12, 39.370147, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 12, 39.370147, 0.0)
    db.AddUnit(
        "length", "Sears Foot", "ftSe", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 12, 39.37, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 12, 39.37, 0.0)
    db.AddUnit(
        "length", "US Survey Foot", "ftUS", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit("mass", "gram", "g", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0003048, 0.000001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0003048, 0.000001, 0.0)
    db.AddUnit(
        "mass per time per area",
        "gram feet/cubic centimetre second",
        "g.ft/cm3.s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "density",
        "grams/cubic centimetre",
        "g/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100000, 1.0, 0.0)
    db.AddUnit(
        "mass per volume per length",
        "grams/centimetre fourth",
        "g/cm4",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "density",
        "grams/cubic decimetre",
        "g/dm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.2199692, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.2199692, 1.0, 0.0)
    db.AddUnit(
        "density",
        "grams/UK gallon",
        "g/galUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.264172, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.264172, 1.0, 0.0)
    db.AddUnit(
        "density",
        "grams/US gallon",
        "g/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "grams/kilogram",
        "g/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mass concentration",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "density", "grams/litre", "g/L", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "density",
        "grams/cubic metre",
        "g/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "mass flow rate",
        "grams/second",
        "g/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3.155815e016, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3.155815e016, 1.0, 0.0)
    db.AddUnit("time", "gigayears", "Ga", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "acceleration linear",
        "galileo",
        "Gal",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.003785412, 42.63769, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.003785412, 42.63769, 0.0)
    db.AddUnit(
        "specific volume",
        "US gallons/94 lb sack",
        "gal/sack",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.004546092, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.004546092, 1.0, 0.0)
    db.AddUnit(
        "volume", "UK gallon", "galUK", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.004549092, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.004549092, 86400, 0.0)
    db.AddUnit(
        "volume flow rate",
        "UK gallons per day",
        "galUK/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1605437, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1605437, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "UK gallons/cubic foot",
        "galUK/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.004549092, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.004549092, 3600, 0.0)
    db.AddUnit(
        "volume flow rate",
        "UK gallons/hour",
        "galUK/hr",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000004143055, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000004143055, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "UK gallons/hour foot",
        "galUK/hr.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000135927, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000135927, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "UK gallons/hour square foot",
        "galUK/hr.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per time per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00004971667, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00004971667, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "UK gallons/hour inch",
        "galUK/hr.in",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001957349, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001957349, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "UK gallons/hour square inch",
        "galUK/hr.in2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per time per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.004546092, 12960000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.004546092, 12960000, 0.0)
    db.AddUnit(
        "volume per time per time",
        "UK gallons/hour/hour",
        "galUK/hr2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "UK gallons per thousand UK gallons",
        "galUK/kgalUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01002242, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01002242, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "UK gallons/pound mass",
        "galUK/lbm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00002859406, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00002859406, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "UK gallons/1000 barrels",
        "galUK/Mbbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.004546092, 1609.344, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.004546092, 1609.344, 0.0)
    db.AddUnit(
        "area",
        "UK gallons/mile",
        "galUK/mi",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.004549092, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.004549092, 60, 0.0)
    db.AddUnit(
        "volume flow rate",
        "UK gallons/minute",
        "galUK/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0002485333, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0002485333, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "UK gallons/minute foot",
        "galUK/min.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0008155621, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0008155621, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "UK gallons/minute square foot",
        "galUK/min.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per time per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.004546092, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.004546092, 3600, 0.0)
    db.AddUnit(
        "volume per time per time",
        "UK gallons/minute/minute",
        "galUK/min2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.003785412, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.003785412, 1.0, 0.0)
    db.AddUnit(
        "volume", "US gallons", "galUS", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.002380952381, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.002380952381, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "US gallons per ten barrels",
        "galUS/10bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02380952381, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02380952381, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "US gallons/barrels",
        "galUS/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.003785412, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.003785412, 86400, 0.0)
    db.AddUnit(
        "volume flow rate",
        "US gallons per day",
        "galUS/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.003785412, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.003785412, 0.3048, 0.0)
    db.AddUnit(
        "area",
        "US gallons/foot",
        "galUS/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1336806, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1336806, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "US gallons/cubic foot",
        "galUS/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.003785412, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.003785412, 3600, 0.0)
    db.AddUnit(
        "volume flow rate",
        "US gallons/hour",
        "galUS/hr",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000003449814, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000003449814, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "US gallons/foot hour",
        "galUS/hr.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00001131829, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00001131829, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "US gallons/hour square foot",
        "galUS/hr.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per time per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00004139776, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00004139776, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "US gallons/hour inch",
        "galUS/hr.in",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001629833, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001629833, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "US gallons/hour square inch",
        "galUS/hr.in2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per time per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.003785412, 12960000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.003785412, 12960000, 0.0)
    db.AddUnit(
        "volume per time per time",
        "US gallons/hour/hour",
        "galUS/hr2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "US gallons per thousand US gallons",
        "galUS/kgalUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.008345404, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.008345404, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "US gallons/pound mass",
        "galUS/lbm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00002380952, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00002380952, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "US gallons/1000 barrels",
        "galUS/Mbbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.003785412, 1609.344, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.003785412, 1609.344, 0.0)
    db.AddUnit(
        "area",
        "US gallons/mile",
        "galUS/mi",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.003785412, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.003785412, 60, 0.0)
    db.AddUnit(
        "volume flow rate",
        "US gallons/minute",
        "galUS/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0002069888, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0002069888, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "US gallons/minute foot",
        "galUS/min.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0006790972, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0006790972, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "US gallons/minute square foot",
        "galUS/min.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per time per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.003785412, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.003785412, 3600, 0.0)
    db.AddUnit(
        "volume per time per time",
        "US gallons/minute/minute",
        "galUS/min2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.003785412, 28.262357, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.003785412, 28.262357, 0.0)
    db.AddUnit(
        "volume per standard volume",
        "US gals/1000 std cubic feet, 60 deg F",
        "galUS/Mscf(60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.003785412, 42.63769, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.003785412, 42.63769, 0.0)
    db.AddUnit(
        "specific volume",
        "US gallons/94 lb sack",
        "galUS/sack94",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000003725627, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000003725627, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "US gallons/UK ton",
        "galUS/tonUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000004172702, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000004172702, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "US gallons/US ton",
        "galUS/tonUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0007957747, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0007957747, 1.0, 0.0)
    db.AddUnit(
        "magnetization", "gamma", "gamma", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0001, 1.0, 0.0)
    db.AddUnit(
        "magnetic induction",
        "gauss",
        "gauss",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "gigabecquerel",
        "GBq",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000160219, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000160219, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "billions of electron volts",
        "GeV",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00980665, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00980665, 1.0, 0.0)
    db.AddUnit("force", "gram force", "gf", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 6283185307, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6283185307, 1.0, 0.0)
    db.AddUnit(
        "frequency", "gigahertz", "GHz", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "gigajoule", "GJ", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 1.0, 0.0)
    db.AddUnit(
        "acceleration linear",
        "gravity",
        "gn",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000, 1.0, 0.0)
    db.AddUnit(
        "resistance", "gigaohm", "Gohm", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.015707963268, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.015707963268, 1.0, 0.0)
    db.AddUnit("plane angle", "gons", "gon", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000, 1.0, 0.0)
    db.AddUnit(
        "pressure", "gigapascal", "GPa", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100000000000, 1.0, 0.0)
    db.AddUnit(
        "pressure per length",
        "gigapascal per centimeter",
        "GPa/cm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1e018, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1e018, 1.0, 0.0)
    db.AddUnit(
        "pressure squared",
        "gigapascal squared",
        "GPa2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.015707963268, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.015707963268, 1.0, 0.0)
    db.AddUnit("plane angle", "grad", "gr", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000, 1.0, 0.0)
    db.AddUnit(
        "plane angle", "gigaradian", "Grad", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00006479891, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00006479891, 1.0, 0.0)
    db.AddUnit("mass", "grain", "grain", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00002288352, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00002288352, 1.0, 0.0)
    db.AddUnit(
        "density",
        "grains/100 cubic feet",
        "grain/100ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.002288352, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.002288352, 1.0, 0.0)
    db.AddUnit(
        "density",
        "grains/cubic foot",
        "grain/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00002288352, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00002288352, 1.0, 0.0)
    db.AddUnit(
        "density",
        "grains/100 cubic feet",
        "grain/ft3(100)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01711806, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01711806, 1.0, 0.0)
    db.AddUnit(
        "density",
        "grains/US gallon",
        "grain/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000, 1.0, 0.0)
    db.AddUnit(
        "electric conductance",
        "gigasiemens",
        "GS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "giga standard cubic metres 15C",
        "Gsm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000, 1.0, 0.0)
    db.AddUnit("power", "gigawatt", "GW", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600000000000, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "gigawatt hour",
        "GW.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600, 1.0, 0.0)
    db.AddUnit("time", "hour", "h", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600, 0.028316846592, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600, 0.028316846592, 0.0)
    db.AddUnit(
        "time per volume",
        "hours/cubic foot",
        "h/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600, 304.8, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600, 304.8, 0.0)
    db.AddUnit(
        "time per length",
        "hour per thousand foot",
        "h/kft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3.6, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3.6, 1.0, 0.0)
    db.AddUnit(
        "time per length",
        "hour per kilometer",
        "h/km",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600, 1.0, 0.0)
    db.AddUnit(
        "time per volume",
        "hour per cubic meter",
        "h/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10000, 1.0, 0.0)
    db.AddUnit("area", "hectare", "ha", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 10000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10000, 1.0, 0.0)
    db.AddUnit(
        "volume", "hectare metres", "ha.m", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10000000, 1.0, 0.0)
    db.AddUnit(
        "pressure", "hectobar", "hbar", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 746.043, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 746.043, 1.0, 0.0)
    db.AddUnit(
        "power",
        "hydraulic horsepower",
        "hhp",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 746.043, 0.00064516, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 746.043, 0.00064516, 0.0)
    db.AddUnit(
        "density of heat flow rate",
        "(hydraulic) horsepower per square inch",
        "hhp/in2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit("volume", "hectoliter", "hL", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 745.6999, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 745.6999, 1.0, 0.0)
    db.AddUnit("power", "horsepower", "hp", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 2684520, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2684520, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "horsepower hour",
        "hp.hr",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 2684520, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2684520, 0.1589873, 0.0)
    db.AddUnit(
        "normal stress",
        "horsepower hours/barrel",
        "hp.hr/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 2684520, 0.4535924, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2684520, 0.4535924, 0.0)
    db.AddUnit(
        "specific energy",
        "horsepower hours/pound mass",
        "hp.hr/lbm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 26334.14, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 26334.14, 1.0, 0.0)
    db.AddUnit(
        "power per volume",
        "horsepower/cubic foot",
        "hp/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 745.6999, 0.00064516, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 745.6999, 0.00064516, 0.0)
    db.AddUnit(
        "density of heat flow rate",
        "horsepower per square inch",
        "hp/in2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100, 1.0, 0.0)
    db.AddUnit(
        "time", "hundred seconds", "hs", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0254, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0254, 1.0, 0.0)
    db.AddUnit("length", "inch", "in", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00254, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00254, 1.0, 0.0)
    db.AddUnit(
        "length", "tenth of an inch", "in/10", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0015875, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0015875, 1.0, 0.0)
    db.AddUnit(
        "length", "16th of an inch", "in/16", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00079375, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00079375, 1.0, 0.0)
    db.AddUnit(
        "length", "32nd of an inch", "in/32", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000396875, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000396875, 1.0, 0.0)
    db.AddUnit(
        "length", "64th of an inch", "in/64", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0254, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0254, 31558150, 0.0)
    db.AddUnit(
        "velocity", "inches/year", "in/a", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.8, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.8, 1.0, 0.0)
    db.AddUnit(
        "volumetric thermal expansion",
        "inches/inch degree Fahrenheit",
        "in/in.degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category="linear thermal expansion",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0254, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0254, 60, 0.0)
    db.AddUnit(
        "velocity", "inches/minute", "in/min", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0254, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0254, 1.0, 0.0)
    db.AddUnit(
        "velocity", "inches/second", "in/s", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00064516, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00064516, 1.0, 0.0)
    db.AddUnit(
        "area", "square inches", "in2", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 144, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 144, 0.0)
    db.AddUnit(
        "dimensionless",
        "square inches/square foot",
        "in2/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "square inches/square inch",
        "in2/in2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00064516, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00064516, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "square inches/second",
        "in2/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00001638706, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00001638706, 1.0, 0.0)
    db.AddUnit(
        "volume", "cubic inches", "in3", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000016387064, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000016387064, 0.3048, 0.0)
    db.AddUnit(
        "area",
        "cubic inches/foot",
        "in3/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000004162314, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000004162314, 1.0, 0.0)
    db.AddUnit(
        "second moment of area",
        "inches to the fourth",
        "in4",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 249.082, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 249.082, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "inches of water at 39.2 deg F",
        "inH2O(39.2F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 248.84, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 248.84, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "inches of water at 60 deg F",
        "inH2O(60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3386.38, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3386.38, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "inches of mercury at 32 deg F",
        "inHg(32F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3376.85, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3376.85, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "inches of mercury at 60 deg F",
        "inHg(60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 39.37, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 39.37, 0.0)
    db.AddUnit(
        "length", "US Survey inch", "inUS", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10000, 1.0, 0.0)
    db.AddUnit(
        "force per length",
        "joules/square centimetre",
        "J/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="energy per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "joules/cubic decimetre",
        "J/dm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "joules/gram",
        "J/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "specific heat capacity",
        "joules/gram degree Kelvin",
        "J/g.K",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "force",
        "joules/metre",
        "J/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="energy per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "force per length",
        "joules/square metre",
        "J/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="energy per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "heat transfer coefficient",
        "joules/second square metre deg C",
        "J/s.m2.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "thermal insulance",
        "degrees Kelvin square metres/kilowatt",
        "K.m2/kW",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "electric current",
        "kiloampere",
        "kA",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158.9873, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158.9873, 86400, 0.0)
    db.AddUnit(
        "volume flow rate",
        "thousand barrels per day",
        "kbbl/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1024, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1024, 1.0, 0.0)
    db.AddUnit(
        "digital storage",
        "kilobyte",
        "kbyte",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "electric capacity",
        "kilocoulombs",
        "kC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "kilocalories",
        "kcal",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184, 0.0001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184, 0.0001, 0.0)
    db.AddUnit(
        "force",
        "kilocalorie metres/square centimetre",
        "kcal.m/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="energy length per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184, 0.000001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184, 0.000001, 0.0)
    db.AddUnit(
        "normal stress",
        "kilocalories/cubic centimetre",
        "kcal/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184, 0.001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184, 0.001, 0.0)
    db.AddUnit(
        "specific energy",
        "kilocalories/gram",
        "kcal/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.162222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.162222, 1.0, 0.0)
    db.AddUnit(
        "power",
        "kilocalories/hour",
        "kcal/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.162222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.162222, 1.0, 0.0)
    db.AddUnit(
        "thermal conductivity",
        "kilocalories/hour metre degree Celsius",
        "kcal/h.m.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001162222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001162222, 1.0, 0.0)
    db.AddUnit(
        "thermal conductivity",
        "calories/metre hour degree Celsius",
        "cal/m.h.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.162222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.162222, 1.0, 0.0)
    db.AddUnit(
        "heat transfer coefficient",
        "kilocalorie/hour square metre deg C",
        "kcal/h.m2.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001162222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001162222, 1.0, 0.0)
    db.AddUnit(
        "heat transfer coefficient",
        "calorie/hour square metre deg C",
        "cal/h.m2.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "kilocalories/kilogram",
        "kcal/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184, 1.0, 0.0)
    db.AddUnit(
        "specific heat capacity",
        "kilocalories/kilogram degree Celsius",
        "kcal/kg.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "kilocalroies/cubic metre",
        "kcal/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184, 1.0, 0.0)
    db.AddUnit(
        "molar thermodynamic energy",
        "kilocalories/mole (gram)",
        "kcal/mol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4184000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4184000, 1.0, 0.0)
    db.AddUnit(
        "molar thermodynamic energy",
        "kilocalories/mole (gram)",
        "kcal/mol(g)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "luminous intensity",
        "kilocandela",
        "kcd",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit("force", "kilodynes", "kdyne", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "per time",
        "thousand per second",
        "kEuc/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.60217733e-016, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.60217733e-016, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "kiloelectron volts",
        "keV",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1355.818, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1355.818, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "thousand foot pounds force",
        "kft.lbf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 304.8, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 304.8, 3600, 0.0)
    db.AddUnit(
        "velocity",
        "thousand feet per hour",
        "kft/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 304.8, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 304.8, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "thousand feet per second",
        "kft/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10000, 1.0, 0.0)
    db.AddUnit(
        "linear density",
        "kilogram metres/square centimetre",
        "kg.m/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mass per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400, 0.0)
    db.AddUnit(
        "mass flow rate",
        "kilogram per day",
        "kg/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "density",
        "kilograms/cubic decimetre",
        "kg/dm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10000, 1.0, 0.0)
    db.AddUnit(
        "mass per volume per length",
        "kilograms/decimetre fourth",
        "kg/dm4",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit(
        "mass flow rate",
        "kilograms/hour",
        "kg/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "kilograms/kilogram",
        "kg/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mass concentration",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600000, 0.0)
    db.AddUnit(
        "mass per energy",
        "kilograms/kilowatt hour",
        "kg/kW.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit(
        "mass per energy",
        "tonne/kilowatt hour",
        "t/kW.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "density",
        "kilogram per litre",
        "kg/L",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "kilograms/metre second",
        "kg/m.s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 60, 0.0)
    db.AddUnit(
        "mass flow rate",
        "kilogram per min",
        "kg/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "mass per energy",
        "kilograms/megajoule",
        "kg/MJ",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 42.63769, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 42.63769, 0.0)
    db.AddUnit(
        "dimensionless",
        "kilogram per 94 pound sack",
        "kg/sack94",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mass concentration",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 1.0, 0.0)
    db.AddUnit(
        "force", "kilogram force", "kgf", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "kilogram force metres",
        "kgf.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 98066.5, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 98066.5, 1.0, 0.0)
    db.AddUnit(
        "force per length",
        "kilogram force metres/square centimetre",
        "kgf.m/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="energy per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 1.0, 0.0)
    db.AddUnit(
        "force",
        "kilograms force metres/metre",
        "kgf.m/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="force length per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 1.0, 0.0)
    db.AddUnit(
        "force area",
        "kilogram force metres squared",
        "kgf.m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "kilograms force seconds/square metre",
        "kgf.s/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="dynamic viscosity",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 0.01, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 0.01, 0.0)
    db.AddUnit(
        "force per length",
        "kilograms force/centimetre",
        "kgf/cm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 0.0001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 0.0001, 0.0)
    db.AddUnit(
        "pressure",
        "kilogram per square centimeter",
        "kgf/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(101325, 98066.5, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(101325, 98066.5, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "kilogram per square centimeter gauge",
        "kgf/cm2(g)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "kilogram force per kilogram force",
        "kgf/kgf",
        f_base_to_unit,
        f_unit_to_base,
        default_category="force per force",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 0.000001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 0.000001, 0.0)
    db.AddUnit(
        "pressure",
        "kilogram force/square millimetre",
        "kgf/mm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6283.185307, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6283.185307, 1.0, 0.0)
    db.AddUnit(
        "frequency", "kilohertz", "kHz", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "kilojoules", "kJ", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3.6, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3.6, 0.0)
    db.AddUnit(
        "thermal conductivity",
        "kilojoule metres/hour sq metre deg K",
        "kJ.m/h.m2.K",
        f_base_to_unit,
        f_unit_to_base,
        default_category="energy length per time area temperature",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "kilojoules/cubic decimetre",
        "kJ/dm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 3600, 0.0)
    db.AddUnit(
        "heat transfer coefficient",
        "kilojoules/hour square metre deg K",
        "kJ/h.m2.K",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "kilojoule/kilogram",
        "kJ/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "specific heat capacity",
        "kilojoules/kilogram degree Kelvin",
        "kJ/kg.K",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "kilojoule/cubic metre",
        "kJ/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0, 0.0)
    db.AddUnit(
        "molar thermodynamic energy",
        "kilojoule/mole (kilogram)",
        "kJ/kmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "molar thermodynamic energy",
        "kilojoule/mole (kilogram)",
        "kJ/mol(kg)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "molar thermodynamic energy",
        "kilojoule/mole (kilogram)",
        "kJ/mol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0, 0.0)
    db.AddUnit(
        "molar heat capacity",
        "kilojoules/mole (kilogram) deg K",
        "kJ/kmol.K",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "molar heat capacity",
        "kilojoules/mole (kilogram) deg K",
        "kJ/mol(kg).K",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4448.222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4448.222, 1.0, 0.0)
    db.AddUnit(
        "force",
        "thousand pounds force",
        "klbf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 453.5924, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 453.5924, 1.0, 0.0)
    db.AddUnit(
        "mass",
        "thousand pounds mass",
        "klbm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 453.5924, 0.0254, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 453.5924, 0.0254, 0.0)
    db.AddUnit(
        "linear density",
        "thousand pounds mass per inch",
        "klbm/in",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "illuminance", "kilolux", "klx", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit("length", "kilometre", "km", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 100000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100000, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "kilometre/ centimetre",
        "km/cm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "per area",
        "kilometres/cubic decimetre",
        "km/dm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="length per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3.6, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3.6, 0.0)
    db.AddUnit(
        "velocity", "kilometres/hour", "km/h", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "per area",
        "kilometres/litre",
        "km/L",
        f_base_to_unit,
        f_unit_to_base,
        default_category="length per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "kilometer per second",
        "km/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "area", "square kilometres", "km2", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000, 1.0, 0.0)
    db.AddUnit(
        "volume", "cubic kilometres", "km3", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "molar mass",
        "kilomole",
        "kmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category="amount of substance",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit("force", "kilonewtons", "kN", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "kilonewton metres",
        "kN.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "force area",
        "kilonewton metres squared",
        "kN.m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "force per length",
        "kilonewtons/metre",
        "kN/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "kilonewtons/square metre",
        "kN/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1852, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1852, 3600, 0.0)
    db.AddUnit("velocity", "knots", "knot", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "resistance", "kilohm", "kohm", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "electrical resistivity",
        "kilo ohm metre",
        "kohm.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "pressure", "kilopascals", "kPa", f_base_to_unit, f_unit_to_base, default_category=None
    )

    f_unit_to_base = MakeCustomaryToBase(101325, 1000, 1, 0)
    f_base_to_unit = MakeBaseToCustomary(101325, 1000, 1, 0)
    db.AddUnit(
        "pressure",
        "kilopascals gauge",
        "kPa(g)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "mass per time per area",
        "kilopascal seconds/metre",
        "kPa.s/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10, 1.0, 0.0)
    db.AddUnit(
        "pressure per length",
        "kilopascal per hundred meter",
        "kPa/100m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 3600, 0.0)
    db.AddUnit(
        "pressure per time",
        "kilopascal per hour",
        "kPa/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "pressure per length",
        "kilopascals/metre",
        "kPa/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 60, 0.0)
    db.AddUnit(
        "pressure per time",
        "kilopascal per min",
        "kPa/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "pressure squared",
        "kilopascal squared",
        "kPa2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000, 1.0, 0.0)
    db.AddUnit(
        "pressure per time",
        "kilopascal squared per centipoise",
        "kPa2/cP",
        f_base_to_unit,
        f_unit_to_base,
        default_category="pressure squared per (dynamic viscosity)",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "pressure per time",
        "kilopascal squared per thousand centipoise",
        "kPa2/kcP",
        f_base_to_unit,
        f_unit_to_base,
        default_category="pressure squared per (dynamic viscosity)",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894757, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894757, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "thousand pounds per square inch",
        "kpsi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 47537674000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 47537674000000, 1.0, 0.0)
    db.AddUnit(
        "pressure squared",
        "thousand pound per square inch, squared",
        "kpsi2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "plane angle", "kiloradian", "krad", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "electric conductance",
        "kilosiemens",
        "kS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "kilo standard cubic metres 15C",
        "ksm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "thousand std cubic metres/ day",
        "ksm3/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "1000 std cubic metres/ std cubic metre",
        "ksm3/sm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "electric potential",
        "kilovolt",
        "kV",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit("power", "kilowatts", "kW", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600000, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "kilowatt hours",
        "kW.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600000, 0.001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600000, 0.001, 0.0)
    db.AddUnit(
        "normal stress",
        "kilowatt hours/decimetre",
        "kW.h/dm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600000, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "kilowatt hours/kilogram",
        "kW.h/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600000, 1.0, 0.0)
    db.AddUnit(
        "specific heat capacity",
        "kilowatt hours/kilogram degree C",
        "kW.h/kg.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600000, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "kilowatt hours/cubic metres",
        "kW.h/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10000000, 1.0, 0.0)
    db.AddUnit(
        "density of heat flow rate",
        "kilowatts/square centimetre",
        "kW/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "density of heat flow rate",
        "kilowatts/square metre",
        "kW/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "heat transfer coefficient",
        "kilowatts/square metre degree Kelvin",
        "kW/m2.K",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "power per volume",
        "kilowatts/cubic metre",
        "kW/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "volumetric heat transfer coefficient",
        "kilowatts/cubic metre degree Kelvin",
        "kW/m3.K",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit("volume", "litre", "L", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00001, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "liter per hundred kilogram",
        "L/100kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "area",
        "litres/100 kilometres",
        "L/100km",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.589873, 0.0)
    db.AddUnit(
        "dimensionless",
        "liter per ten barrel",
        "L/10bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 6000000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 6000000, 0.0)
    db.AddUnit(
        "productivity index",
        "litres per minute per bar",
        "L/bar.min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 3600, 0.0)
    db.AddUnit(
        "volume flow rate",
        "liter per hour",
        "L/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "liter per kilogram",
        "L/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "area",
        "litres/100 kilometres",
        "L/km(100)",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "area",
        "litres/metre",
        "L/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "litres/cubic metre",
        "L/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 60, 0.0)
    db.AddUnit(
        "volume flow rate",
        "liter per minute",
        "L/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "molar volume",
        "litres/mole (gram)",
        "L/mol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "molar volume",
        "litres/mole (gram)",
        "L/mol(g)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "molar volume",
        "litres/mole (kilogram)",
        "L/kmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "molar volume",
        "litres/mole (kilogram)",
        "L/mol(kg)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "volume flow rate",
        "litres/second",
        "L/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "volume per time per time",
        "litres/second/second",
        "L/s2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "litres/tonne",
        "L/t",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1016.047, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1016.047, 0.0)
    db.AddUnit(
        "specific volume",
        "liter per UK ton",
        "L/tonUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.448222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.448222, 1.0, 0.0)
    db.AddUnit(
        "force", "pounds force", "lbf", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.355818, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.355818, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "foot pounds force",
        "lbf.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.355818, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.355818, 0.1589873, 0.0)
    db.AddUnit(
        "normal stress",
        "foot pounds force/barrel",
        "lbf.ft/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.355818, 0.0254, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.355818, 0.0254, 0.0)
    db.AddUnit(
        "force",
        "pounds force feet/inch",
        "lbf.ft/in",
        f_base_to_unit,
        f_unit_to_base,
        default_category="force length per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 2101.522, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2101.522, 1.0, 0.0)
    db.AddUnit(
        "force per length",
        "foot pounds force/square inch",
        "lbf.ft/in2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="energy per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.355818, 0.4535924, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.355818, 0.4535924, 0.0)
    db.AddUnit(
        "specific energy",
        "foot pounds force/pound mass",
        "lbf.ft/lbm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1129848, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1129848, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "inch pounds force",
        "lbf.in",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.448222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.448222, 1.0, 0.0)
    db.AddUnit(
        "force",
        "pounds force inches/inch",
        "lbf.in/in",
        f_base_to_unit,
        f_unit_to_base,
        default_category="force length per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.002869815, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.002869815, 1.0, 0.0)
    db.AddUnit(
        "force area",
        "pounds force inches squared",
        "lbf.in2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 47.88026, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 47.88026, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "pounds force seconds/square foot",
        "lbf.s/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="dynamic viscosity",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "pounds force seconds/square inch",
        "lbf.s/in2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="dynamic viscosity",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.448222, 30.48, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.448222, 30.48, 0.0)
    db.AddUnit(
        "force per length",
        "pounds force per hundred foot",
        "lbf/100ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4788026, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4788026, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "pounds force/100 square foot",
        "lbf/100ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.448222, 30, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.448222, 30, 0.0)
    db.AddUnit(
        "force per length",
        "pounds force per thirty meters",
        "lbf/30m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.448222, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.448222, 0.3048, 0.0)
    db.AddUnit(
        "force per length",
        "pounds force per foot",
        "lbf/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 47.88026, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 47.88026, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "pounds force/square foot",
        "lbf/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4788026, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4788026, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "pounds force/100 square foot",
        "lbf/ft2(100)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.448222, 0.02831685, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.448222, 0.02831685, 0.0)
    db.AddUnit(
        "force per volume",
        "pounds force/cubic foot",
        "lbf/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.448222, 0.003785412, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.448222, 0.003785412, 0.0)
    db.AddUnit(
        "force per volume",
        "pounds force/US gallon",
        "lbf/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.448222, 0.0254, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.448222, 0.0254, 0.0)
    db.AddUnit(
        "force per length",
        "pounds force/inch",
        "lbf/in",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "pounds force/square inch",
        "lbf/in2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "pound force per pound force",
        "lbf/lbf",
        f_base_to_unit,
        f_unit_to_base,
        default_category="force per force",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 1.0, 0.0)
    db.AddUnit("mass", "pounds mass", "lbm", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.138255, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.138255, 1.0, 0.0)
    db.AddUnit(
        "momentum",
        "foot pounds mass/second",
        "lbm.ft/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.04214011, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.04214011, 1.0, 0.0)
    db.AddUnit(
        "moment of inertia",
        "pounds mass square feet",
        "lbm.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.04214011, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.04214011, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "pounds mass square feet/second squared",
        "lbm.ft2/s2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 453592.4, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 453592.4, 31558150, 0.0)
    db.AddUnit(
        "mass flow rate",
        "million pounds mass/year",
        "lbm(million)/yr",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 99.77633, 1000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 99.77633, 1000, 0.0)
    db.AddUnit(
        "density",
        "pounds mass/1000 UK gallons",
        "lbm/1000galUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 119.8264, 1000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 119.8264, 1000, 0.0)
    db.AddUnit(
        "density",
        "pounds mass/1000 US gallons",
        "lbm/1000galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.882428, 100, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.882428, 100, 0.0)
    db.AddUnit(
        "surface density",
        "pounds mass per hundred square foot",
        "lbm/100ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 1.589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 1.589873, 0.0)
    db.AddUnit(
        "density",
        "pounds mass per 10 barrel",
        "lbm/10bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 0.1589873, 0.0)
    db.AddUnit(
        "density",
        "pounds mass/barrel",
        "lbm/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 86400, 0.0)
    db.AddUnit(
        "mass flow rate",
        "pound mass per day",
        "lbm/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 0.3048, 0.0)
    db.AddUnit(
        "linear density",
        "pounds mass/foot",
        "lbm/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0004133789, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0004133789, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "pounds mass/foot hour",
        "lbm/ft.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.488164, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.488164, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "pounds mass/foot second",
        "lbm/ft.s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.882428, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.882428, 1.0, 0.0)
    db.AddUnit(
        "surface density",
        "pounds mass/square foot",
        "lbm/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 16.01846, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 16.01846, 1.0, 0.0)
    db.AddUnit(
        "density",
        "pounds mass/cubic foot",
        "lbm/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 16.01846, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 16.01846, 0.3048, 0.0)
    db.AddUnit(
        "mass per volume per length",
        "pounds mass/foot fourth",
        "lbm/ft4",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 99.77633, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 99.77633, 1.0, 0.0)
    db.AddUnit(
        "density",
        "pounds mass/UK gallon",
        "lbm/galUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 99.77633, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 99.77633, 0.3048, 0.0)
    db.AddUnit(
        "mass per volume per length",
        "pounds mass/UK gallon foot",
        "lbm/galUK.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 99.77633, 1000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 99.77633, 1000, 0.0)
    db.AddUnit(
        "density",
        "pounds mass/1000 UK gallons",
        "lbm/galUK(1000)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 119.8264, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 119.8264, 1.0, 0.0)
    db.AddUnit(
        "density",
        "pounds mass/US gallon",
        "lbm/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 119.8264, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 119.8264, 0.3048, 0.0)
    db.AddUnit(
        "mass per volume per length",
        "pounds mass/US gallon foot",
        "lbm/galUS.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 119.8264, 1000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 119.8264, 1000, 0.0)
    db.AddUnit(
        "density",
        "pounds mass/1000 US gallons",
        "lbm/galUS(1000)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 3600, 0.0)
    db.AddUnit(
        "mass flow rate",
        "pounds mass/hour",
        "lbm/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0004133789, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0004133789, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "pounds mass/hour foot",
        "lbm/h.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00135623, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00135623, 1.0, 0.0)
    db.AddUnit(
        "mass per time per area",
        "pounds mass/hour square foot",
        "lbm/h.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000001689659, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000001689659, 1.0, 0.0)
    db.AddUnit(
        "mass per energy",
        "pounds mass/horsepower hour",
        "lbm/hp.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 0.000016387064, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 0.000016387064, 0.0)
    db.AddUnit(
        "density",
        "pounds mass/cubic inch",
        "lbm/in3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00285301, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00285301, 1.0, 0.0)
    db.AddUnit(
        "density",
        "pounds mass/1000 barrels",
        "lbm/Mbbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 60, 0.0)
    db.AddUnit(
        "mass flow rate",
        "pounds mass/minute",
        "lbm/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 1.0, 0.0)
    db.AddUnit(
        "mass flow rate",
        "pounds mass/second",
        "lbm/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.488164, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.488164, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "pounds mass/second foot",
        "lbm/s.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.882428, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.882428, 1.0, 0.0)
    db.AddUnit(
        "mass per time per area",
        "pounds mass/second square foot",
        "lbm/s.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.201167824, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.201167824, 1.0, 0.0)
    db.AddUnit(
        "length",
        "British link 1895 A",
        "lkBnA",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 7.92, 39.370113, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 7.92, 39.370113, 0.0)
    db.AddUnit(
        "length",
        "British link 1895 B",
        "lkBnB",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 7.92, 39.370432, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 7.92, 39.370432, 0.0)
    db.AddUnit(
        "length", "Clarke link", "lkCla", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 7.92, 39.370147, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 7.92, 39.370147, 0.0)
    db.AddUnit(
        "length", "Sears link", "lkSe", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 7.92, 39.37, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 7.92, 39.37, 0.0)
    db.AddUnit(
        "length", "US Survey link", "lkUS", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "illuminance",
        "lumens/square metre",
        "lm/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="luminous exitance",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28316.846592, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28316.846592, 1.0, 0.0)
    db.AddUnit(
        "volume",
        "million cubic feet",
        "MMcf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 43560, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 43560, 0.0)
    db.AddUnit(
        "dimensionless",
        "million cubic feet per acre-foot",
        "MMcf/acre.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28316.85, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28316.85, 86400, 0.0)
    db.AddUnit(
        "volume flow rate",
        "million cubic feet per day",
        "MMcf/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "volume",
        "million cubic meters",
        "MMm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 86400, 0.0)
    db.AddUnit(
        "volume flow rate",
        "million cubic metres per day",
        "MMm3/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 30, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 30, 0.0)
    db.AddUnit(
        "dimensionless",
        "metres per thirty metres",
        "m/30m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "metres/ centimetre",
        "m/cm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400, 0.0)
    db.AddUnit(
        "velocity", "metres/day", "m/d", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit(
        "velocity", "metres/hour", "m/h", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "metres/kilometre",
        "m/km",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "metres/metre",
        "m/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "volumetric thermal expansion",
        "metres/metre Kelvin",
        "m/m.K",
        f_base_to_unit,
        f_unit_to_base,
        default_category="linear thermal expansion",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "per area",
        "metres/cubic metre",
        "m/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="length per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 60, 0.0)
    db.AddUnit(
        "velocity",
        "meter per minute",
        "m/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "metres/millisecond",
        "m/ms",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "per length",
        "square metres/cubic centimetre",
        "m2/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="area per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400000, 0.0)
    db.AddUnit(
        "unit productivity index",
        "square metres/day kiloPascal",
        "m2/d.kPa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "mass attenuation coefficient",
        "square metres/gram",
        "m2/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit(
        "volume per time per length",
        "square metres/hour",
        "m2/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "square metres/square metre",
        "m2/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "per length",
        "square metres/cubic metre",
        "m2/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="area per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0446158, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0446158, 1.0, 0.0)
    db.AddUnit(
        "molar mass",
        "cubic metres at std condition (0 deg C)",
        "m3(std,0C)",
        f_base_to_unit,
        f_unit_to_base,
        default_category="amount of substance",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0422932, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0422932, 1.0, 0.0)
    db.AddUnit(
        "molar mass",
        "cubic metres at std condition (15 deg C)",
        "m3(std,15C)",
        f_base_to_unit,
        f_unit_to_base,
        default_category="amount of substance",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 8640000000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 8640000000, 0.0)
    db.AddUnit(
        "productivity index",
        "cubic meter per day per bar",
        "m3/bar.d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 360000000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 360000000, 0.0)
    db.AddUnit(
        "productivity index",
        "cubic meter per hour per bar",
        "m3/bar.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 6000000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 6000000, 0.0)
    db.AddUnit(
        "productivity index",
        "cubic meter per minute per bar",
        "m3/bar.min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.1802270983e-10, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.1802270983e-10, 1.0, 0.0)
    db.AddUnit(
        "productivity index",
        "cubic meter per day per kilogram-force per square centimeter",
        "m3/d/kgf/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400, 0.0)
    db.AddUnit(
        "specific productivity index",
        "cubic metres/centiPoise day kiloPascal",
        "m3/cP.d.kPa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "specific productivity index",
        "cubic metres/centiPoise Pascal second",
        "m3/cP.Pa.s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic metres/day",
        "m3/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400000, 0.0)
    db.AddUnit(
        "productivity index",
        "cubic metres/day kilopascal",
        "m3/d.kPa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400, 0.0)
    db.AddUnit(
        "volume per time per length",
        "cubic meter per day per meter",
        "m3/d.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 7464960000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 7464960000, 0.0)
    db.AddUnit(
        "volume per time per time",
        "cubic metres/day/day",
        "m3/d2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "cubic metres/gram",
        "m3/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic metres/hour",
        "m3/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit(
        "volume per time per length",
        "cubic meter per hour per meter",
        "m3/h.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "cubic metres/hectare metre",
        "m3/ha.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "area",
        "cubic metres/kilometre",
        "m3/km",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400000, 0.0)
    db.AddUnit(
        "productivity index",
        "cubic meter per day per kilopascal",
        "m3/kPa.d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600000, 0.0)
    db.AddUnit(
        "productivity index",
        "(cubic metres per hour) per kilopascal",
        "m3/kPa.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600000, 0.0)
    db.AddUnit(
        "isothermal compressibility",
        "cubic metres/kilowatt hour",
        "m3/kW.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "area",
        "cubic metres/metre",
        "m3/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "length",
        "cubic meter per square meter",
        "m3/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "cubic metres/cubic metre",
        "m3/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 60, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic meter per minute",
        "m3/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "molar volume",
        "cubic metres/mole (kilogram)",
        "m3/kmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "molar volume",
        "cubic metres/mole (kilogram)",
        "m3/mol(kg)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 595707004.8, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 595707004.8, 0.0)
    db.AddUnit(
        "productivity index",
        "cubic meter per day per (pound per square inch)",
        "m3/psi.d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.3048, 0.0)
    db.AddUnit(
        "volume per time per length",
        "cubic meter per second per foot",
        "m3/s.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "cubic metres/second metre",
        "m3/s.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "cubic metres/second square metre",
        "m3/s.m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per time per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "cubic metres/tonne",
        "m3/t",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1016.047, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1016.047, 0.0)
    db.AddUnit(
        "specific volume",
        "cubic meters per UK ton",
        "m3/tonUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 907.1847, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 907.1847, 0.0)
    db.AddUnit(
        "specific volume",
        "cubic meters per US ton",
        "m3/tonUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "electric current", "milliamp", "mA", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 31558150000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 31558150000000, 1.0, 0.0)
    db.AddUnit("time", "megayears", "Ma", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "electric current",
        "megaampere",
        "MA",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10, 1.0, 0.0)
    db.AddUnit(
        "current density",
        "milliampere per square centimeter",
        "mA/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 0.09290304, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 0.09290304, 0.0)
    db.AddUnit(
        "current density",
        "milliampere per square foot",
        "mA/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100, 1.0, 0.0)
    db.AddUnit(
        "pressure", "millibar", "mbar", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158.9873, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158.9873, 1.0, 0.0)
    db.AddUnit(
        "volume", "thousand barrels", "Mbbl", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 48.45933, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 48.45933, 86400, 0.0)
    db.AddUnit(
        "volume length per time",
        "thousand barrel feet/day",
        "Mbbl.ft/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158.9873, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158.9873, 86400, 0.0)
    db.AddUnit(
        "volume flow rate",
        "thousand barrels/day",
        "Mbbl/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "megabecquerel",
        "MBq",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 293071.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 293071.1, 1.0, 0.0)
    db.AddUnit(
        "power",
        "million Btus/hour",
        "MBtu/hr",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1048576, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1048576, 1.0, 0.0)
    db.AddUnit(
        "digital storage",
        "megabyte",
        "Mbyte",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "electric capacity",
        "millicoulomb",
        "mC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "electric polarization",
        "millicoulombs/square metre",
        "mC/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 37000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 37000000, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "None",
        "mCi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 37000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 37000, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "millicurie",
        "mcurie",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.86923e-016, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.86923e-016, 1.0, 0.0)
    db.AddUnit(
        "area",
        "millidarcy",
        "mD",
        f_base_to_unit,
        f_unit_to_base,
        default_category="permeability rock",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3.008141e-016, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3.008141e-016, 1.0, 0.0)
    db.AddUnit(
        "volume",
        "millidarcy foot",
        "mD.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category="permeability length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.86932e-016, 47.88026, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.86932e-016, 47.88026, 0.0)
    db.AddUnit(
        "unit productivity index",
        "millidarcy sq feet/pound force second",
        "mD.ft2/lbf.s",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mobility",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.86932e-016, 6894.757, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.86932e-016, 6894.757, 0.0)
    db.AddUnit(
        "unit productivity index",
        "millidarcy sq inches/pound force second",
        "mD.in2/lbf.s",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mobility",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.86932e-016, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.86932e-016, 1.0, 0.0)
    db.AddUnit(
        "volume",
        "millidarcy metres",
        "mD.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="permeability length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.86932e-016, 0.001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.86932e-016, 0.001, 0.0)
    db.AddUnit(
        "unit productivity index",
        "millidarcies/centipoise",
        "mD/cP",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mobility",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.86932e-016, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.86932e-016, 1.0, 0.0)
    db.AddUnit(
        "unit productivity index",
        "millidarcies/Pascal second",
        "mD/Pa.s",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mobility",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "electrochemical equivalent",
        "milliequivalent",
        "meq",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100, 1.0, 0.0)
    db.AddUnit(
        "equivalent per mass",
        "milliequivalents/ hectogram",
        "meq/100g",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "equivalent per volume",
        "milliequivalents/ cubic centimeter",
        "meq/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "equivalent per mass",
        "milliequivalents/ gram",
        "meq/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "milliEuclid",
        "mEuc",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000000160219, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000000160219, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "millions of electron volts",
        "MeV",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "per time",
        "megaflops",
        "Mflops",
        f_base_to_unit,
        f_unit_to_base,
        default_category="operations per time",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit("mass", "megagram", "Mg", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit("mass", "milligram", "mg", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 31558150, 0.0)
    db.AddUnit(
        "mass flow rate",
        "megagrams/year",
        "Mg/a",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 86400, 0.0)
    db.AddUnit(
        "mass flow rate",
        "megagrams/day",
        "Mg/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "density",
        "milligrams/cubic decimetre",
        "mg/dm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000264172, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000264172, 1.0, 0.0)
    db.AddUnit(
        "density",
        "milligrams/US gallon",
        "mg/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3.6, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3.6, 0.0)
    db.AddUnit(
        "mass flow rate",
        "megagrams/hour",
        "Mg/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 0.0254, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 0.0254, 0.0)
    db.AddUnit(
        "linear density",
        "thousand kilograms per inch",
        "Mg/in",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "mass per energy",
        "milligrams/joule",
        "mg/J",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "milligrams/kilogram",
        "mg/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mass concentration",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "density",
        "milligram per litre",
        "mg/L",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "surface density",
        "megagrams/square metre",
        "Mg/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "density",
        "milligrams/cubic metre",
        "mg/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "density",
        "thousand kilograms per cubic metre",
        "Mg/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00001, 1.0, 0.0)
    db.AddUnit(
        "acceleration linear",
        "milligalileo",
        "mGal",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000001, 1.0, 0.0)
    db.AddUnit(
        "magnetic induction",
        "milligauss",
        "mgauss",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.000014, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.000014, 1.0, 0.0)
    db.AddUnit(
        "length",
        "German legal metre",
        "mGer",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4448222, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4448222, 1.0, 0.0)
    db.AddUnit(
        "force",
        "thousand kilograms force",
        "Mgf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00980665, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00980665, 1.0, 0.0)
    db.AddUnit(
        "acceleration linear",
        "milligravity",
        "mgn",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "absorbed dose", "milligray", "mGy", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "self inductance",
        "millihenries",
        "mH",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "electric conductance", "mhos", "mho", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "conductivity", "mhos/metre", "mho/m", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6283185.307, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6283185.307, 1.0, 0.0)
    db.AddUnit(
        "frequency", "megahertz", "MHz", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.006283185307, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.006283185307, 1.0, 0.0)
    db.AddUnit(
        "frequency", "millihertz", "mHz", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1609.344, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1609.344, 1.0, 0.0)
    db.AddUnit("length", "mile", "mi", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1609.344, 0.004546092, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1609.344, 0.004546092, 0.0)
    db.AddUnit(
        "per area",
        "miles/UK gallon",
        "mi/galUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category="length per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1609.344, 0.003785412, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1609.344, 0.003785412, 0.0)
    db.AddUnit(
        "per area",
        "miles/US gallon",
        "mi/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category="length per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1609.344, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1609.344, 3600, 0.0)
    db.AddUnit(
        "velocity", "miles/hour", "mi/h", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 63360, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 63360, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "miles/inch",
        "mi/in",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 2589988, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2589988, 1.0, 0.0)
    db.AddUnit("area", "square miles", "mi2", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 4168182000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4168182000, 1.0, 0.0)
    db.AddUnit("volume", "cubic mile", "mi3", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000254, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000254, 1.0, 0.0)
    db.AddUnit(
        "length",
        "mil, a thousandth of an inch",
        "mil",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000254, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000254, 31558150, 0.0)
    db.AddUnit(
        "velocity", "mils/year", "mil/yr", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3.1415926535898, 3200, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3.1415926535898, 3200, 0.0)
    db.AddUnit(
        "plane angle", "mil_6400", "mila", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 60, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 60, 1.0, 0.0)
    db.AddUnit("time", "minutes", "min", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 60, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 60, 0.3048, 0.0)
    db.AddUnit(
        "time per length",
        "minute per foot",
        "min/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 60, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 60, 1.0, 0.0)
    db.AddUnit(
        "time per length",
        "minute per meter",
        "min/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00029088821, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00029088821, 1.0, 0.0)
    db.AddUnit(
        "plane angle",
        "minutes angular",
        "mina",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1609.347, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1609.347, 1.0, 0.0)
    db.AddUnit(
        "length", "U.S. Survey mile", "miUS", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 2589998, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2589998, 1.0, 0.0)
    db.AddUnit(
        "area",
        "U.S. Survey square mile",
        "miUS2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "megajoules", "MJ", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "millijoules",
        "mJ",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 31558150, 0.0)
    db.AddUnit(
        "power", "megajoules/year", "MJ/a", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10, 1.0, 0.0)
    db.AddUnit(
        "force per length",
        "millijoules/square centimetre",
        "mJ/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="energy per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "megajoules/kilogram",
        "MJ/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "force",
        "megajoules/metre",
        "MJ/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="energy per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "force per length",
        "millijoules/square metre",
        "mJ/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="energy per area",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "megajoules/cubic metre",
        "MJ/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "molar thermodynamic energy",
        "megajoules/mole (kilogram)",
        "MJ/kmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "molar thermodynamic energy",
        "megajoules/mole (kilogram)",
        "MJ/mol(kg)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "temperature per length",
        "millidegrees Kelvin/metre",
        "mK/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit("volume", "millilitre", "mL", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0002199692, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0002199692, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "millilitres/UK gallon",
        "mL/galUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000264172, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000264172, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "millilitres/US gallon",
        "mL/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "milliliter per milliliter",
        "mL/mL",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 453592.4, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 453592.4, 31558150, 0.0)
    db.AddUnit(
        "mass flow rate",
        "million pounds mass/year",
        "Mlbm/yr",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit("length", "millimetres", "mm", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit("length", "megameter", "Mm", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 31558150, 0.0)
    db.AddUnit(
        "velocity",
        "millimetres/year",
        "mm/a",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "volumetric thermal expansion",
        "millimetres/millimetre degree Kelvin",
        "mm/mm.K",
        f_base_to_unit,
        f_unit_to_base,
        default_category="linear thermal expansion",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "millimetres/second",
        "mm/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "area", "square millimetres", "mm2", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "square millimetres/square millimetre",
        "mm2/mm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "volume per time per length",
        "square millimetres/second",
        "mm2/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "volume", "cubic millimetres", "mm3", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "isothermal compressibility",
        "cubic millimetres/joule",
        "mm3/J",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158987.3, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158987.3, 1.0, 0.0)
    db.AddUnit(
        "volume", "million barrels", "MMbbl", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158987.3, 1233.489, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158987.3, 1233.489, 0.0)
    db.AddUnit(
        "dimensionless",
        "million barrels/acre foot",
        "MMbbl/acre.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 133.3224, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 133.3224, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "millimetres of Mercury at 0 deg C",
        "mmHg(0C)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "conductivity",
        "millimhos/metre",
        "mmho/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "molar mass",
        "millimole",
        "mmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category="amount of substance",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28262.357, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28262.357, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "million standard cubic feet at 60 deg F",
        "MMscf(60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28262.357, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28262.357, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "million standard cubic feet/day",
        "MMscf(60F)/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28262.357, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28262.357, 0.1589873, 0.0)
    db.AddUnit(
        "dimensionless",
        "million std cu ft/ stock tank barrel",
        "MMscf60/stb60",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "million standard cubic metres 15C",
        "MMscm(15C)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "million std cubic metres, 15 degC/day",
        "MMscm(15C)/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158987.3, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158987.3, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "million stock tank barrels 60 deg F",
        "MMstb(60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158987.3, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158987.3, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "million stock tank barrels, 60 deg F/day",
        "MMstb(60F)/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158987.3, 4046.873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158987.3, 4046.873, 0.0)
    db.AddUnit(
        "standard volume per area",
        "million stock tank barrels 60 deg F/acre",
        "MMstb/acre",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158987.3, 1233.489, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158987.3, 1233.489, 0.0)
    db.AddUnit(
        "standard volume per volume",
        "million stbs, 60 deg F/acre foot",
        "MMstb/acre.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit("force", "meganewtons", "MN", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit("force", "millinewtons", "mN", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "force area",
        "millinewton metres squared",
        "mN.m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "force per length",
        "millinewtons/kilometre",
        "mN/km",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "force per length",
        "millinewtons/metre",
        "mN/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "resistance", "megaohm", "Mohm", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "resistance", "milliohm", "mohm", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "molar mass",
        "mole (gram)",
        "mol(g)",
        f_base_to_unit,
        f_unit_to_base,
        default_category="amount of substance",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "molar mass",
        "mole (kilogram)",
        "mol(kg)",
        f_base_to_unit,
        f_unit_to_base,
        default_category="amount of substance",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 3600, 0.0)
    db.AddUnit(
        "mole per time",
        "moles (kilogram)/hour",
        "kmol/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit(
        "mole per time",
        "moles (kilogram)/hour",
        "mol(kg)/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "concentration of B",
        "moles (kilogram)/cubic metre",
        "kmol/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "concentration of B",
        "moles (kilogram)/cubic metre",
        "mol(kg)/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "mole per time",
        "moles (kilogram)/second",
        "kmol/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "mole per time",
        "moles (kilogram)/second",
        "mol(kg)/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 453.5924, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 453.5924, 1.0, 0.0)
    db.AddUnit(
        "molar mass",
        "moles (pounds mass)",
        "lbmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 1.0, 0.0)
    db.AddUnit(
        "molar mass",
        "moles (pounds mass)",
        "mol(lbm)",
        f_base_to_unit,
        f_unit_to_base,
        default_category="amount of substance",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 16018.46, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 16018.46, 1.0, 0.0)
    db.AddUnit(
        "concentration of B",
        "moles (pounds mass)/cubic foot",
        "lbmol/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 16.01846, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 16.01846, 1.0, 0.0)
    db.AddUnit(
        "concentration of B",
        "moles (pounds mass)/cubic foot",
        "mol(lbm)/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 99776.33537, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 99776.33537, 1.0, 0.0)
    db.AddUnit(
        "concentration of B",
        "moles (pounds mass)/UK gallon",
        "lbmol/galUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 99.77633, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 99.77633, 1.0, 0.0)
    db.AddUnit(
        "concentration of B",
        "moles (pounds mass)/UK gallon",
        "mol(lbm)/galUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 119826.4, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 119826.4, 1.0, 0.0)
    db.AddUnit(
        "concentration of B",
        "moles (pounds mass)/US gallon",
        "lbmol/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 119.8264, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 119.8264, 1.0, 0.0)
    db.AddUnit(
        "concentration of B",
        "moles (pounds mass)/US gallon",
        "mol(lbm)/galUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 453.5924, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 453.5924, 3600, 0.0)
    db.AddUnit(
        "mole per time",
        "moles (pounds mass)/hour",
        "lbmol/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 3600, 0.0)
    db.AddUnit(
        "mole per time",
        "moles (pounds mass)/hour",
        "mol(lbm)/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 334.450944, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 334.450944, 0.0)
    db.AddUnit(
        "mole per time per area",
        "moles (pounds mass)/hour square foot",
        "mol(lbm)/h.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 453.5924, 334.450944, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 453.5924, 334.450944, 0.0)
    db.AddUnit(
        "mole per time per area",
        "moles (pounds mass)/hour square foot",
        "lbmol/h.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 453.5924, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 453.5924, 1.0, 0.0)
    db.AddUnit(
        "mole per time",
        "moles (pounds mass)/second",
        "lbmol/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 1.0, 0.0)
    db.AddUnit(
        "mole per time",
        "moles (pounds mass)/second",
        "mol(lbm)/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 453.5924, 0.09290304, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 453.5924, 0.09290304, 0.0)
    db.AddUnit(
        "mole per time per area",
        "moles (pounds mass)/second square foot",
        "lbmol/s.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 0.09290304, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 0.09290304, 0.0)
    db.AddUnit(
        "mole per time per area",
        "moles (pounds mass)/second square foot",
        "mol(lbm)/s.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "pressure", "millipascal", "mPa", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "pressure", "megapascals", "MPa", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "millipascal seconds",
        "mPa.s",
        f_base_to_unit,
        f_unit_to_base,
        default_category="dynamic viscosity",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "mass per time per area",
        "megapascal seconds/metre (megarayl)",
        "MPa.s/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 3600, 0.0)
    db.AddUnit(
        "pressure per time",
        "megapascal per hour",
        "MPa/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "pressure per length",
        "megapascal per meter",
        "MPa/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894757000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894757000, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "mega pounds per square inch",
        "Mpsi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "plane angle", "milliradian", "mrad", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "plane angle", "megaradian", "Mrad", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00001, 1.0, 0.0)
    db.AddUnit(
        "dose equivalent",
        "milli-rem",
        "mrem",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00001, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00001, 3600, 0.0)
    db.AddUnit(
        "dose equivalent rate",
        "milli-rems per hour",
        "mrem/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "electric conductance",
        "millisiemen",
        "mS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit("time", "milliseconds", "ms", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0005, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0005, 1.0, 0.0)
    db.AddUnit(
        "time", "half a millisecond", "ms/2", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "time per length",
        "milliseconds/centimetre",
        "ms/cm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 0.3048, 0.0)
    db.AddUnit(
        "time per length",
        "millisecond per foot",
        "ms/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 0.0254, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 0.0254, 0.0)
    db.AddUnit(
        "time per length",
        "milliseconds/inch",
        "ms/in",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "conductivity",
        "millisiemens/metre",
        "mS/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "time per length",
        "millisecond per meter",
        "ms/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "milliseconds/second",
        "ms/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category="relative time",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28.262357, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28.262357, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "thousand cubic feet at 60 deg F",
        "Mscf(60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28.262357, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28.262357, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "thousand standard cubic feet/day",
        "Mscf(60F)/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28.262357, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28.262357, 0.1589873, 0.0)
    db.AddUnit(
        "dimensionless",
        "thousand std cu ft/ stock tank barrel",
        "Mscf60/stb60",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "thousand std cubic metres, 15 degC/day",
        "Mscm(15C)/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "std cubic metres/day",
        "sm3/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1, 0.0)
    db.AddUnit(
        "standard volume per time",
        "std cubic metres/second",
        "sm3/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "thousand std cubic metres/day",
        "Msm3/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "million std cubic metres/day",
        "MMsm3/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00000000484814, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00000000484814, 1.0, 0.0)
    db.AddUnit(
        "plane angle",
        "milliseconds angular",
        "mseca",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "mega standard cubic metres 15C",
        "Msm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158.9873, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158.9873, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "thousand stock tank barrels 60 F",
        "Mstb(60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158.9873, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158.9873, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "thousand stock tank barrels,60 deg F/day",
        "Mstb(60F)/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dose equivalent",
        "millisievert",
        "mSv",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 3600, 0.0)
    db.AddUnit(
        "dose equivalent rate",
        "millisieverts per hour",
        "mSv/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "magnetic induction",
        "milliteslas",
        "mT",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "electric potential",
        "megavolt",
        "MV",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "electric potential",
        "millivolts",
        "mV",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 0.3048, 0.0)
    db.AddUnit(
        "electric field strength",
        "millivolt per foot",
        "mV/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "electric field strength",
        "millivolt per meter",
        "mV/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit("power", "megawatts", "MW", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit("power", "milliwatt", "mW", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600000000, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "megawatt hours",
        "MW.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600000000, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "megawatt hours/kilogram",
        "MW.h/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3600000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3600000000, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "megawatt hours/cubic metre",
        "MW.h/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "density of heat flow rate",
        "milliwatts/square metres",
        "mW/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "magnetic flux", "milliwebers", "mWb", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 31558150000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 31558150000000, 1.0, 0.0)
    db.AddUnit("time", "megayears", "MY", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "newton metre",
        "N.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "force",
        "newton metres/metre",
        "N.m/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="force length per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "newton seconds/metre squared",
        "N.s/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category="dynamic viscosity",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 30, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 30, 0.0)
    db.AddUnit(
        "force per length",
        "newton per thirty meters",
        "N/30m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "newtons/square metre",
        "N/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "newtons/square millimetre",
        "N/mm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "electric current",
        "nanoampere",
        "nA",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1852, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1852, 1.0, 0.0)
    db.AddUnit(
        "length", "nautical mile", "nautmi", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "electric capacity",
        "nanocoulomb",
        "nC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 37, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 37, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "None",
        "nCi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 37, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 37, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "nanocurie",
        "ncurie",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless", "nanoeuclid", "nEuc", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "self inductance", "nanohenry", "nH", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "nanojoules", "nJ", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit("length", "nanometres", "nm", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "nanometer per second",
        "nm/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "resistance", "nanohm", "nohm", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit("time", "nanoseconds", "ns", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 0.3048, 0.0)
    db.AddUnit(
        "time per length",
        "nanoseconds/foot",
        "ns/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "time per length",
        "nanoseconds/metre",
        "ns/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "magnetic induction",
        "nanoteslas",
        "nT",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit("power", "nanowatts", "nW", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 79.57747, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 79.57747, 1.0, 0.0)
    db.AddUnit(
        "magnetization", "oersted", "Oe", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "electrical resistivity",
        "ohm centimetres",
        "ohm.cm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02834952, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02834952, 1.0, 0.0)
    db.AddUnit(
        "mass",
        "avoirdupois ounces",
        "oz(av)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.03110348, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.03110348, 1.0, 0.0)
    db.AddUnit(
        "mass", "troy ounces", "oz(troy)", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4.448222, 16, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4.448222, 16, 0.0)
    db.AddUnit("force", "ounce force", "ozf", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4535924, 16.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4535924, 16.0, 0.0)
    db.AddUnit("mass", "ounce mass", "ozm", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "poise",
        "P",
        f_base_to_unit,
        f_unit_to_base,
        default_category="dynamic viscosity",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000001, 1.0, 0.0)
    db.AddUnit(
        "electric current",
        "picoampere",
        "pA",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(101325, 1, 1, 0)
    f_base_to_unit = MakeBaseToCustomary(101325, 1, 1, 0)
    db.AddUnit(
        "pressure", "pascal gauge", "Pa(g)", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit(
        "pressure per time",
        "pascal per hour",
        "Pa/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000001, 1.0, 0.0)
    db.AddUnit(
        "electric capacity",
        "picocoulomb",
        "pC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.037, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.037, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "None",
        "pCi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 37, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 37, 1.0, 0.0)
    db.AddUnit(
        "specific activity (of radioactivity)",
        "picocurie per gram",
        "pCi/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.037, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.037, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "picocurie",
        "pcurie",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.138255, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.138255, 1.0, 0.0)
    db.AddUnit("force", "poundals", "pdl", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000138255, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000138255, 1.0, 0.0)
    db.AddUnit(
        "force area",
        "poundal centimetre squared",
        "pdl.cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.04214012, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.04214012, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "foot poundal",
        "pdl.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.138255, 0.01, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.138255, 0.01, 0.0)
    db.AddUnit(
        "force per length",
        "poundals/centimetre",
        "pdl/cm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "per mille",
        "permil",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000001, 1.0, 0.0)
    db.AddUnit(
        "capacitance", "picofarads", "pF", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000001, 1.0, 0.0)
    db.AddUnit("length", "picometer", "pm", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000001, 1.0, 0.0)
    db.AddUnit(
        "pressure", "picopascal", "pPa", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "parts per ten thousand",
        "ppdk",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "parts per thousand",
        "ppk",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "parts per million",
        "ppm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "volumetric thermal expansion",
        "part per million per degree Celsius",
        "ppm/degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000018, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000018, 1.0, 0.0)
    db.AddUnit(
        "volumetric thermal expansion",
        "part per million per degree Fahrenheit",
        "ppm/degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000001, 1.0, 0.0)
    db.AddUnit("time", "picosecond", "ps", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "electric conductance",
        "picosiemens",
        "pS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 47.88026, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 47.88026, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "pounds/square foot",
        "psf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "pounds/square inch",
        "psi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 23.05916, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 23.05916, 0.0)
    db.AddUnit(
        "pressure time per volume",
        "pounds per square inch days/barrel",
        "psi.d/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "pound per square inch second",
        "psi.s",
        f_base_to_unit,
        f_unit_to_base,
        default_category="dynamic viscosity",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 30.48, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 30.48, 0.0)
    db.AddUnit(
        "pressure per length",
        "pounds/square inch per 100 feet",
        "psi/100ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 0.3048, 0.0)
    db.AddUnit(
        "pressure per length",
        "pounds/square inch per foot",
        "psi/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 30.48, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 30.48, 0.0)
    db.AddUnit(
        "pressure per length",
        "pounds/square inch per 100 feet",
        "psi/ft(100)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 3600, 0.0)
    db.AddUnit(
        "pressure per time",
        "pound per square inch per hour",
        "psi/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 304.8, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 304.8, 0.0)
    db.AddUnit(
        "pressure per length",
        "pounds/square inch per thousand feet",
        "psi/kft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 1.0, 0.0)
    db.AddUnit(
        "pressure per length",
        "pound per square inch per meter",
        "psi/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 60, 0.0)
    db.AddUnit(
        "pressure per time",
        "pound per square inch per minute",
        "psi/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 47537674, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 47537674, 1.0, 0.0)
    db.AddUnit(
        "pressure squared",
        "pound per square inch squared",
        "psi2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4107255041294, 0.000028316847, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4107255041294, 0.000028316847, 0.0)
    db.AddUnit(
        "Darcy flow coefficient",
        "psi squared days/ centipoise cubic foot",
        "psi2.d/cP.ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4107255041294, 0.000028316847, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4107255041294, 0.000028316847, 0.0)
    db.AddUnit(
        "Darcy flow coefficient",
        "psi squared days/ centipoise cubic foot",
        "psi2.d/cp.ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3.5486698355e017, 0.0000008018438, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3.5486698355e017, 0.0000008018438, 0.0)
    db.AddUnit(
        "nonDarcy flow coefficient",
        "(psi days/cubic foot)squared/centipoise",
        "psi2.d2/cP.ft6",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3.5486698355e017, 0.0000008018438, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3.5486698355e017, 0.0000008018438, 0.0)
    db.AddUnit(
        "nonDarcy flow coefficient",
        "(psi days/cubic foot)squared/centipoise",
        "psi2.d2/cp.ft6",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 4753764090, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 4753764090, 1.0, 0.0)
    db.AddUnit(
        "pressure per time",
        "pounds/square inch squared/ centipoise",
        "psi2/cP",
        f_base_to_unit,
        f_unit_to_base,
        default_category="pressure squared per (dynamic viscosity)",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "pounds/square inch absolute",
        "psia",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(101325, 6894.757, 1, 0)
    f_base_to_unit = MakeBaseToCustomary(101325, 6894.757, 1, 0)
    db.AddUnit(
        "pressure",
        "pounds/square inch gauge",
        "psig",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0005682615, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0005682615, 1.0, 0.0)
    db.AddUnit("volume", "UK pint", "ptUK", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000000002116809, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000000002116809, 1.0, 0.0)
    db.AddUnit(
        "isothermal compressibility",
        "UK pints/horsepower hour",
        "ptUK/hp.hr",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0005682615, 158.9873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0005682615, 158.9873, 0.0)
    db.AddUnit(
        "dimensionless",
        "UK pints/1000 barrels",
        "ptUK/Mbbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0004731765, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0004731765, 1.0, 0.0)
    db.AddUnit("volume", "US pints", "ptUS", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4731765, 0.01589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4731765, 0.01589873, 0.0)
    db.AddUnit(
        "dimensionless",
        "US pint per ten barrel",
        "ptUS/10bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001136523, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001136523, 1.0, 0.0)
    db.AddUnit("volume", "UK quarts", "qtUK", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0009463529, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0009463529, 1.0, 0.0)
    db.AddUnit("volume", "US quarts", "qtUS", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.055056e018, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.055056e018, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "quads", "quad", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.055056e018, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.055056e018, 31558150, 0.0)
    db.AddUnit(
        "power",
        "quads/year",
        "quad/yr",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.3048, 0.0)
    db.AddUnit(
        "angle per length",
        "radians per foot",
        "rad/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.028316846592, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.028316846592, 0.0)
    db.AddUnit(
        "angle per volume",
        "radians per cubic foot",
        "rad/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit("absorbed dose", "rad", "rd", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "dose equivalent", "rem", "rem", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 3600, 0.0)
    db.AddUnit(
        "dose equivalent rate",
        "rems per hour",
        "rem/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6.283185307, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6.283185307, 60, 0.0)
    db.AddUnit(
        "frequency",
        "revolutions/minute",
        "rev/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category="angle per time",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6.283185307, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6.283185307, 1.0, 0.0)
    db.AddUnit(
        "frequency",
        "revolutions/second",
        "rev/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category="angle per time",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6.283185307, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6.283185307, 60, 0.0)
    db.AddUnit(
        "frequency",
        "revolutions/minute",
        "rpm",
        f_base_to_unit,
        f_unit_to_base,
        default_category="angle per time",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6.283185307, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6.283185307, 60, 0.0)
    db.AddUnit(
        "angular acceleration",
        "revolutions/minute per second",
        "rpm/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100, 1.0, 0.0)
    db.AddUnit(
        "time per length",
        "seconds/centimetre",
        "s/cm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.3048, 0.0)
    db.AddUnit(
        "time per length",
        "seconds/foot",
        "s/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.028316846592, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.028316846592, 0.0)
    db.AddUnit(
        "time per volume",
        "second per cubic foot",
        "s/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.0254, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.0254, 0.0)
    db.AddUnit(
        "time per length",
        "seconds/inch",
        "s/in",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.001, 0.0)
    db.AddUnit(
        "time per volume",
        "second per litre",
        "s/L",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.001136523, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.001136523, 0.0)
    db.AddUnit(
        "time per volume",
        "second per UK quart",
        "s/qtUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.0009463529, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.0009463529, 0.0)
    db.AddUnit(
        "time per volume",
        "second per US quart",
        "s/qtUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 42.63769, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 42.63769, 1.0, 0.0)
    db.AddUnit("mass", "sacks", "sack94", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.028262357, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.028262357, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "std cubic feet at 60 deg F",
        "scf(60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.028262357, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.028262357, 0.1589873, 0.0)
    db.AddUnit(
        "standard volume per volume",
        "std cubic feet at 60 deg F/barrel",
        "scf(60F)/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.028262357, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.028262357, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "standard cubic feet/day",
        "scf(60F)/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.028262357, 0.09290304, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.028262357, 0.09290304, 0.0)
    db.AddUnit(
        "standard volume per area",
        "std cubic feet at 60 deg F/square foot",
        "scf(60F)/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.9980757, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.9980757, 1.0, 0.0)
    db.AddUnit(
        "standard volume per volume",
        "std cubic feet at 60 deg Ft/cubic foot",
        "scf(60F)/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "std cubic metres at 15 deg C/day",
        "scm(15C)/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.1589873, 0.0)
    db.AddUnit(
        "dimensionless",
        "std cubic metres / stock tank barrel",
        "scm15/stb60",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00000484814, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00000484814, 1.0, 0.0)
    db.AddUnit(
        "plane angle",
        "seconds angular",
        "seca",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "per length",
        "capture unit",
        "sigma",
        f_base_to_unit,
        f_unit_to_base,
        default_category="area per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1000, 0.0)
    db.AddUnit(
        "dimensionless",
        "std cubic metres/ 1000 std cubic metre",
        "sm3/ksm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.09290304, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.09290304, 1.0, 0.0)
    db.AddUnit(
        "area", "square feet", "sq ft", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00064516, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00064516, 1.0, 0.0)
    db.AddUnit(
        "area", "square inches", "sq in", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 2589988, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2589988, 1.0, 0.0)
    db.AddUnit(
        "area", "square miles", "sq mi", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.8361274, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.8361274, 1.0, 0.0)
    db.AddUnit(
        "area", "square yards", "sq yd", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "stock tank barrel at 60 deg F",
        "stb(60F)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 4046.873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 4046.873, 0.0)
    db.AddUnit(
        "standard volume per area",
        "stock tank barrels, 60 deg F/acre",
        "stb(60F)/acre",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "standard volume per volume",
        "stock tank barrels, 60 deg F/barrel",
        "stb(60F)/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "stock tank barrels, 60 deg F/day",
        "stb(60F)/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 28262.357, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 28262.357, 0.0)
    db.AddUnit(
        "dimensionless",
        "stock tank barrels/ million std cu ft",
        "stb60/MMscf60",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 1000000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 1000000, 0.0)
    db.AddUnit(
        "dimensionless",
        "stock tank barrels/ million std cu mts",
        "stb60/MMscm15",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 28.262357, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 28.262357, 0.0)
    db.AddUnit(
        "dimensionless",
        "stock tank barrels/ 1000 std cu ft",
        "stb60/Mscf60",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 1000, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 1000, 0.0)
    db.AddUnit(
        "dimensionless",
        "stock tank barrels/ 1000 std cu metres",
        "stb60/Mscm15",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "stock tank barrels/ std cu metres",
        "stb60/scm15",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit(
        "dose equivalent rate",
        "sieverts per hour",
        "Sv/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit("mass", "tonne", "t", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 31558150, 0.0)
    db.AddUnit(
        "mass flow rate",
        "tonnes/year",
        "t/a",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 86400, 0.0)
    db.AddUnit(
        "mass flow rate", "tonnes/day", "t/d", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 3600, 0.0)
    db.AddUnit(
        "mass flow rate",
        "tonnes/hour",
        "t/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 60, 0.0)
    db.AddUnit(
        "mass flow rate",
        "tonnes per minute",
        "t/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "quantity of light",
        "talbot",
        "talbot",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0e12, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0e12, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "terabecquerel",
        "TBq",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28316850000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28316850000, 1.0, 0.0)
    db.AddUnit(
        "volume",
        "trillion cubic feet",
        "tcf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000001602177, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000001602177, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "tera electron volts",
        "TeV",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 105505600, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 105505600, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "therms", "therm", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 105505600, 0.02831685, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 105505600, 0.02831685, 0.0)
    db.AddUnit(
        "normal stress",
        "therms/cubic foot",
        "therm/ft3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 23208000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 23208000000, 1.0, 0.0)
    db.AddUnit(
        "normal stress",
        "therms/UK gallon",
        "therm/galUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 105505600, 0.4535924, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 105505600, 0.4535924, 0.0)
    db.AddUnit(
        "specific energy",
        "therms/pound mass",
        "therm/lbm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000000, 1.0, 0.0)
    db.AddUnit(
        "moment of force", "terajoules", "TJ", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000000, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000000, 31558150, 0.0)
    db.AddUnit(
        "power",
        "terajoules/year",
        "TJ/a",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000000, 1.0, 0.0)
    db.AddUnit(
        "resistance", "teraohm", "Tohm", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3516.853, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3516.853, 1.0, 0.0)
    db.AddUnit(
        "power",
        "tons of refrigeration",
        "ton of refrig",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9964.016, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9964.016, 1.0, 0.0)
    db.AddUnit(
        "force", "UK tons force", "tonfUK", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 925.6874, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 925.6874, 1.0, 0.0)
    db.AddUnit(
        "force area",
        "UK ton feet squared",
        "tonfUK.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9964.016, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9964.016, 0.3048, 0.0)
    db.AddUnit(
        "force per length",
        "UK tons force/foot",
        "tonfUK/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9964.016, 0.09290304, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9964.016, 0.09290304, 0.0)
    db.AddUnit(
        "pressure",
        "UK tons force/square foot",
        "tonfUK/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 8896.443, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 8896.443, 1.0, 0.0)
    db.AddUnit(
        "force", "US tons force", "tonfUS", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 2711.636, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2711.636, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "US tons force feet",
        "tonfUS.ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 826.5067, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 826.5067, 1.0, 0.0)
    db.AddUnit(
        "force area",
        "US tons force feet squared",
        "tonfUS.ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 14317440, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 14317440, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "US tons force miles",
        "tonfUS.mi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 14317440, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 14317440, 0.1589873, 0.0)
    db.AddUnit(
        "normal stress",
        "US ton force miles/barrel",
        "tonfUS.mi/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 14317440, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 14317440, 0.3048, 0.0)
    db.AddUnit(
        "force",
        "US tons force miles/foot",
        "tonfUS.mi/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category="force length per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 8896.443, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 8896.443, 0.3048, 0.0)
    db.AddUnit(
        "force per length",
        "US tons force/foot",
        "tonfUS/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 95760.52, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 95760.52, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "US tons force/square foot",
        "tonfUS/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 13789510, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 13789510, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "US tons force/square inch",
        "tonfUS/in2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1016.047, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1016.047, 1.0, 0.0)
    db.AddUnit("mass", "UK tons", "tonUK", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1016.047, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1016.047, 31558150, 0.0)
    db.AddUnit(
        "mass flow rate",
        "UK tons/year",
        "tonUK/a",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1016.047, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1016.047, 86400, 0.0)
    db.AddUnit(
        "mass flow rate",
        "UK tons/day",
        "tonUK/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1016.047, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1016.047, 3600, 0.0)
    db.AddUnit(
        "mass flow rate",
        "UK tons/hour",
        "tonUK/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1016.047, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1016.047, 60, 0.0)
    db.AddUnit(
        "mass flow rate",
        "UK tons/minute",
        "tonUK/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 907.1847, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 907.1847, 1.0, 0.0)
    db.AddUnit("mass", "US tons", "tonUS", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 907.1847, 31558150, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 907.1847, 31558150, 0.0)
    db.AddUnit(
        "mass flow rate",
        "US tons/year",
        "tonUS/a",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 907.1847, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 907.1847, 86400, 0.0)
    db.AddUnit(
        "mass flow rate",
        "US tons/day",
        "tonUS/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9764.855, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9764.855, 1.0, 0.0)
    db.AddUnit(
        "surface density",
        "US tons/square foot",
        "tonUS/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 907.1847, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 907.1847, 3600, 0.0)
    db.AddUnit(
        "mass flow rate",
        "US tons/hour",
        "tonUS/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 907.1847, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 907.1847, 60, 0.0)
    db.AddUnit(
        "mass flow rate",
        "US tons/minute",
        "tonUS/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 133.3224, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 133.3224, 1.0, 0.0)
    db.AddUnit("pressure", "torr", "torr", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000000000, 1.0, 0.0)
    db.AddUnit("power", "terawatts", "TW", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 3.6e015, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3.6e015, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "terrawatt hours",
        "TW.h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "electric current",
        "microampere",
        "uA",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "current density",
        "microampere per square centimeter",
        "uA/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 0.00064516, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 0.00064516, 0.0)
    db.AddUnit(
        "current density",
        "microampere per square inch",
        "uA/in2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1, 1.0, 0.0)
    db.AddUnit(
        "pressure", "microbars", "ubar", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "electric capacity",
        "microcoulomb",
        "uC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.04184, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.04184, 1.0, 0.0)
    db.AddUnit(
        "density of heat flow rate",
        "microcalories/second square centimetre",
        "ucal/s.cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 37000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 37000, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "None",
        "uCi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 37000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 37000, 1.0, 0.0)
    db.AddUnit(
        "activity (of radioactivity)",
        "microcurie",
        "ucurie",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "microEuclids",
        "uEuc",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "capacitance", "microfarads", "uF", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "permittivity",
        "microfarads/metre",
        "uF/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit("mass", "micrograms", "ug", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "density",
        "micrograms/cubic centimetre",
        "ug/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "self inductance", "microhenry", "uH", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "magnetic permeability",
        "microhenries/metre",
        "uH/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000006283185307, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000006283185307, 1.0, 0.0)
    db.AddUnit(
        "frequency", "microhertz", "uHz", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "moment of force",
        "microjoules",
        "uJ",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit("length", "microns", "um", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "velocity",
        "micrometer per second",
        "um/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000001, 1.0, 0.0)
    db.AddUnit(
        "area", "square microns", "um2", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000001, 1.0, 0.0)
    db.AddUnit(
        "volume",
        "square micron metres",
        "um2.m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1333224, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1333224, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "microns of Mercury at 0 deg C",
        "umHg(0C)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "molar mass",
        "micromole",
        "umol",
        f_base_to_unit,
        f_unit_to_base,
        default_category="amount of substance",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit("force", "micronewtons", "uN", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "unitless",
        "unitless",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "resistance", "microohm", "uohm", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 0.3048, 0.0)
    db.AddUnit(
        "resistivity per length",
        "microhm per foot",
        "uohm/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "resistivity per length",
        "microhm per meter",
        "uohm/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "pressure", "micropascal", "uPa", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.006894757, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.006894757, 1.0, 0.0)
    db.AddUnit(
        "pressure",
        "micropounds/square inch",
        "upsi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "plane angle", "microradian", "urad", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "electric conductance",
        "microsiemens",
        "uS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit("time", "microsecond", "us", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 0.3048, 0.0)
    db.AddUnit(
        "time per length",
        "microseconds/foot",
        "us/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "time per length",
        "microseconds/metre",
        "us/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "magnetic induction",
        "microteslas",
        "uT",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "electric potential",
        "microvolts",
        "uV",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 0.3048, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 0.3048, 0.0)
    db.AddUnit(
        "electric field strength",
        "microvolt per foot",
        "uV/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "electric field strength",
        "microvolt per meter",
        "uV/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit("power", "microwatts", "uW", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "power per volume",
        "microwatts/cubic metre",
        "uW/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "magnetic flux", "microwebers", "uWb", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10, 1.0, 0.0)
    db.AddUnit(
        "potential difference per per power drop",
        "volts/decibel",
        "V/dB",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "volume percent",
        "volpercent",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "volume parts per million",
        "volppm",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 10000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 10000, 1.0, 0.0)
    db.AddUnit(
        "density of heat flow rate",
        "watts/square centimetre",
        "W/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "watts/kilowatt",
        "W/kW",
        f_base_to_unit,
        f_unit_to_base,
        default_category="relative power",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "density of heat flow rate",
        "watts per square millimeter",
        "W/mm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "watts/watt",
        "W/W",
        f_base_to_unit,
        f_unit_to_base,
        default_category="relative power",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "magnetic vector potential",
        "webers/millimetre",
        "Wb/mm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 604800, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 604800, 1.0, 0.0)
    db.AddUnit("time", "weeks", "wk", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "weight percent",
        "wtpercent",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mass concentration",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "weight parts per million",
        "wtppm",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mass concentration",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.9144, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.9144, 1.0, 0.0)
    db.AddUnit("length", "yards", "yd", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.83612736, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.83612736, 1.0, 0.0)
    db.AddUnit("area", "square yards", "yd2", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.7645549, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.7645549, 1.0, 0.0)
    db.AddUnit("volume", "cubic yard", "yd3", f_base_to_unit, f_unit_to_base, default_category=None)
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.9143992, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.9143992, 1.0, 0.0)
    db.AddUnit(
        "length",
        "Benoits yard (1895 A)",
        "ydBnA",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 36, 39.370113, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 36, 39.370113, 0.0)
    db.AddUnit(
        "length",
        "Benoits yard (1895 B)",
        "ydBnB",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.914391795, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.914391795, 1.0, 0.0)
    db.AddUnit(
        "length", "Clarkes yard", "ydCla", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.914391795, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.914391795, 1.0, 0.0)
    db.AddUnit(
        "length", "imperial yard", "ydIm", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 36, 39.370142, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 36, 39.370142, 0.0)
    db.AddUnit(
        "length", "Indian yard", "ydInd", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.91439523, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.91439523, 1.0, 0.0)
    db.AddUnit(
        "length",
        "Indian yard (1937)",
        "ydInd(37)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.9143988, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.9143988, 1.0, 0.0)
    db.AddUnit(
        "length",
        "Indian yard (1962)",
        "ydInd(62)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.9143985, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.9143985, 1.0, 0.0)
    db.AddUnit(
        "length",
        "Indian yard (1975)",
        "ydInd(75)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 36, 39.370147, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 36, 39.370147, 0.0)
    db.AddUnit(
        "length", "Sears yard", "ydSe", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3155815000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3155815000000, 1.0, 0.0)
    db.AddUnit(
        "time", "100000 years", "yr(100k)", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.002649, 6894.757, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.002649, 6894.757, 0.0)
    db.AddUnit(
        "injectivity factor",
        "injectivity factor in barrel per minute",
        "bbl/min.psi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.1802270983e-10, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.1802270983e-10, 1.0, 0.0)
    db.AddUnit(
        "injectivity factor",
        "injectivity factor in meter per day",
        "(m3/d)/(kgf/cm2)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 86400, 0.0)
    db.AddUnit(
        "velocity",
        "centimeter per day",
        "cm/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 2.3059150743957171368106291270119, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 2.3059150743957171368106291270119, 1.0, 0.0)
    db.AddUnit(
        "transmissibility",
        "cp.bbl/day/psi",
        "cp.bbl/day/psi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.028316846592, 0.0689475729, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.028316846592, 0.0689475729, 0.0)
    db.AddUnit(
        "transmissibility",
        "cp.ft3/day/psi",
        "cp.ft3/day/psi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 0.0028728155375, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 0.0028728155375, 0.0)
    db.AddUnit(
        "transmissibility",
        "cp.cm3/h/psi",
        "cp.cm3/h/psi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.01, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.01, 0.0)
    db.AddUnit(
        "transmissibility",
        "cp.m3/day/kPa",
        "cp.m3/day/kPa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.980665, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.980665, 0.0)
    db.AddUnit(
        "transmissibility",
        "cp.m3/day/kgf/cm2",
        "cp.m3/day/kgf/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000023686152, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000023686152, 1.0, 0.0)
    db.AddUnit(
        "transmissibility",
        "cp.cm3/h/Atm",
        "cp.cm3/h/Atm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3.53146667115e-5, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3.53146667115e-5, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "cubic meter per million cubic feet",
        "m3/MMcf",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28316.85, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28316.85, 0.1589873, 0.0)
    db.AddUnit(
        "dimensionless",
        "million cubic feet per barrel",
        "MMcf/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 101325, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 101325, 0.0)
    db.AddUnit(
        "compressibility",
        "per atmospheres",
        "1/atm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 86400000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 86400000, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "kilopascal day",
        "kPa.d",
        f_base_to_unit,
        f_unit_to_base,
        default_category="dynamic viscosity",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1, 0.0)
    db.AddUnit(
        "mass per time per length",
        "kilopascal second",
        "kPa.s",
        f_base_to_unit,
        f_unit_to_base,
        default_category="dynamic viscosity",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "volume per standard volume",
        "cubic metres/std cubic metres",
        "m3/sm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "standard volume per volume",
        "std cubic metres/cubic metre",
        "sm3/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "volume per standard volume",
        "cubic centimetres/std cubic centimetres",
        "cm3/scm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "standard volume per volume",
        "std cubic centimetres/cubic centimetre",
        "scm3/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "volume per standard volume",
        "barrels/stock tank barrel",
        "bbl/stb",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 28.262357, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 28.262357, 0.0)
    db.AddUnit(
        "volume per standard volume",
        "barrels/thousand std cubic feet",
        "bbl/Mscf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "standard volume per volume",
        "stock tank barrels/barrel",
        "stb/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "stock tank barrels, 60 deg F/day",
        "stb/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158.9873, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158.9873, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "thousand stock tank barrels, 60 deg F/day",
        "Mstb/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 158987.3, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 158987.3, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "million stock tank barrels, 60 deg F/day",
        "MMstb/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.028262357, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.028262357, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "standard cubic feet/day",
        "scf/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28.262357, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28.262357, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "thousand standard cubic feet/day",
        "Mscf/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28262.357, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28262.357, 86400, 0.0)
    db.AddUnit(
        "standard volume per time",
        "million standard cubic feet/day",
        "MMscf/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28.262357, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28.262357, 0.1589873, 0.0)
    db.AddUnit(
        "standard volume per volume",
        "thousand std cubic feet/barrel",
        "Mscf/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.028262357, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.028262357, 0.1589873, 0.0)
    db.AddUnit(
        "standard volume per volume",
        "std cubic feet/barrel",
        "scf/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28.31685, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28.31685, 86400, 0.0)
    db.AddUnit(
        "volume flow rate",
        "thousand cubic feet per day",
        "Mcf/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 28.31685, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 28.31685, 0.0)
    db.AddUnit(
        "dimensionless",
        "barrel per thousand cubic feet",
        "bbl/Mcf",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per volume",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.0001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.0001, 0.0)
    db.AddUnit(
        "per area",
        "per square centimetre",
        "1/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "stock tank barrel",
        "stb",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.028262357, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.028262357, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "std cubic feet",
        "scf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "molar mass",
        "mole (kilogram)",
        "kgmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category="amount of substance",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "molar mass", "gram mole", "gmol", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "concentration of B",
        "moles (gram)/cubic metre",
        "gmol/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit(
        "mole per time",
        "moles/hour",
        "mol/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 86400, 0.0)
    db.AddUnit(
        "mole per time",
        "moles (kilogram)/day",
        "kmol/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400, 0.0)
    db.AddUnit(
        "mole per time", "moles/day", "mol/d", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 453.5924, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 453.5924, 86400, 0.0)
    db.AddUnit(
        "mole per time",
        "moles (pounds mass)/day",
        "lbmol/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "concentration of B",
        "moles/litre",
        "mol/L",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.000001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.000001, 0.0)
    db.AddUnit(
        "concentration of B",
        "moles/cubic centimetre",
        "mol/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3804.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3804.01, 1.0, 0.0)
    db.AddUnit(
        "concentration of B",
        "moles (pounds mass)/barrel",
        "lbmol/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1e6, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1e6, 1.0, 0.0)
    db.AddUnit(
        "solubility product",
        "squared moles/litre",
        "(mol/L)^2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "moles/moles",
        "mol/mol",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mole per mole",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "kilogram moles/kilogram moles",
        "kmol/kmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mole per mole",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "pound mass mol/pound mass mol",
        "lbmol/lbmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mole per mole",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "grams/gram",
        "g/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mass concentration",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "miligrams/gram",
        "mg/g",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mass concentration",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "grams per hundred gram",
        "g/100g",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mass concentration",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "pounds mass/pounds mass",
        "lbm/lbm",
        f_base_to_unit,
        f_unit_to_base,
        default_category="mass concentration",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 86400, 0.0)
    db.AddUnit(
        "pressure per time",
        "kilopascal per day",
        "kPa/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 86400, 0.0)
    db.AddUnit(
        "pressure per time",
        "pound per square inch per day",
        "psi/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless", "<ind>", "<ind>", f_base_to_unit, f_unit_to_base, default_category="index"
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "<mult>",
        "<mult>",
        f_base_to_unit,
        f_unit_to_base,
        default_category="multiplier",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "<stat>",
        "<stat>",
        f_base_to_unit,
        f_unit_to_base,
        default_category="status",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100.0, 1.0, 0.0)
    db.AddUnit(
        "fraction", "fraction", "<fraction>", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "parts per million by volume",
        "ppmv",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "standard volume",
        "standard cubic metres",
        "sm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000.0, 1.0, 0.0)
    db.AddUnit(
        "mass per time per length",
        "megapascal seconds",
        "MPa.s",
        f_base_to_unit,
        f_unit_to_base,
        default_category="dynamic viscosity",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "equivalent per volume",
        "milliequivalents/milliliter",
        "meq/mL",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000.0, 1.0, 0.0)
    db.AddUnit(
        "adsorption rate",
        "kilograms per kg per day",
        "kg/kg/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0, 0.0)
    db.AddUnit(
        "mass consumption efficiency",
        "mgrams per liters per mgrams per liters",
        "kg/m3/kg/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "density generation",
        "mgrams per liter per day",
        "mg/l/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "parts per million by volume per concentration",
        "parts per million by volume per kilograms per cubic metre",
        "ppmv/kg/m3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 47.88026, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 47.88026, 1.0, 0.0)
    db.AddUnit(
        "fluid consistency",
        "pound force to seconds to the power of n per feet squared",
        "lbf.s^n/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.4788026, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.4788026, 1.0, 0.0)
    db.AddUnit(
        "fluid consistency",
        "pound force to seconds to the power of n per hundred feet squared",
        "lbf.s^n/100ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0010055063442902922275386711091103, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0010055063442902922275386711091103, 1.0, 0.0)
    db.AddUnit(
        "fluid consistency",
        "equivalent to centipoise",
        "eq.cp",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 1.0, 0.0)
    db.AddUnit(
        "area",
        "barrel/meter",
        "bbl/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="volume per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "volume fraction per temperature",
        "(volume/volume)/temperature",
        "(m3/m3)/degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9, 5, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9, 5, 0.0)
    db.AddUnit(
        "volume fraction per temperature",
        "(volume/volume)/temperature",
        "(m3/m3)/degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400, 0.0)
    db.AddUnit(
        "volume per time per length",
        "square metres/day",
        "m2/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.09290304, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.09290304, 86400, 0.0)
    db.AddUnit(
        "volume per time per length",
        "square feet/day",
        "ft2/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.02831685, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.02831685, 1.0, 0.0)
    db.AddUnit(
        "volume per wtpercent",
        "ft3/wtpercent",
        "ft3/wtpercent",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "mass per mol", "g/mol", "g/mol", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "mass per mol",
        "lb/lbmol",
        "lb/lbmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000.0, 1.0, 0.0)
    db.AddUnit(
        "mole per mass", "mol/g", "mol/g", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000.0, 1.0, 0.0)
    db.AddUnit(
        "mole per mass",
        "lbmol/lb",
        "lbmol/lb",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.07211, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.07211, 1.0, 0.0)
    db.AddUnit(
        "thermal conductivity",
        "British thermal units/day foot deg F",
        "Btu/d.ft.degF",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01157, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01157, 1.0, 0.0)
    db.AddUnit(
        "thermal conductivity",
        "kilojoules/day metre kelvin",
        "kJ/d.m.K",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 30.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 30.0, 0.0)
    db.AddUnit(
        "temperature per length",
        "degrees Celsius per thirty metre",
        "degC/30m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0, 0.0)
    db.AddUnit(
        "power",
        "joules/second",
        "J/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01157407, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01157407, 1.0, 0.0)
    db.AddUnit(
        "power",
        "kilojoules/day",
        "kJ/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 86400, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 86400, 0.0)
    db.AddUnit(
        "power",
        "joules/day",
        "J/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.01221, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.01221, 1.0, 0.0)
    db.AddUnit(
        "power",
        "British thermal unit/day",
        "Btu/d",
        f_base_to_unit,
        f_unit_to_base,
        default_category="heat flow rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 86400, 28.316846592, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 86400, 28.316846592, 0.0)
    db.AddUnit(
        "time per volume",
        "day per thousand cubic feet",
        "d/Mscf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 86400.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 86400.0, 0.0)
    db.AddUnit(
        "mass per time per area",
        "kilograms/square metre days",
        "kg/m2.d",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0001, 9.80665, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0001, 9.80665, 0.0)
    db.AddUnit(
        "compressibility",
        "per kilogram per square centimeter",
        "1/kgf/cm2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.757, 0.01, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.757, 0.01, 0.0)
    db.AddUnit(
        "pressure per length",
        "pound per square inch per centimeter",
        "psi/cm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 0.0001, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 0.0001, 0.0)
    db.AddUnit(
        "pressure per length",
        "kilogram per square centimeter per meter",
        "kgf/cm2/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "volume",
        "thousand cubic meters",
        "Mm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 3600, 0.0)
    db.AddUnit(
        "acceleration linear",
        "metres/minutes squared",
        "m/min2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.3048, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.3048, 3600, 0.0)
    db.AddUnit(
        "acceleration linear",
        "feet/minutes squared",
        "ft/min2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000.0, 1.0, 0.0)
    db.AddUnit(
        "specific volume",
        "liters/miligram",
        "l/mg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 60, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 60, 0.0)
    db.AddUnit(
        "mass flow rate",
        "gram per min",
        "g/min",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 3600, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 3600, 0.0)
    db.AddUnit(
        "mass flow rate",
        "grams per hour",
        "g/h",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "viscosity per pressure",
        "centipoise per kilopascal",
        "cP/kPa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000001450377377302092151542410280, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000001450377377302092151542410280, 1.0, 0.0)
    db.AddUnit(
        "viscosity per pressure",
        "centipoise per psi",
        "cP/psi",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00000001019716212977928242570092743, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00000001019716212977928242570092743, 1.0, 0.0)
    db.AddUnit(
        "viscosity per pressure",
        "centipoise per kilogram force per squared centimeter",
        "cP/(kgf/cm2)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 1.0, 0.0)
    db.AddUnit(
        "force per length",
        "kilogram force per meter",
        "kgf/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0, 0.0)
    db.AddUnit(
        "per time",
        "meters per second per meter",
        "(m/s)/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="shear rate",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 0.1589873, 0.0)
    db.AddUnit(
        "density",
        "gram/barrel",
        "g/bbl",
        f_base_to_unit,
        f_unit_to_base,
        default_category="concentration",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "electric field strength",
        "kilovolt per millimetre",
        "KV/mm",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "conductivity",
        "microsiemens/metre",
        "uS/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 100, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 100, 1.0, 0.0)
    db.AddUnit(
        "conductivity",
        "centisiemens/metre",
        "cS/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "conductivity",
        "kilosiemens/metre",
        "kS/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000000001, 1.0, 0.0)
    db.AddUnit(
        "capacitance", "femtofarads", "fF", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "capacitance", "millifarads", "mF", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "capacitance", "nanofarads", "nF", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000000001, 1.0, 0.0)
    db.AddUnit(
        "self inductance", "femtohenry", "fH", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000001, 1.0, 0.0)
    db.AddUnit(
        "self inductance",
        "picohenry",
        "picoH",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "magnetic permeability",
        "henry per kilometer",
        "H/km",
        f_base_to_unit,
        f_unit_to_base,
        default_category="self inductance per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "magnetic permeability",
        "milihenry per meter",
        "mH/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="self inductance per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "magnetic permeability",
        "nanohenry per meter",
        "nH/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category="self inductance per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000001, 1.0, 0.0)
    db.AddUnit(
        "magnetic permeability",
        "milihenry per kilometer",
        "mH/km",
        f_base_to_unit,
        f_unit_to_base,
        default_category="self inductance per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000001, 1.0, 0.0)
    db.AddUnit(
        "magnetic permeability",
        "microhenry per kilometer",
        "uH/km",
        f_base_to_unit,
        f_unit_to_base,
        default_category="self inductance per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.000000000001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.000000000001, 1.0, 0.0)
    db.AddUnit(
        "magnetic permeability",
        "nanohenry per kilometer",
        "nH/km",
        f_base_to_unit,
        f_unit_to_base,
        default_category="self inductance per length",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "volt ampere",
        "mega volt ampere",
        "MVA",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "volt ampere",
        "kilo volt ampere",
        "kVA",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000000, 1.0, 0.0)
    db.AddUnit(
        "volt ampere reactive",
        "mega volt ampere reactive",
        "MVAr",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "volt ampere reactive",
        "kilo volt ampere reactive",
        "kVAr",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "resistivity per length",
        "ohm per kilometer",
        "ohm/km",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 60, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 60, 1.0, 0.0)
    db.AddUnit(
        "stroke frequency",
        "strokes per second",
        "sps",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1000, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1000, 1.0, 0.0)
    db.AddUnit(
        "power per mass",
        "kilowatts/kilogram",
        "kW/kg",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "concentration per square time",
        "concentration per square time",
        "mg/l/d2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 57.29578778556937, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 57.29578778556937, 0.0)
    db.AddUnit(
        "angular acceleration",
        "degrees of an angle/second squared",
        "dega/s2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 206264.83602804973, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 206264.83602804973, 0.0)
    db.AddUnit(
        "angular acceleration",
        "degrees of an angle/minute squared",
        "dega/min2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6.283185307, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6.283185307, 1.0, 0.0)
    db.AddUnit(
        "angular acceleration",
        "revolutions/second squared",
        "rev/s2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 572.957795130823, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 572.957795130823, 0.0)
    db.AddUnit(
        "angular acceleration",
        "revolutions/minute squared",
        "rev/min2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0, 0.0)
    db.AddUnit(
        "density",
        "milligrams/cubic centimetre",
        "mg/cm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3.6e3, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3.6e3, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "kilowatt hours/tonne",
        "kW.h/t",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3265864920, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3265864920, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "kilowatt hours/U.S. ton",
        "kW.h/tonUS",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 3657769200, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 3657769200, 1.0, 0.0)
    db.AddUnit(
        "specific energy",
        "kilowatt hours/U.S. ton",
        "kW.h/tonUK",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0004299226139295, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0004299226139295, 1.0, 0.0)
    db.AddUnit(
        "mass per energy",
        "pounds mass/British thermal units",
        "lbm/Btu",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.334552563, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.334552563, 1.0, 0.0)
    db.AddUnit(
        "mass per energy",
        "pounds mass/Foot pounds force",
        "lbm/ft.lbf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1e-18, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1e-18, 1.0, 0.0)
    db.AddUnit(
        "volume", "cubic micrometres", "um3", f_base_to_unit, f_unit_to_base, default_category=None
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1e-18, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1e-18, 1.0, 0.0)
    db.AddUnit(
        "volume flow rate",
        "cubic micrometres/second",
        "um3/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0, 0.0)
    db.AddUnit(
        "specific heat capacity",
        "joules/kilogram degrees Celsius",
        "J/kg.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0, 0.0)
    db.AddUnit(
        "thermal conductivity",
        "watts/meter degrees Celsius",
        "W/m.degC",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1024, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1024, 1.0, 0.0)
    db.AddUnit(
        "computer binary memory",
        "kiloByte",
        "kByte",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1024 * 1024, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1024 * 1024, 1.0, 0.0)
    db.AddUnit(
        "computer binary memory",
        "megaByte",
        "MByte",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1024 * 1024 * 1024, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1024 * 1024 * 1024, 1.0, 0.0)
    db.AddUnit(
        "computer binary memory",
        "gigaByte",
        "GByte",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1024 * 1024 * 1024 * 1024, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1024 * 1024 * 1024 * 1024, 1.0, 0.0)
    db.AddUnit(
        "computer binary memory",
        "teraByte",
        "TByte",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1138419.9576606166, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1138419.9576606166, 0.0)
    db.AddUnit(
        "flow coefficient",
        "flow rate per pressure power of 0.5 ",
        "(m3/h)/(bar^0.5)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.0000630901964, 83.03467524575719, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.0000630901964, 83.03467524575719, 0.0)
    db.AddUnit(
        "flow coefficient",
        "galUs per pressure power of 0.5 ",
        "(galUS/min)/(psi^0.5)",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6.283185307, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6.283185307, 1.0, 0.0)
    db.AddUnit(
        "angular acceleration",
        "hertz per second",
        "Hz/s",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.00033333, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.00033333, 1.0, 0.0)
    db.AddUnit(
        "dimensionless",
        "total gas unit",
        "tgu",
        f_base_to_unit,
        f_unit_to_base,
        default_category="fluid gas concentration",
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 14.5939029372, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 14.5939029372, 1, 0.0)
    db.AddUnit(
        "force per velocity",
        "Pound force second per foot",
        "lbf.s/ft",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 175.126835246, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 175.126835246, 1, 0.0)
    db.AddUnit(
        "force per velocity",
        "Pound force second per inch",
        "lbf.s/in",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 1, 0.0)
    db.AddUnit(
        "force per velocity",
        "Kilogram force second per meter",
        "kgf.s/m",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.017453292519943, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.017453292519943, 0.0)
    db.AddUnit(
        "moment per angle",
        "Newton meter per angle",
        "Nm/dega",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 836.169044926, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 836.169044926, 1, 0.0)
    db.AddUnit(
        "moment per angle",
        "Pound force foot per angle",
        "lbf.ft/dega",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.35581794833, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.35581794833, 1, 0.0)
    db.AddUnit(
        "moment per angle",
        "Pound force foot per angle",
        "lbf.ft/rad",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6.47355385229, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6.47355385229, 1, 0.0)
    db.AddUnit(
        "moment per angle",
        "Pound force inch per angle",
        "lbf.in/dega",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.11298482902, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.11298482902, 1, 0.0)
    db.AddUnit(
        "moment per angle",
        "Pound force inch per angle",
        "lbf.in/rad",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 561.879656162, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 561.879656162, 1, 0.0)
    db.AddUnit(
        "moment per angle",
        "Kilogram force meter per angle",
        "kgf.m/dega",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 1, 0.0)
    db.AddUnit(
        "moment per angle",
        "Kilogram force meter per angle",
        "kgf.m/rad",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 0.017453292519943, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 0.017453292519943, 0.0)
    db.AddUnit(
        "moment per angular velocity",
        "newton meter per angular velocity",
        "Nms/dega",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.017453292519943, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.017453292519943, 1, 0.0)
    db.AddUnit(
        "moment per angular velocity",
        "Pound force foot per angular velocity",
        "lbf.ft.s/dega",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.35581794833, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.35581794833, 1, 0.0)
    db.AddUnit(
        "moment per angular velocity",
        "Pound force foot per angular velocity",
        "lbf.ft.s/rad",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6.47355385229, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6.47355385229, 1, 0.0)
    db.AddUnit(
        "moment per angular velocity",
        "Pound force inch per angular velocity",
        "lbf.in.s/dega",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.11298482902, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.11298482902, 1, 0.0)
    db.AddUnit(
        "moment per angular velocity",
        "Pound force inch per angular velocity",
        "lbf.in.s/rad",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 561.879656162, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 561.879656162, 1, 0.0)
    db.AddUnit(
        "moment per angular velocity",
        "Kilogram force meter per angular velocity",
        "kgf.m.s/dega",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 1, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 1, 0.0)
    db.AddUnit(
        "moment per angular velocity",
        "Kilogram force meter per angular velocity",
        "kgf.m.s/rad",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "mass temperature per mol",
        "g.K/mol",
        "g.K/mol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0, 0.0)
    db.AddUnit(
        "mass temperature per mol",
        "kg.degC/mol",
        "kg.degC/mol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.001, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.001, 1.0, 0.0)
    db.AddUnit(
        "mass temperature per mol",
        "g.degC/mol",
        "g.degC/mol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1000.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1000.0, 0.0)
    db.AddUnit(
        "mass temperature per mol",
        "kg.K/kmol",
        "kg.K/kmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1000.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1000.0, 0.0)
    db.AddUnit(
        "mass temperature per mol",
        "kg.degC/kmol",
        "kg.degC/kmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5.0, 9.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5.0, 9.0, 0.0)
    db.AddUnit(
        "mass temperature per mol",
        "kg.degF/mol",
        "kg.degF/mol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.005, 9.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.005, 9.0, 0.0)
    db.AddUnit(
        "mass temperature per mol",
        "g.degF/mol",
        "g.degF/mol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5.0, 9000.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5.0, 9000.0, 0.0)
    db.AddUnit(
        "mass temperature per mol",
        "kg.degF/kmol",
        "kg.degF/kmol",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0, 0.0)
    db.AddUnit(
        "joule-thomson coefficient",
        "delta degrees celsius per pascal",
        "degC/Pa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0e-5, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0e-5, 0.0)
    db.AddUnit(
        "joule-thomson coefficient",
        "delta degrees celsius per bar",
        "degC/bar",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0e-6, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0e-6, 0.0)
    db.AddUnit(
        "joule-thomson coefficient",
        "delta degrees celsius per megapascal",
        "degC/MPa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0e-5, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0e-5, 0.0)
    db.AddUnit(
        "joule-thomson coefficient",
        "delta kelvin per bar",
        "K/bar",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0e-6, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0e-6, 0.0)
    db.AddUnit(
        "joule-thomson coefficient",
        "delta kelvin per megapascal",
        "K/MPa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5.0, 9.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5.0, 9.0, 0.0)
    db.AddUnit(
        "joule-thomson coefficient",
        "delta degrees fahrenheit per pascal",
        "degF/Pa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5.0, 9.0e-5, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5.0, 9.0e-5, 0.0)
    db.AddUnit(
        "joule-thomson coefficient",
        "delta degrees fahrenheit per bar",
        "degF/bar",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5.0, 9.0e-6, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5.0, 9.0e-6, 0.0)
    db.AddUnit(
        "joule-thomson coefficient",
        "delta degrees fahrenheit per megapascal",
        "degF/MPa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5.0, 9.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5.0, 9.0, 0.0)
    db.AddUnit(
        "joule-thomson coefficient",
        "delta degrees rankine per pascal",
        "degR/Pa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5.0, 9.0e-5, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5.0, 9.0e-5, 0.0)
    db.AddUnit(
        "joule-thomson coefficient",
        "delta degrees rankine per bar",
        "degR/bar",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 5.0, 9.0e-6, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 5.0, 9.0e-6, 0.0)
    db.AddUnit(
        "joule-thomson coefficient",
        "delta degrees rankine per megapascal",
        "degR/MPa",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1.0, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1.0, 1.0, 0.0)
    db.AddUnit(
        "density derivative in respect to temperature",
        "kilogram per cubic meter Kelvin",
        "kg/m3.K",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.028262357, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.028262357, 0.1589873, 0.0)
    db.AddUnit(
        "standard volume per standard volume",
        "std cubic feet at 60 deg F/stock tank barrel",
        "scf(60F)/stb",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.9980757, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.9980757, 1.0, 0.0)
    db.AddUnit(
        "standard volume per standard volume",
        "std cubic feet at 60 deg Ft/std cubic foot",
        "scf(60F)/scf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "standard volume per standard volume",
        "stock tank barrels, 60 deg F/stock tank barrel",
        "stb(60F)/stb",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "standard volume per standard volume",
        "std cubic metres/std cubic metres",
        "sm3/sm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "standard volume per standard volume",
        "std cubic centimetres/std cubic centimetres",
        "scm3/scm3",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 1, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 1, 1.0, 0.0)
    db.AddUnit(
        "standard volume per standard volume",
        "stock tank barrels/stock tank barrels",
        "stb/stb",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28.262357, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28.262357, 0.1589873, 0.0)
    db.AddUnit(
        "standard volume per standard volume",
        "thousand std cubic feet/stock tank barrel",
        "Mscf/stb",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 28262.357, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 28262.357, 0.1589873, 0.0)
    db.AddUnit(
        "standard volume per standard volume",
        "million std cubic feet/stock tank barrel",
        "MMscf/stb",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.028262357, 0.1589873, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.028262357, 0.1589873, 0.0)
    db.AddUnit(
        "standard volume per standard volume",
        "std cubic feet/stock tank barrel",
        "scf/stb",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 0.028262357, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 0.028262357, 0.0)
    db.AddUnit(
        "standard volume per standard volume",
        "stock tank barrel/std cubic feet",
        "stb/scf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 0.1589873, 28262.357, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 0.1589873, 28262.357, 0.0)
    db.AddUnit(
        "standard volume per standard volume",
        "stock tank barrel/million std cubic feet",
        "stb/MMscf",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 47.8802631216, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 47.8802631216, 1.0, 0.0)
    db.AddUnit(
        "force per velocity squared",
        "Pound force second squared per foot squared",
        "lbf.s2/ft2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 6894.75788952, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 6894.75788952, 1.0, 0.0)
    db.AddUnit(
        "force per velocity squared",
        "Pound force second squared per inch squared",
        "lbf.s2/in2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    f_unit_to_base = MakeCustomaryToBase(0.0, 9.80665, 1.0, 0.0)
    f_base_to_unit = MakeBaseToCustomary(0.0, 9.80665, 1.0, 0.0)
    db.AddUnit(
        "force per velocity squared",
        "Kilogram force second squared per meter squared",
        "kgf.s2/m2",
        f_base_to_unit,
        f_unit_to_base,
        default_category=None,
    )
    if fill_categories:
        db.AddCategory(
            "reluctance", "reluctance", override=override_categories, valid_units=["1/H"]
        )
        db.AddCategory(
            "mole per mass",
            "mole per mass",
            override=override_categories,
            valid_units=["mol/kg", "mol/g", "lbmol/lb"],
            default_unit="mol/kg",
        )
        db.AddCategory(
            "molality",
            "mole per mass",
            override=override_categories,
            valid_units=["mol/kg", "mol/g", "lbmol/lb"],
            default_unit="mol/kg",
        )
        db.AddCategory(
            "linear thermal expansion",
            "volumetric thermal expansion",
            override=override_categories,
            valid_units=["1/K", "in/in.degF", "m/m.K", "mm/mm.K"],
        )
        db.AddCategory(
            "volumetric thermal expansion",
            "volumetric thermal expansion",
            override=override_categories,
            valid_units=["1/K", "1/degC", "1/degF", "1/degR", "ppm/degC", "ppm/degF"],
        )
        db.AddCategory(
            "per mass",
            "per mass",
            override=override_categories,
            valid_units=["1/kg", "1/g", "1/lbm"],
        )
        db.AddCategory(
            "area per volume",
            "per length",
            override=override_categories,
            valid_units=["b/cm3", "cu", "ft2/in3", "m2/cm3", "m2/m3", "sigma"],
        )
        db.AddCategory(
            "per length",
            "per length",
            override=override_categories,
            valid_units=[
                "1/m",
                "1/angstrom",
                "1/cm",
                "1/ft",
                "1/in",
                "1/mi",
                "1/mm",
                "1/nm",
                "1/yd",
            ],
        )
        db.AddCategory(
            "wave number",
            "per length",
            override=override_categories,
            valid_units=["1/m", "1/angstrom", "1/cm", "1/mm", "1/nm"],
        )
        db.AddCategory(
            "length per volume",
            "per area",
            override=override_categories,
            valid_units=[
                "ft/bbl",
                "ft/ft3",
                "ft/galUS",
                "km/dm3",
                "km/L",
                "m/m3",
                "mi/galUK",
                "mi/galUS",
            ],
        )
        db.AddCategory(
            "per area",
            "per area",
            override=override_categories,
            valid_units=["1/m2", "1/ft2", "1/km2", "1/mi2", "1/cm2"],
        )
        db.AddCategory(
            "per volume",
            "per volume",
            override=override_categories,
            valid_units=["1/m3", "1/bbl", "1/ft3", "1/galUK", "1/galUS", "1/L"],
        )
        db.AddCategory(
            "per force", "per force", override=override_categories, valid_units=["1/N", "1/lbf"]
        )
        db.AddCategory(
            "bulk compressibility",
            "compressibility",
            override=override_categories,
            valid_units=[
                "1/Pa",
                "1/bar",
                "1/kPa",
                "1/pPa",
                "1/psi",
                "1/upsi",
                "1/atm",
                "1/kgf/cm2",
            ],
        )
        db.AddCategory(
            "compressibility",
            "compressibility",
            override=override_categories,
            valid_units=[
                "1/Pa",
                "1/bar",
                "1/kPa",
                "1/pPa",
                "1/psi",
                "1/upsi",
                "1/atm",
                "1/kgf/cm2",
            ],
        )
        db.AddCategory(
            "viscosibility",
            "compressibility",
            override=override_categories,
            valid_units=[
                "1/Pa",
                "1/bar",
                "1/kPa",
                "1/pPa",
                "1/psi",
                "1/upsi",
                "1/atm",
                "1/kgf/cm2",
            ],
        )
        db.AddCategory(
            "operations per time",
            "per time",
            override=override_categories,
            valid_units=["1/s", "flops", "Mflops"],
        )
        db.AddCategory(
            "per time",
            "per time",
            override=override_categories,
            valid_units=["1/s", "1/a", "1/d", "1/h", "1/min", "1/wk", "kEuc/s"],
        )
        db.AddCategory(
            "shear rate", "per time", override=override_categories, valid_units=["1/s", "(m/s)/m"]
        )
        db.AddCategory(
            "volume per time per volume",
            "per time",
            override=override_categories,
            valid_units=["bbl/d.acre.ft"],
        )
        db.AddCategory(
            "per electric potential",
            "per electric potential",
            override=override_categories,
            valid_units=["1/V", "1/uV"],
        )
        db.AddCategory(
            "electric current",
            "electric current",
            override=override_categories,
            valid_units=["A", "kA", "mA", "MA", "nA", "pA", "uA"],
        )
        db.AddCategory(
            "magnetic potential difference",
            "electric current",
            override=override_categories,
            valid_units=["A", "kA", "mA", "MA", "nA", "pA", "uA"],
        )
        db.AddCategory(
            "magnetomotive force",
            "electric current",
            override=override_categories,
            valid_units=["A", "kA", "mA", "MA", "nA", "pA", "uA"],
        )
        db.AddCategory(
            "electromagnetic moment",
            "electromagnetic moment",
            override=override_categories,
            valid_units=["A.m2"],
        )
        db.AddCategory(
            "linear electric current density",
            "magnetization",
            override=override_categories,
            valid_units=["A/m", "A/mm", "gamma", "Oe"],
        )
        db.AddCategory(
            "magnetic field strength",
            "magnetization",
            override=override_categories,
            valid_units=["A/m", "A/mm", "gamma", "Oe"],
        )
        db.AddCategory(
            "magnetization",
            "magnetization",
            override=override_categories,
            valid_units=["A/m", "A/mm", "gamma", "Oe"],
        )
        db.AddCategory(
            "current density",
            "current density",
            override=override_categories,
            valid_units=["A/m2", "A/cm2", "A/ft2", "A/mm2", "mA/cm2", "mA/ft2", "uA/cm2", "uA/in2"],
        )
        db.AddCategory(
            "level of power intensity",
            "level of power intensity",
            override=override_categories,
            valid_units=["B", "dB"],
        )
        db.AddCategory(
            "attenuation per length",
            "attenuation per length",
            override=override_categories,
            valid_units=["B/m", "dB/ft", "dB/m", "dB/km"],
        )
        db.AddCategory(
            "attenuation", "attenuation", override=override_categories, valid_units=["B/O", "dB/O"]
        )
        db.AddCategory(
            "data transmission speed",
            "data transmission speed",
            override=override_categories,
            valid_units=["bps"],
        )
        db.AddCategory(
            "activity (of radioactivity)",
            "activity (of radioactivity)",
            override=override_categories,
            valid_units=[
                "Bq",
                "Ci",
                "curie",
                "GBq",
                "MBq",
                "mCi",
                "mcurie",
                "nCi",
                "ncurie",
                "pCi",
                "pcurie",
                "TBq",
                "uCi",
                "ucurie",
            ],
        )
        db.AddCategory(
            "specific activity (of radioactivity)",
            "specific activity (of radioactivity)",
            override=override_categories,
            valid_units=["Bq/kg", "pCi/g"],
        )
        db.AddCategory(
            "digital storage",
            "digital storage",
            override=override_categories,
            valid_units=["byte", "bit", "kbyte", "Mbyte"],
        )
        db.AddCategory(
            "electric capacity",
            "electric capacity",
            override=override_categories,
            valid_units=["C", "A.h", "fC", "kC", "mC", "nC", "pC", "uC"],
        )
        db.AddCategory(
            "electric charge",
            "electric capacity",
            override=override_categories,
            valid_units=["C", "A.h", "fC", "kC", "mC", "nC", "pC", "uC"],
        )
        db.AddCategory(
            "electric flux",
            "electric capacity",
            override=override_categories,
            valid_units=["C", "A.h", "fC", "kC", "mC", "nC", "pC", "uC"],
        )
        db.AddCategory(
            "electric dipole moment",
            "electric dipole moment",
            override=override_categories,
            valid_units=["C.m"],
        )
        db.AddCategory(
            "exposure (radioactivity)",
            "exposure (radioactivity)",
            override=override_categories,
            valid_units=["C/kg", "C/g"],
        )
        db.AddCategory(
            "electric polarization",
            "electric polarization",
            override=override_categories,
            valid_units=["C/m2", "C/cm2", "C/mm2", "mC/m2"],
        )
        db.AddCategory(
            "charge density",
            "charge density",
            override=override_categories,
            valid_units=["C/m3", "C/cm3", "C/mm3"],
        )
        db.AddCategory(
            "luminous intensity",
            "luminous intensity",
            override=override_categories,
            valid_units=["cd", "kcd"],
        )
        db.AddCategory(
            "luminance", "luminance", override=override_categories, valid_units=["cd/m2"]
        )
        db.AddCategory(
            "electrochemical equivalent",
            "electrochemical equivalent",
            override=override_categories,
            valid_units=["eq", "meq"],
        )
        db.AddCategory(
            "equivalent per mass",
            "equivalent per mass",
            override=override_categories,
            valid_units=["eq/kg", "meq/100g", "meq/g"],
        )
        db.AddCategory(
            "equivalent per volume",
            "equivalent per volume",
            override=override_categories,
            valid_units=["eq/m3", "eq/L", "meq/cm3", "meq/mL"],
        )
        db.AddCategory(
            "area per area",
            "dimensionless",
            override=override_categories,
            valid_units=["%", "in2/ft2", "in2/in2", "m2/m2", "mm2/mm2"],
        )
        db.AddCategory(
            "dimensionless",
            "dimensionless",
            override=override_categories,
            valid_units=["Euc", "%", "cEuc", "mEuc", "nEuc", "uEuc", "unitless", "ppmv", "-"],
        )
        db.AddCategory(
            "fluid gas concentration",
            "dimensionless",
            override=override_categories,
            valid_units=["Euc", "%", "ppm", "tgu"],
        )
        db.AddCategory(
            "force per force",
            "dimensionless",
            override=override_categories,
            valid_units=["%", "kgf/kgf", "lbf/lbf"],
        )
        db.AddCategory(
            "index", "dimensionless", override=override_categories, valid_units=["<ind>"]
        )
        db.AddCategory(
            "length per length",
            "dimensionless",
            override=override_categories,
            valid_units=[
                "%",
                "ft/100ft",
                "ft/ft",
                "ft/in",
                "ft/m",
                "ft/mi",
                "km/cm",
                "m/30m",
                "m/cm",
                "m/km",
                "m/m",
                "mi/in",
            ],
        )
        db.AddCategory(
            "linear concentration",
            "dimensionless",
            override=override_categories,
            valid_units=["ft/100ft", "ft/ft", "ft/m", "ft/mi", "m/30m", "m/km", "m/m"],
        )
        db.AddCategory(
            "linear strain",
            "dimensionless",
            override=override_categories,
            valid_units=["Euc", "%", "ft/100ft", "ft/ft", "ft/m", "ft/mi", "m/30m", "m/km", "m/m"],
        )
        db.AddCategory(
            "mass concentration",
            "dimensionless",
            override=override_categories,
            valid_units=[
                "Euc",
                "%",
                "g/kg",
                "kg/kg",
                "kg/sack94",
                "mg/kg",
                "permil",
                "ppdk",
                "ppk",
                "ppm",
                "wtpercent",
                "wtppm",
                "g/g",
                "mg/g",
                "g/100g",
                "lbm/lbm",
            ],
        )
        db.AddCategory(
            "mole per mole",
            "dimensionless",
            override=override_categories,
            valid_units=["mol/mol", "kmol/kmol", "lbmol/lbmol"],
        )
        db.AddCategory(
            "multiplier", "dimensionless", override=override_categories, valid_units=["<mult>"]
        )
        db.AddCategory(
            "percentage", "dimensionless", override=override_categories, valid_units=["%", "-"]
        )
        db.AddCategory(
            "poisson ratio",
            "dimensionless",
            override=override_categories,
            valid_units=["Euc", "cEuc", "mEuc", "nEuc", "uEuc"],
        )
        db.AddCategory(
            "relative elongation",
            "dimensionless",
            override=override_categories,
            valid_units=["%", "ft/100ft", "ft/ft", "ft/m", "ft/mi", "m/30m", "m/km", "m/m"],
        )
        db.AddCategory(
            "relative power",
            "dimensionless",
            override=override_categories,
            valid_units=["%", "Btu/bhp.hr", "W/kW", "W/W"],
        )
        db.AddCategory(
            "relative proportion",
            "dimensionless",
            override=override_categories,
            valid_units=["ppmv"],
        )
        db.AddCategory(
            "relative time", "dimensionless", override=override_categories, valid_units=["ms/s"]
        )
        db.AddCategory(
            "scale",
            "dimensionless",
            override=override_categories,
            valid_units=[
                "ft/100ft",
                "ft/ft",
                "ft/in",
                "ft/m",
                "ft/mi",
                "km/cm",
                "m/30m",
                "m/cm",
                "m/km",
                "m/m",
                "mi/in",
            ],
        )
        db.AddCategory(
            "shear strain",
            "dimensionless",
            override=override_categories,
            valid_units=["Euc", "in2/ft2", "in2/in2", "m2/m2", "mm2/mm2"],
        )
        db.AddCategory(
            "status", "dimensionless", override=override_categories, valid_units=["<stat>"]
        )
        db.AddCategory(
            "volume per volume",
            "dimensionless",
            override=override_categories,
            valid_units=[
                "Mcf/bbl",
                "bbl/100bbl",
                "bbl/bbl",
                "bbl/ft3",
                "bbl/Mcf",
                "bbl/MMcf",
                "cm3/cm3",
                "cm3/m3",
                "dm3/m3",
                "ft3/bbl",
                "ft3/ft3",
                "ksm3/sm3",
                "L/m3",
                "m3/m3",
                "mL/mL",
                "MMscf60/stb60",
                "Mscf60/stb60",
                "volpercent",
                "volppm",
                "m3/MMcf",
                "MMcf/bbl",
            ],
        )
        db.AddCategory(
            "volumic concentration",
            "dimensionless",
            override=override_categories,
            valid_units=["Euc", "%", "permil", "ppdk", "ppk", "ppm"],
        )
        db.AddCategory(
            "capacitance",
            "capacitance",
            override=override_categories,
            valid_units=["F", "pF", "uF", "fF", "mF", "nF"],
        )
        db.AddCategory(
            "permittivity",
            "permittivity",
            override=override_categories,
            valid_units=["F/m", "uF/m"],
        )
        db.AddCategory(
            "gamma ray API unit",
            "gamma ray API unit",
            override=override_categories,
            valid_units=["gAPI"],
        )
        db.AddCategory(
            "absorbed dose",
            "absorbed dose",
            override=override_categories,
            valid_units=["Gy", "mGy", "rd"],
        )
        db.AddCategory(
            "permeance",
            "self inductance",
            override=override_categories,
            valid_units=["H", "mH", "nH", "uH", "fH", "picoH"],
        )
        db.AddCategory(
            "self inductance",
            "self inductance",
            override=override_categories,
            valid_units=["H", "mH", "nH", "uH", "fH", "picoH"],
        )
        db.AddCategory(
            "magnetic permeability",
            "magnetic permeability",
            override=override_categories,
            valid_units=["H/m", "uH/m"],
        )
        db.AddCategory(
            "self inductance per length",
            "magnetic permeability",
            override=override_categories,
            valid_units=["H/m", "uH/m", "H/km", "mH/m", "nH/m", "mH/km", "uH/km", "nH/km"],
        )
        db.AddCategory(
            "angle per time",
            "frequency",
            override=override_categories,
            valid_units=["rad/s", "c/s", "dega/h", "dega/min", "dega/s", "rev/min", "rev/s", "rpm"],
        )
        db.AddCategory(
            "angular velocity",
            "frequency",
            override=override_categories,
            valid_units=["rad/s", "c/s"],
        )
        db.AddCategory(
            "circular frequency",
            "frequency",
            override=override_categories,
            valid_units=["rad/s", "c/s", "dega/h", "dega/min", "dega/s"],
        )
        db.AddCategory(
            "frequency",
            "frequency",
            override=override_categories,
            valid_units=["Hz", "GHz", "kHz", "MHz", "mHz", "uHz"],
        )
        db.AddCategory(
            "rotational frequency",
            "frequency",
            override=override_categories,
            valid_units=["rad/s", "c/s", "dega/h", "dega/min", "dega/s"],
        )
        db.AddCategory(
            "rotational velocity",
            "frequency",
            override=override_categories,
            valid_units=["rad/s", "c/s", "dega/h", "dega/min"],
        )
        db.AddCategory(
            "energy",
            "moment of force",
            override=override_categories,
            valid_units=[
                "J",
                "aJ",
                "Btu",
                "cal",
                "ch.h",
                "Chu",
                "CV.h",
                "EJ",
                "erg",
                "eV",
                "ft.lbf",
                "GeV",
                "GJ",
                "GW.h",
                "hp.hr",
                "kcal",
                "keV",
                "kJ",
                "kW.h",
                "MeV",
                "MJ",
                "mJ",
                "MW.h",
                "nJ",
                "quad",
                "TeV",
                "therm",
                "TJ",
                "TW.h",
                "uJ",
            ],
        )
        db.AddCategory(
            "moment of couple",
            "moment of force",
            override=override_categories,
            valid_units=[
                "J",
                "daN.m",
                "dN.m",
                "ft.lbf",
                "kft.lbf",
                "kgf.m",
                "kN.m",
                "lbf.ft",
                "lbf.in",
                "lbm.ft2/s2",
                "N.m",
                "pdl.ft",
                "tonfUS.ft",
                "tonfUS.mi",
            ],
        )
        db.AddCategory(
            "moment of force",
            "moment of force",
            override=override_categories,
            valid_units=[
                "J",
                "daN.m",
                "dN.m",
                "ft.lbf",
                "kft.lbf",
                "kgf.m",
                "kN.m",
                "lbf.ft",
                "lbf.in",
                "lbm.ft2/s2",
                "N.m",
                "pdl.ft",
                "tonfUS.ft",
                "tonfUS.mi",
            ],
        )
        db.AddCategory(
            "torque",
            "moment of force",
            override=override_categories,
            valid_units=[
                "J",
                "daN.m",
                "dN.m",
                "ft.lbf",
                "kft.lbf",
                "kgf.m",
                "kN.m",
                "lbf.ft",
                "lbf.in",
                "lbm.ft2/s2",
                "N.m",
                "pdl.ft",
                "tonfUS.ft",
                "tonfUS.mi",
            ],
        )
        db.AddCategory(
            "work",
            "moment of force",
            override=override_categories,
            valid_units=[
                "J",
                "aJ",
                "Btu",
                "cal",
                "ch.h",
                "Chu",
                "CV.h",
                "EJ",
                "erg",
                "eV",
                "GeV",
                "GJ",
                "GW.h",
                "hp.hr",
                "kcal",
                "keV",
                "kJ",
                "kW.h",
                "MeV",
                "MJ",
                "mJ",
                "MW.h",
                "nJ",
                "quad",
                "TeV",
                "therm",
                "TJ",
                "TW.h",
                "uJ",
            ],
        )
        db.AddCategory(
            "heat capacity", "heat capacity", override=override_categories, valid_units=["J/K"]
        )
        db.AddCategory(
            "specific energy",
            "specific energy",
            override=override_categories,
            valid_units=[
                "J/kg",
                "Btu/lbm",
                "cal/g",
                "cal/kg",
                "cal/lbm",
                "erg/g",
                "erg/kg",
                "ft.lbf/lbm",
                "hp.hr/lbm",
                "J/g",
                "kcal/g",
                "kcal/kg",
                "kJ/kg",
                "kW.h/kg",
                "lbf.ft/lbm",
                "MJ/kg",
                "MW.h/kg",
                "therm/lbm",
                "kW.h/t",
                "kW.h/tonUS",
                "kW.h/tonUK",
            ],
        )
        db.AddCategory(
            "massic heat capacity",
            "specific heat capacity",
            override=override_categories,
            valid_units=[
                "J/kg.K",
                "Btu/lbm.degF",
                "Btu/lbm.degR",
                "cal/g.K",
                "J/g.K",
                "kcal/kg.degC",
                "kJ/kg.K",
                "kW.h/kg.degC",
            ],
        )
        db.AddCategory(
            "specific entropy",
            "specific heat capacity",
            override=override_categories,
            valid_units=[
                "J/kg.K",
                "Btu/lbm.degF",
                "Btu/lbm.degR",
                "cal/g.K",
                "J/g.K",
                "kcal/kg.degC",
                "kJ/kg.K",
                "kW.h/kg.degC",
            ],
        )
        db.AddCategory(
            "specific heat capacity",
            "specific heat capacity",
            override=override_categories,
            valid_units=[
                "J/kg.K",
                "Btu/lbm.degF",
                "Btu/lbm.degR",
                "cal/g.K",
                "J/g.K",
                "kcal/kg.degC",
                "kJ/kg.K",
                "kW.h/kg.degC",
                "J/kg.degC",
            ],
        )
        db.AddCategory(
            "bulk modulus",
            "normal stress",
            override=override_categories,
            valid_units=[
                "J/m3",
                "Btu/bbl",
                "Btu/ft3",
                "Btu/galUK",
                "Btu/galUS",
                "cal/cm3",
                "cal/mL",
                "cal/mm3",
                "erg/cm3",
                "erg/m3",
                "ft.lbf/bbl",
                "ft.lbf/galUS",
                "hp.hr/bbl",
                "J/dm3",
                "kcal/cm3",
                "kcal/m3",
                "kJ/dm3",
                "kJ/m3",
                "kW.h/dm3",
                "kW.h/m3",
                "lbf.ft/bbl",
                "MJ/m3",
                "MW.h/m3",
                "therm/ft3",
                "therm/galUK",
                "tonfUS.mi/bbl",
            ],
        )
        db.AddCategory(
            "electromagnetic energy density",
            "normal stress",
            override=override_categories,
            valid_units=[
                "J/m3",
                "Btu/bbl",
                "Btu/ft3",
                "Btu/galUK",
                "Btu/galUS",
                "cal/cm3",
                "cal/mL",
                "cal/mm3",
                "erg/cm3",
                "erg/m3",
                "ft.lbf/bbl",
                "ft.lbf/galUS",
                "hp.hr/bbl",
                "J/dm3",
                "kcal/cm3",
                "kcal/m3",
                "kJ/dm3",
                "kJ/m3",
                "kW.h/dm3",
                "kW.h/m3",
                "lbf.ft/bbl",
                "MJ/m3",
                "MW.h/m3",
                "therm/ft3",
                "therm/galUK",
                "tonfUS.mi/bbl",
            ],
        )
        db.AddCategory(
            "modulus of compression",
            "normal stress",
            override=override_categories,
            valid_units=[
                "J/m3",
                "Btu/bbl",
                "Btu/ft3",
                "Btu/galUK",
                "Btu/galUS",
                "cal/cm3",
                "cal/mL",
                "cal/mm3",
                "erg/cm3",
                "erg/m3",
                "ft.lbf/bbl",
                "ft.lbf/galUS",
                "hp.hr/bbl",
                "J/dm3",
                "kcal/cm3",
                "kcal/m3",
                "kJ/dm3",
                "kJ/m3",
                "kW.h/dm3",
                "kW.h/m3",
                "lbf.ft/bbl",
                "MJ/m3",
                "MW.h/m3",
                "therm/ft3",
                "therm/galUK",
                "tonfUS.mi/bbl",
            ],
        )
        db.AddCategory(
            "modulus of elasticity",
            "normal stress",
            override=override_categories,
            valid_units=[
                "J/m3",
                "Btu/bbl",
                "Btu/ft3",
                "Btu/galUK",
                "Btu/galUS",
                "cal/cm3",
                "cal/mL",
                "cal/mm3",
                "erg/cm3",
                "erg/m3",
                "ft.lbf/bbl",
                "ft.lbf/galUS",
                "hp.hr/bbl",
                "J/dm3",
                "kcal/cm3",
                "kcal/m3",
                "kJ/dm3",
                "kJ/m3",
                "kW.h/dm3",
                "kW.h/m3",
                "lbf.ft/bbl",
                "MJ/m3",
                "MW.h/m3",
                "therm/ft3",
                "therm/galUK",
                "tonfUS.mi/bbl",
            ],
        )
        db.AddCategory(
            "modulus of rigidity",
            "normal stress",
            override=override_categories,
            valid_units=[
                "J/m3",
                "Btu/bbl",
                "Btu/ft3",
                "Btu/galUK",
                "Btu/galUS",
                "cal/cm3",
                "cal/mL",
                "cal/mm3",
                "erg/cm3",
                "erg/m3",
                "ft.lbf/bbl",
                "ft.lbf/galUS",
                "hp.hr/bbl",
                "J/dm3",
                "kcal/cm3",
                "kcal/m3",
                "kJ/dm3",
                "kJ/m3",
                "kW.h/dm3",
                "kW.h/m3",
                "lbf.ft/bbl",
                "MJ/m3",
                "MW.h/m3",
                "therm/ft3",
                "therm/galUK",
                "tonfUS.mi/bbl",
            ],
        )
        db.AddCategory(
            "normal stress",
            "normal stress",
            override=override_categories,
            valid_units=[
                "J/m3",
                "Btu/bbl",
                "Btu/ft3",
                "Btu/galUK",
                "Btu/galUS",
                "cal/cm3",
                "cal/mL",
                "cal/mm3",
                "erg/cm3",
                "erg/m3",
                "ft.lbf/bbl",
                "ft.lbf/galUS",
                "hp.hr/bbl",
                "J/dm3",
                "kcal/cm3",
                "kcal/m3",
                "kJ/dm3",
                "kJ/m3",
                "kW.h/dm3",
                "kW.h/m3",
                "lbf.ft/bbl",
                "MJ/m3",
                "MW.h/m3",
                "therm/ft3",
                "therm/galUK",
                "tonfUS.mi/bbl",
            ],
        )
        db.AddCategory(
            "radiant energy density",
            "normal stress",
            override=override_categories,
            valid_units=[
                "J/m3",
                "Btu/bbl",
                "Btu/ft3",
                "Btu/galUK",
                "Btu/galUS",
                "cal/cm3",
                "cal/mL",
                "cal/mm3",
                "erg/cm3",
                "erg/m3",
                "ft.lbf/bbl",
                "ft.lbf/galUS",
                "hp.hr/bbl",
                "J/dm3",
                "kcal/cm3",
                "kcal/m3",
                "kJ/dm3",
                "kJ/m3",
                "kW.h/dm3",
                "kW.h/m3",
                "lbf.ft/bbl",
                "MJ/m3",
                "MW.h/m3",
                "therm/ft3",
                "therm/galUK",
                "tonfUS.mi/bbl",
            ],
        )
        db.AddCategory(
            "shear modulus",
            "normal stress",
            override=override_categories,
            valid_units=[
                "J/m3",
                "Btu/bbl",
                "Btu/ft3",
                "Btu/galUK",
                "Btu/galUS",
                "cal/cm3",
                "cal/mL",
                "cal/mm3",
                "erg/cm3",
                "erg/m3",
                "ft.lbf/bbl",
                "ft.lbf/galUS",
                "hp.hr/bbl",
                "J/dm3",
                "kcal/cm3",
                "kcal/m3",
                "kJ/dm3",
                "kJ/m3",
                "kW.h/dm3",
                "kW.h/m3",
                "lbf.ft/bbl",
                "MJ/m3",
                "MW.h/m3",
                "therm/ft3",
                "therm/galUK",
                "tonfUS.mi/bbl",
            ],
        )
        db.AddCategory(
            "shear stress",
            "normal stress",
            override=override_categories,
            valid_units=[
                "J/m3",
                "Btu/bbl",
                "Btu/ft3",
                "Btu/galUK",
                "Btu/galUS",
                "cal/cm3",
                "cal/mL",
                "cal/mm3",
                "erg/cm3",
                "erg/m3",
                "ft.lbf/bbl",
                "ft.lbf/galUS",
                "hp.hr/bbl",
                "J/dm3",
                "kcal/cm3",
                "kcal/m3",
                "kJ/dm3",
                "kJ/m3",
                "kW.h/dm3",
                "kW.h/m3",
                "lbf.ft/bbl",
                "MJ/m3",
                "MW.h/m3",
                "therm/ft3",
                "therm/galUK",
                "tonfUS.mi/bbl",
            ],
        )
        db.AddCategory(
            "affinity of a chemical reaction",
            "molar thermodynamic energy",
            override=override_categories,
            valid_units=[
                "J/mol",
                "Btu/lbmol",
                "Btu/mol(lbm)",
                "kcal/mol",
                "kcal/mol(g)",
                "kJ/kmol",
                "kJ/mol(kg)",
                "kJ/mol",
                "MJ/kmol",
                "MJ/mol(kg)",
            ],
        )
        db.AddCategory(
            "chemical potential",
            "molar thermodynamic energy",
            override=override_categories,
            valid_units=[
                "J/mol",
                "Btu/lbmol",
                "Btu/mol(lbm)",
                "kcal/mol",
                "kcal/mol(g)",
                "kJ/kmol",
                "kJ/mol(kg)",
                "kJ/mol",
                "MJ/kmol",
                "MJ/mol(kg)",
            ],
        )
        db.AddCategory(
            "molar thermodynamic energy",
            "molar thermodynamic energy",
            override=override_categories,
            valid_units=[
                "J/mol",
                "Btu/lbmol",
                "Btu/mol(lbm)",
                "kcal/mol",
                "kcal/mol(g)",
                "kJ/kmol",
                "kJ/mol(kg)",
                "kJ/mol",
                "MJ/kmol",
                "MJ/mol(kg)",
            ],
        )
        db.AddCategory(
            "molar entropy",
            "molar heat capacity",
            override=override_categories,
            valid_units=[
                "J/mol.K",
                "Btu/lbmol.F",
                "Btu/mol(lbm).F",
                "cal/mol.degC",
                "cal/mol(g).degC",
                "kJ/kmol.K",
                "kJ/mol(kg).K",
            ],
        )
        db.AddCategory(
            "molar gas constant",
            "molar heat capacity",
            override=override_categories,
            valid_units=[
                "J/mol.K",
                "Btu/lbmol.F",
                "Btu/mol(lbm).F",
                "cal/mol.degC",
                "cal/mol(g).degC",
                "kJ/kmol.K",
                "kJ/mol(kg).K",
            ],
        )
        db.AddCategory(
            "molar heat capacity",
            "molar heat capacity",
            override=override_categories,
            valid_units=[
                "J/mol.K",
                "Btu/lbmol.F",
                "Btu/mol(lbm).F",
                "cal/mol.degC",
                "cal/mol(g).degC",
                "kJ/kmol.K",
                "kJ/mol(kg).K",
            ],
        )
        db.AddCategory(
            "delta temperature",
            "temperature",
            override=override_categories,
            valid_units=["K", "ddegC", "ddegF", "ddegK", "ddegR"],
        )
        db.AddCategory(
            "temperature",
            "temperature",
            override=override_categories,
            valid_units=["degC", "K", "degF", "degR"],
        )
        db.AddCategory(
            "thermodynamic temperature",
            "temperature",
            override=override_categories,
            valid_units=["K", "degC", "degF", "degR"],
        )
        db.AddCategory(
            "coefficient of thermal insulation",
            "thermal insulance",
            override=override_categories,
            valid_units=["K.m2/W", "degC.m2.h/kcal", "degF.ft2.h/Btu", "K.m2/kW"],
        )
        db.AddCategory(
            "thermal insulance",
            "thermal insulance",
            override=override_categories,
            valid_units=["K.m2/W", "degC.m2.h/kcal", "degF.ft2.h/Btu", "K.m2/kW"],
        )
        db.AddCategory(
            "temperature per length",
            "temperature per length",
            override=override_categories,
            valid_units=[
                "K/m",
                "degC/100m",
                "degC/ft",
                "degC/km",
                "degC/m",
                "degF/100ft",
                "degF/ft",
                "degF/ft(100)",
                "degF/m",
                "mK/m",
                "degC/30m",
            ],
        )
        db.AddCategory(
            "temperature per time",
            "temperature per time",
            override=override_categories,
            valid_units=["K/s", "degC/h", "degC/min", "degC/s", "degF/h", "degF/min", "degF/s"],
        )
        db.AddCategory(
            "thermal resistance",
            "thermal resistance",
            override=override_categories,
            valid_units=["K/W"],
        )
        db.AddCategory(
            "mass",
            "mass",
            override=override_categories,
            valid_units=[
                "kg",
                "ct",
                "g",
                "grain",
                "klbm",
                "lbm",
                "mg",
                "ozm",
                "t",
                "tonUK",
                "tonUS",
                "ug",
            ],
        )
        db.AddCategory(
            "mass length",
            "mass length",
            override=override_categories,
            valid_units=["kg.m", "ft.lbm"],
        )
        db.AddCategory(
            "impulse", "momentum", override=override_categories, valid_units=["kg.m/s", "lbm.ft/s"]
        )
        db.AddCategory(
            "momentum", "momentum", override=override_categories, valid_units=["kg.m/s", "lbm.ft/s"]
        )
        db.AddCategory(
            "moment of inertia",
            "moment of inertia",
            override=override_categories,
            valid_units=["kg.m2", "lbm.ft2"],
        )
        db.AddCategory(
            "mass per energy",
            "mass per energy",
            override=override_categories,
            valid_units=[
                "kg/J",
                "kg/kW.h",
                "t/kW.h",
                "kg/MJ",
                "lbm/hp.h",
                "mg/J",
                "lbm/Btu",
                "lbm/ft.lbf",
            ],
        )
        db.AddCategory(
            "linear density",
            "linear density",
            override=override_categories,
            valid_units=["kg/m", "klbm/in", "lbm/ft", "Mg/in"],
        )
        db.AddCategory(
            "linear mass", "linear density", override=override_categories, valid_units=["kg/m"]
        )
        db.AddCategory(
            "mass per length",
            "linear density",
            override=override_categories,
            valid_units=["kg/m", "kg.m/cm2", "klbm/in", "lbm/ft", "Mg/in"],
        )
        db.AddCategory(
            "areic mass",
            "surface density",
            override=override_categories,
            valid_units=["kg/m2", "lbm/100ft2", "lbm/ft2", "Mg/m2", "tonUS/ft2"],
        )
        db.AddCategory(
            "surface density",
            "surface density",
            override=override_categories,
            valid_units=["kg/m2", "lbm/100ft2", "lbm/ft2", "Mg/m2", "tonUS/ft2"],
        )
        db.AddCategory(
            "mass per time per area",
            "mass per time per area",
            override=override_categories,
            valid_units=[
                "kg/m2.s",
                "g.ft/cm3.s",
                "kPa.s/m",
                "lbm/h.ft2",
                "lbm/s.ft2",
                "MPa.s/m",
                "kg/m2.d",
            ],
        )
        db.AddCategory(
            "concentration",
            "density",
            override=override_categories,
            valid_units=[
                "kg/m3",
                "10Mg/m3",
                "g/cm3",
                "g/dm3",
                "g/galUK",
                "g/galUS",
                "g/L",
                "g/m3",
                "grain/100ft3",
                "grain/ft3",
                "kg/dm3",
                "kg/L",
                "lbm/ft3",
                "lbm/galUS",
                "mg/dm3",
                "mg/L",
                "g/bbl",
            ],
        )
        db.AddCategory(
            "density",
            "density",
            override=override_categories,
            valid_units=[
                "kg/m3",
                "10Mg/m3",
                "g/cm3",
                "g/dm3",
                "g/galUK",
                "g/galUS",
                "g/L",
                "g/m3",
                "grain/100ft3",
                "grain/ft3",
                "grain/ft3(100)",
                "grain/galUS",
                "kg/dm3",
                "kg/L",
                "lbm/1000galUK",
                "lbm/1000galUS",
                "lbm/10bbl",
                "lbm/bbl",
                "lbm/ft3",
                "lbm/galUK",
                "lbm/galUK(1000)",
                "lbm/galUS",
                "lbm/galUS(1000)",
                "lbm/in3",
                "lbm/Mbbl",
                "mg/dm3",
                "mg/galUS",
                "mg/L",
                "mg/m3",
                "Mg/m3",
                "ug/cm3",
                "mg/cm3",
            ],
        )
        db.AddCategory(
            "mass density",
            "density",
            override=override_categories,
            valid_units=[
                "kg/m3",
                "10Mg/m3",
                "g/cm3",
                "g/dm3",
                "g/galUK",
                "g/galUS",
                "g/L",
                "g/m3",
                "grain/100ft3",
                "grain/ft3",
                "grain/ft3(100)",
                "grain/galUS",
                "kg/dm3",
                "kg/L",
                "lbm/1000galUK",
                "lbm/1000galUS",
                "lbm/10bbl",
                "lbm/bbl",
                "lbm/ft3",
                "lbm/galUK",
                "lbm/galUK(1000)",
                "lbm/galUS",
                "lbm/galUS(1000)",
                "lbm/in3",
                "lbm/Mbbl",
                "mg/dm3",
                "mg/galUS",
                "mg/L",
                "mg/m3",
                "Mg/m3",
                "ug/cm3",
                "mg/cm3",
            ],
        )
        db.AddCategory(
            "volumic mass",
            "density",
            override=override_categories,
            valid_units=[
                "kg/m3",
                "10Mg/m3",
                "g/cm3",
                "g/dm3",
                "g/galUK",
                "g/galUS",
                "g/L",
                "g/m3",
                "grain/100ft3",
                "grain/ft3",
                "grain/ft3(100)",
                "grain/galUS",
                "kg/dm3",
                "kg/L",
                "lbm/1000galUK",
                "lbm/1000galUS",
                "lbm/10bbl",
                "lbm/bbl",
                "lbm/ft3",
                "lbm/galUK",
                "lbm/galUK(1000)",
                "lbm/galUS",
                "lbm/galUS(1000)",
                "lbm/in3",
                "lbm/Mbbl",
                "mg/dm3",
                "mg/galUS",
                "mg/L",
                "mg/m3",
                "Mg/m3",
                "ug/cm3",
                "mg/cm3",
            ],
        )
        db.AddCategory(
            "mass per volume per length",
            "mass per volume per length",
            override=override_categories,
            valid_units=["kg/m4", "g/cm4", "kg/dm4", "lbm/ft4", "lbm/galUK.ft", "lbm/galUS.ft"],
        )
        db.AddCategory(
            "mass flow rate",
            "mass flow rate",
            override=override_categories,
            valid_units=[
                "kg/s",
                "g/s",
                "kg/d",
                "kg/h",
                "kg/min",
                "lbm(million)/yr",
                "lbm/d",
                "lbm/h",
                "lbm/min",
                "lbm/s",
                "Mg/a",
                "Mg/d",
                "Mg/h",
                "Mlbm/yr",
                "t/a",
                "t/d",
                "t/h",
                "t/min",
                "tonUK/a",
                "tonUK/d",
                "tonUK/h",
                "tonUK/min",
                "tonUS/a",
                "tonUS/d",
                "tonUS/h",
                "tonUS/min",
                "g/min",
                "g/h",
            ],
        )
        db.AddCategory(
            "luminous flux", "luminous flux", override=override_categories, valid_units=["lm"]
        )
        db.AddCategory(
            "quantity of light",
            "quantity of light",
            override=override_categories,
            valid_units=["lm.s", "talbot"],
        )
        db.AddCategory(
            "luminous efficacy",
            "luminous efficacy",
            override=override_categories,
            valid_units=["lm/W"],
        )
        db.AddCategory(
            "illuminance",
            "illuminance",
            override=override_categories,
            valid_units=["lx", "footcandle", "klx"],
        )
        db.AddCategory(
            "luminous exitance", "illuminance", override=override_categories, valid_units=["lm/m2"]
        )
        db.AddCategory(
            "light exposure",
            "light exposure",
            override=override_categories,
            valid_units=["lx.s", "footcandle.s"],
        )
        db.AddCategory(
            "Cartesian coordinates",
            "length",
            override=override_categories,
            valid_units=["m", "cm", "dm", "ft", "in", "km", "mi", "mm", "yd"],
        )
        db.AddCategory(
            "breadth",
            "length",
            override=override_categories,
            valid_units=["m", "cm", "dm", "ft", "in", "km", "mi", "mm", "nm", "pm", "um", "yd"],
        )
        db.AddCategory("depth", "length", override=override_categories, valid_units=["m"])
        db.AddCategory(
            "diameter",
            "length",
            override=override_categories,
            valid_units=["m", "cm", "dm", "ft", "in", "km", "mi", "mm", "nm", "pm", "um", "yd"],
        )
        db.AddCategory(
            "distance",
            "length",
            override=override_categories,
            valid_units=["m", "cm", "dm", "ft", "in", "km", "mi", "mm", "yd"],
        )
        db.AddCategory(
            "height",
            "length",
            override=override_categories,
            valid_units=["m", "cm", "dm", "ft", "in", "km", "mi", "mm", "nm", "pm", "um", "yd"],
        )
        db.AddCategory(
            "length",
            "length",
            override=override_categories,
            valid_units=["m", "cm", "dm", "ft", "in", "km", "mi", "mm", "nm", "pm", "um", "yd"],
        )
        db.AddCategory(
            "length of path",
            "length",
            override=override_categories,
            valid_units=["m", "cm", "dm", "ft", "in", "km", "mi", "mm", "nm", "pm", "um", "yd"],
        )
        db.AddCategory(
            "mean free path",
            "length",
            override=override_categories,
            valid_units=["m", "cm", "dm", "ft", "in", "km", "mm", "nm", "pm", "um"],
        )
        db.AddCategory(
            "radius",
            "length",
            override=override_categories,
            valid_units=["m", "cm", "dm", "ft", "in", "km", "mi", "mm", "nm", "pm", "um", "yd"],
        )
        db.AddCategory(
            "radius of curvature",
            "length",
            override=override_categories,
            valid_units=["m", "cm", "dm", "ft", "in", "km", "mi", "mm", "nm", "pm", "um", "yd"],
        )
        db.AddCategory(
            "thickness",
            "length",
            override=override_categories,
            valid_units=["m", "cm", "dm", "ft", "in", "km", "mi", "mm", "nm", "pm", "um", "yd"],
        )
        db.AddCategory(
            "volume per area",
            "length",
            override=override_categories,
            valid_units=["bbl/acre", "m3/m2"],
        )
        db.AddCategory(
            "wavelength",
            "length",
            override=override_categories,
            valid_units=["m", "cm", "dm", "ft", "in", "km", "mi", "mm", "nm", "pm", "um"],
        )
        db.AddCategory(
            "length per temperature",
            "length per temperature",
            override=override_categories,
            valid_units=["m/K", "ft/degF"],
        )
        db.AddCategory(
            "velocity",
            "velocity",
            override=override_categories,
            valid_units=[
                "m/s",
                "cm/a",
                "cm/s",
                "dm/s",
                "ft/d",
                "ft/h",
                "ft/min",
                "ft/ms",
                "ft/s",
                "ft/us",
                "m/us",
                "in/a",
                "in/min",
                "in/s",
                "kft/h",
                "kft/s",
                "km/h",
                "km/s",
                "knot",
                "m/d",
                "m/h",
                "m/min",
                "m/ms",
                "mi/h",
                "mil/yr",
                "mm/a",
                "mm/s",
                "nm/s",
                "um/s",
                "cm/d",
            ],
        )
        db.AddCategory(
            "volume per time per area",
            "velocity",
            override=override_categories,
            valid_units=[
                "ft3/min.ft2",
                "ft3/s.ft2",
                "galUK/hr.ft2",
                "galUK/hr.in2",
                "galUK/min.ft2",
                "galUS/hr.ft2",
                "galUS/hr.in2",
                "galUS/min.ft2",
                "m3/s.m2",
            ],
        )
        db.AddCategory(
            "acceleration linear",
            "acceleration linear",
            override=override_categories,
            valid_units=["m/s2", "cm/s2", "ft/s2", "Gal", "gn", "mGal", "mgn", "m/min2", "ft/min2"],
        )
        db.AddCategory(
            "area",
            "area",
            override=override_categories,
            valid_units=[
                "m2",
                "acre",
                "b",
                "cm2",
                "ft2",
                "ha",
                "in2",
                "km2",
                "mi2",
                "miUS2",
                "mm2",
                "sq ft",
                "sq in",
                "sq mi",
                "sq yd",
                "um2",
                "yd2",
            ],
        )
        db.AddCategory(
            "permeability rock", "area", override=override_categories, valid_units=["m2", "D", "mD"]
        )
        db.AddCategory(
            "volume per length",
            "area",
            override=override_categories,
            valid_units=[
                "bbl/ft",
                "bbl/in",
                "bbl/mi",
                "dm3/100km",
                "dm3/km(100)",
                "dm3/m",
                "ft3/ft",
                "galUK/mi",
                "galUS/ft",
                "galUS/mi",
                "in3/ft",
                "L/100km",
                "L/km(100)",
                "L/m",
                "m3/km",
                "m3/m",
                "bbl/m",
            ],
        )
        db.AddCategory(
            "mass attenuation coefficient",
            "mass attenuation coefficient",
            override=override_categories,
            valid_units=["m2/kg", "cm2/g", "m2/g"],
        )
        db.AddCategory(
            "cross section absorption",
            "cross section absorption",
            override=override_categories,
            valid_units=["m2/mol", "b/elec"],
        )
        db.AddCategory(
            "mobility",
            "unit productivity index",
            override=override_categories,
            valid_units=["m2/Pa.s", "mD.ft2/lbf.s", "mD.in2/lbf.s", "mD/cP", "mD/Pa.s"],
        )
        db.AddCategory(
            "unit productivity index",
            "unit productivity index",
            override=override_categories,
            valid_units=["m2/Pa.s", "bbl/d.ft.psi", "ft3/d.ft.psi", "m2/d.kPa"],
        )
        db.AddCategory(
            "area per time",
            "volume per time per length",
            override=override_categories,
            valid_units=[
                "m2/s",
                "cm2/s",
                "St",
                "cSt",
                "ft2/h",
                "ft2/s",
                "in2/s",
                "m2/h",
                "mm2/s",
                "m2/d",
                "ft2/d",
            ],
        )
        db.AddCategory(
            "diffusion coefficient",
            "volume per time per length",
            override=override_categories,
            valid_units=["m2/s"],
        )
        db.AddCategory(
            "kinematic viscosity",
            "volume per time per length",
            override=override_categories,
            valid_units=[
                "m2/s",
                "cm2/s",
                "St",
                "cSt",
                "ft2/h",
                "ft2/s",
                "in2/s",
                "m2/h",
                "mm2/s",
                "m2/d",
                "ft2/d",
            ],
        )
        db.AddCategory(
            "thermal diffusivity",
            "volume per time per length",
            override=override_categories,
            valid_units=[
                "m2/s",
                "cm2/s",
                "ft2/h",
                "ft2/s",
                "in2/s",
                "m2/h",
                "mm2/s",
                "m2/d",
                "ft2/d",
            ],
        )
        db.AddCategory(
            "volume per time per length",
            "volume per time per length",
            override=override_categories,
            valid_units=[
                "Mcf/d.ft",
                "Mm3/d.m",
                "Mm3/h.m",
                "bbl/d.ft",
                "galUK/hr.ft",
                "galUK/hr.in",
                "galUK/min.ft",
                "galUS/hr.ft",
                "galUS/hr.in",
                "galUS/min.ft",
                "m3/d.m",
                "m3/h.m",
                "m3/s.ft",
                "m3/s.m",
            ],
        )
        db.AddCategory(
            "permeability length",
            "volume",
            override=override_categories,
            valid_units=["D.ft", "D.m", "mD.ft", "mD.m"],
        )
        db.AddCategory(
            "volume",
            "volume",
            override=override_categories,
            valid_units=[
                "m3",
                "Mcf",
                "bbl",
                "bcf",
                "cm3",
                "cu ft",
                "cu in",
                "dm3",
                "ft3",
                "galUK",
                "galUS",
                "hL",
                "in3",
                "L",
                "MMcf",
                "MMm3",
                "Mbbl",
                "mL",
                "mm3",
                "MMbbl",
                "tcf",
                "Mm3",
                "um3",
            ],
        )
        db.AddCategory(
            "isothermal compressibility",
            "isothermal compressibility",
            override=override_categories,
            valid_units=["m3/J", "dm3/kW.h", "dm3/MJ", "m3/kW.h", "mm3/J", "ptUK/hp.hr"],
        )
        db.AddCategory(
            "massic volume",
            "specific volume",
            override=override_categories,
            valid_units=[
                "m3/kg",
                "bbl/tonUK",
                "bbl/tonUS",
                "cm3/g",
                "dm3/kg",
                "dm3/t",
                "ft3/kg",
                "ft3/lbm",
                "ft3/sack94",
                "gal/sack",
                "galUK/lbm",
                "galUS/lbm",
                "galUS/sack94",
                "galUS/tonUK",
                "galUS/tonUS",
                "L/100kg",
                "L/kg",
                "L/t",
                "L/tonUK",
                "m3/g",
                "m3/t",
                "m3/tonUK",
                "m3/tonUS",
                "l/mg",
            ],
        )
        db.AddCategory(
            "specific volume",
            "specific volume",
            override=override_categories,
            valid_units=[
                "m3/kg",
                "bbl/tonUK",
                "bbl/tonUS",
                "cm3/g",
                "dm3/kg",
                "dm3/t",
                "ft3/kg",
                "ft3/lbm",
                "ft3/sack94",
                "gal/sack",
                "galUK/lbm",
                "galUS/lbm",
                "galUS/sack94",
                "galUS/tonUK",
                "galUS/tonUS",
                "L/100kg",
                "L/kg",
                "L/t",
                "L/tonUK",
                "m3/g",
                "m3/t",
                "m3/tonUK",
                "m3/tonUS",
                "l/mg",
            ],
        )
        db.AddCategory(
            "molar volume",
            "molar volume",
            override=override_categories,
            valid_units=[
                "m3/mol",
                "dm3/kmol",
                "dm3/mol(kg)",
                "ft3/lbmol",
                "ft3/mol(lbm)",
                "L/mol",
                "L/mol(g)",
                "L/kmol",
                "L/mol(kg)",
                "m3/kmol",
                "m3/mol(kg)",
            ],
        )
        db.AddCategory(
            "productivity index",
            "productivity index",
            override=override_categories,
            valid_units=[
                "m3/Pa.s",
                "Mcf/psi.d",
                "ft3/psi.d",
                "bbl/d.psi",
                "bbl/kPa.d",
                "bbl/psi.d",
                "L/bar.min",
                "m3/bar.d",
                "m3/bar.h",
                "m3/bar.min",
                "m3/d.kPa",
                "m3/kPa.d",
                "m3/kPa.h",
                "m3/psi.d",
                "m3/d/kgf/cm2",
            ],
        )
        db.AddCategory(
            "specific productivity index",
            "specific productivity index",
            override=override_categories,
            valid_units=["m3/Pa2.s2", "bbl/cP.d.psi", "m3/cP.d.kPa", "m3/cP.Pa.s"],
        ),
        db.AddCategory(
            "forchheimer linear productivity index",
            "forchheimer linear productivity index",
            override=override_categories,
            valid_units=["Pa2.s/scm", "Pa2.d/scm", "psi2.d/scf", "psi2.d/Mscf", "bar2.d/scm"],
        )
        db.AddCategory(
            "forchheimer quadratic productivity index",
            "forchheimer quadratic productivity index",
            override=override_categories,
            valid_units=[
                "Pa2.s2/scm2",
                "Pa2.d2/scm2",
                "psi2.d2/scf2",
                "psi2.d2/Mscf2",
                "bar2.d2/scm2",
            ],
        )
        db.AddCategory(
            "volume flow rate",
            "volume flow rate",
            override=override_categories,
            valid_units=[
                "m3/s",
                "Mcf/d",
                "Mm3/d",
                "Mm3/h",
                "bbl/s",
                "bbl/d",
                "bbl/hr",
                "bbl/min",
                "cm3/30min",
                "cm3/h",
                "cm3/min",
                "cm3/s",
                "dm3/s",
                "ft3/d",
                "ft3/h",
                "ft3/min",
                "ft3/s",
                "galUK/d",
                "galUK/hr",
                "galUK/min",
                "galUS/d",
                "galUS/hr",
                "galUS/min",
                "kbbl/d",
                "L/h",
                "L/min",
                "L/s",
                "MMcf/d",
                "MMm3/d",
                "m3/d",
                "m3/h",
                "m3/min",
                "Mbbl/d",
                "um3/s",
            ],
        )
        db.AddCategory(
            "volume per time per time",
            "volume per time per time",
            override=override_categories,
            valid_units=[
                "m3/s2",
                "bbl/d2",
                "bbl/hr2",
                "dm3/s2",
                "ft3/d2",
                "ft3/h2",
                "ft3/min2",
                "ft3/s2",
                "galUK/hr2",
                "galUK/min2",
                "galUS/hr2",
                "galUS/min2",
                "L/s2",
                "m3/d2",
            ],
        )
        db.AddCategory(
            "volume per standard volume",
            "volume per standard volume",
            override=override_categories,
            valid_units=[
                "m3/scm(15C)",
                "acre.ft/MMstb",
                "bbl/MMscf(60F)",
                "bbl/stb(60F)",
                "ft3/scf(60F)",
                "galUS/Mscf(60F)",
                "m3/sm3",
                "cm3/scm3",
                "bbl/stb",
                "bbl/Mscf",
            ],
        )
        db.AddCategory(
            "moment of section",
            "second moment of area",
            override=override_categories,
            valid_units=["m4"],
        )
        db.AddCategory(
            "second moment of area",
            "second moment of area",
            override=override_categories,
            valid_units=["m4", "cm4", "in4"],
        )
        db.AddCategory(
            "volume length per time",
            "volume length per time",
            override=override_categories,
            valid_units=["m4/s", "1000m4/d", "Mbbl.ft/d"],
        )
        db.AddCategory(
            "amount of substance",
            "molar mass",
            override=override_categories,
            valid_units=[
                "mol",
                "kmol",
                "m3(std,0C)",
                "m3(std,15C)",
                "mmol",
                "mol(g)",
                "mol(kg)",
                "lbmol",
                "mol(lbm)",
                "umol",
                "kgmol",
            ],
        )
        db.AddCategory(
            "molar mass",
            "molar mass",
            override=override_categories,
            valid_units=["lbmol", "gmol"],
        )
        db.AddCategory(
            "mole per area", "mole per area", override=override_categories, valid_units=["mol/m2"]
        )
        db.AddCategory(
            "mole per time per area",
            "mole per time per area",
            override=override_categories,
            valid_units=[
                "mol/m2.s",
                "mol(lbm)/h.ft2",
                "lbmol/h.ft2",
                "lbmol/s.ft2",
                "mol(lbm)/s.ft2",
            ],
        )
        db.AddCategory(
            "amount of a substance",
            "concentration of B",
            override=override_categories,
            valid_units=[
                "mol/m3",
                "kmol/m3",
                "mol(kg)/m3",
                "lbmol/ft3",
                "mol(lbm)/ft3",
                "lbmol/galUK",
                "mol(lbm)/galUK",
                "lbmol/galUS",
                "mol(lbm)/galUS",
                "gmol/m3",
                "mol/L",
                "mol/cm3",
                "lbmol/bbl",
            ],
        )
        db.AddCategory(
            "concentration of B",
            "concentration of B",
            override=override_categories,
            valid_units=[
                "mol/m3",
                "kmol/m3",
                "mol(kg)/m3",
                "lbmol/ft3",
                "mol(lbm)/ft3",
                "lbmol/galUK",
                "mol(lbm)/galUK",
                "lbmol/galUS",
                "mol(lbm)/galUS",
                "gmol/m3",
                "mol/L",
                "mol/cm3",
                "lbmol/bbl",
            ],
        )
        db.AddCategory(
            "mole per time",
            "mole per time",
            override=override_categories,
            valid_units=[
                "mol/s",
                "kmol/h",
                "mol(kg)/h",
                "kmol/s",
                "mol(kg)/s",
                "lbmol/h",
                "mol(lbm)/h",
                "lbmol/s",
                "mol(lbm)/s",
                "mol/h",
                "kmol/d",
                "mol/d",
                "lbmol/d",
            ],
        )
        db.AddCategory(
            "energy length per area",
            "force",
            override=override_categories,
            valid_units=["kcal.m/cm2"],
        )
        db.AddCategory(
            "energy per length", "force", override=override_categories, valid_units=["J/m", "MJ/m"]
        )
        db.AddCategory(
            "force",
            "force",
            override=override_categories,
            valid_units=[
                "N",
                "daN",
                "dyne",
                "gf",
                "kdyne",
                "kgf",
                "klbf",
                "kN",
                "lbf",
                "Mgf",
                "MN",
                "mN",
                "ozf",
                "pdl",
                "tonfUK",
                "tonfUS",
                "uN",
            ],
        )
        db.AddCategory(
            "force length per length",
            "force",
            override=override_categories,
            valid_units=["kgf.m/m", "lbf.ft/in", "lbf.in/in", "N.m/m", "tonfUS.mi/ft"],
        )
        db.AddCategory(
            "force area",
            "force area",
            override=override_categories,
            valid_units=[
                "N.m2",
                "dyne.cm2",
                "kgf.m2",
                "kN.m2",
                "lbf.in2",
                "mN.m2",
                "pdl.cm2",
                "tonfUK.ft2",
                "tonfUS.ft2",
            ],
        )
        db.AddCategory(
            "energy per area",
            "force per length",
            override=override_categories,
            valid_units=[
                "N/m",
                "erg/cm2",
                "J/cm2",
                "J/m2",
                "kgf.m/cm2",
                "lbf.ft/in2",
                "lbf/ft",
                "mJ/cm2",
                "mJ/m2",
            ],
        )
        db.AddCategory(
            "force per length",
            "force per length",
            override=override_categories,
            valid_units=[
                "N/m",
                "dyne/cm",
                "kgf/cm",
                "kN/m",
                "lbf/100ft",
                "lbf/30m",
                "lbf/ft",
                "lbf/in",
                "mN/km",
                "mN/m",
                "N/30m",
                "pdl/cm",
                "tonfUK/ft",
                "tonfUS/ft",
                "kgf/m",
            ],
        )
        db.AddCategory(
            "force per volume",
            "force per volume",
            override=override_categories,
            valid_units=["N/m3", "lbf/ft3", "lbf/galUS"],
        )
        db.AddCategory(
            "parachor",
            "parachor",
            override=override_categories,
            valid_units=["N4/kg.m7", "(dyne/cm)4/gcm3", "(N/m)4/kg.m3"],
        )
        db.AddCategory(
            "neutron API unit",
            "neutron API unit",
            override=override_categories,
            valid_units=["nAPI"],
        )
        db.AddCategory(
            "frequency interval",
            "frequency interval",
            override=override_categories,
            valid_units=["O"],
        )
        db.AddCategory(
            "impedance",
            "resistance",
            override=override_categories,
            valid_units=["ohm", "Gohm", "kohm", "Mohm", "mohm", "nohm", "Tohm", "uohm"],
        )
        db.AddCategory(
            "resistance",
            "resistance",
            override=override_categories,
            valid_units=["ohm", "Gohm", "kohm", "Mohm", "mohm", "nohm", "Tohm", "uohm"],
        )
        db.AddCategory(
            "electrical resistivity",
            "electrical resistivity",
            override=override_categories,
            valid_units=["ohm.m", "kohm.m", "ohm.cm"],
        )
        db.AddCategory(
            "resistivity per length",
            "resistivity per length",
            override=override_categories,
            valid_units=["ohm/m", "uohm/ft", "uohm/m", "ohm/km"],
        )
        db.AddCategory(
            "force per area",
            "pressure",
            override=override_categories,
            valid_units=[
                "Pa",
                "atm",
                "bar",
                "cmH2O(4degC)",
                "dyne/cm2",
                "GPa",
                "hbar",
                "inH2O(39.2F)",
                "inH2O(60F)",
                "inHg(32F)",
                "inHg(60F)",
                "kgf/cm2",
                "kgf/cm2(g)",
                "kgf/mm2",
                "kN/m2",
                "kPa",
                "kPa(g)",
                "kpsi",
                "lbf/100ft2",
                "lbf/ft2",
                "lbf/in2",
                "mbar",
                "mPa",
                "MPa",
                "N/m2",
                "N/mm2",
                "psf",
                "psi",
                "psia",
                "psig",
                "tonfUS/ft2",
                "tonfUS/in2",
                "torr",
                "ubar",
                "uPa",
                "upsi",
                "Pa(g)",
                "bar(g)",
            ],
        )
        db.AddCategory(
            "pressure",
            "pressure",
            override=override_categories,
            valid_units=[
                "Pa",
                "atm",
                "bar",
                "cmH2O(4degC)",
                "dyne/cm2",
                "GPa",
                "hbar",
                "inH2O(39.2F)",
                "inH2O(60F)",
                "inHg(32F)",
                "inHg(60F)",
                "kgf/cm2",
                "kgf/cm2(g)",
                "kgf/mm2",
                "kN/m2",
                "kPa",
                "kPa(g)",
                "kpsi",
                "lbf/100ft2",
                "lbf/ft2",
                "lbf/in2",
                "mbar",
                "mPa",
                "MPa",
                "N/m2",
                "N/mm2",
                "psf",
                "psi",
                "psia",
                "psig",
                "tonfUK/ft2",
                "tonfUS/ft2",
                "tonfUS/in2",
                "torr",
                "ubar",
                "uPa",
                "upsi",
                "Pa(g)",
                "bar(g)",
            ],
        )
        db.AddCategory(
            "yield stress",
            "pressure",
            override=override_categories,
            valid_units=["Pa", "lbf/100ft2"],
        )
        db.AddCategory(
            "dynamic viscosity",
            "mass per time per length",
            override=override_categories,
            valid_units=[
                "Pa.s",
                "cP",
                "dyne.s/cm2",
                "kgf.s/m2",
                "lbf.s/ft2",
                "lbf.s/in2",
                "mPa.s",
                "N.s/m2",
                "P",
                "psi.s",
                "kPa.d",
                "kPa.s",
                "MPa.s",
            ],
        )
        db.AddCategory(
            "mass per time per length",
            "mass per time per length",
            override=override_categories,
            valid_units=["Pa.s", "kg/m.s", "lbm/ft.h", "lbm/ft.s", "lbm/h.ft", "lbm/s.ft"],
        )
        db.AddCategory(
            "acoustic impedance",
            "pressure time per volume",
            override=override_categories,
            valid_units=["Pa.s/m3"],
        )
        db.AddCategory(
            "pressure time per volume",
            "pressure time per volume",
            override=override_categories,
            valid_units=["Pa.s/m3", "psi.d/bbl"],
        )
        db.AddCategory(
            "nonDarcy flow coefficient",
            "nonDarcy flow coefficient",
            override=override_categories,
            valid_units=["Pa.s/m6", "psi2.d2/cP.ft6", "psi2.d2/cp.ft6"],
        )
        db.AddCategory(
            "pressure per length",
            "pressure per length",
            override=override_categories,
            valid_units=[
                "Pa/m",
                "atm/ft",
                "atm/hm",
                "atm/m",
                "bar/km",
                "bar/m",
                "GPa/cm",
                "kPa/100m",
                "kPa/m",
                "MPa/m",
                "psi/100ft",
                "psi/ft",
                "psi/ft(100)",
                "psi/kft",
                "psi/m",
                "psi/cm",
                "kgf/cm2/m",
            ],
        )
        db.AddCategory(
            "Darcy flow coefficient",
            "Darcy flow coefficient",
            override=override_categories,
            valid_units=["Pa/m3", "psi2.d/cP.ft3", "psi2.d/cp.ft3"],
        )
        db.AddCategory(
            "pressure per time",
            "pressure per time",
            override=override_categories,
            valid_units=[
                "Pa/s",
                "atm/h",
                "bar/h",
                "kPa/h",
                "kPa/min",
                "MPa/h",
                "Pa/h",
                "psi/h",
                "psi/min",
                "kPa/d",
                "psi/d",
            ],
        )
        db.AddCategory(
            "pressure squared per (dynamic viscosity)",
            "pressure per time",
            override=override_categories,
            valid_units=["bar2/cP", "kPa2/cP", "kPa2/kcP", "psi2/cP"],
        )
        db.AddCategory(
            "pressure squared",
            "pressure squared",
            override=override_categories,
            valid_units=["Pa2", "bar2", "GPa2", "kPa2", "kpsi2", "psi2"],
        )
        db.AddCategory("pH", "pH", override=override_categories, valid_units=["pH"])
        db.AddCategory(
            "plane angle",
            "plane angle",
            override=override_categories,
            valid_units=[
                "rad",
                "ccgr",
                "cgr",
                "dega",
                "gr",
                "mila",
                "mina",
                "mrad",
                "mseca",
                "seca",
                "urad",
            ],
        )
        db.AddCategory(
            "angle per length",
            "angle per length",
            override=override_categories,
            valid_units=[
                "rad/m",
                "dega/100ft",
                "dega/30ft",
                "dega/30m",
                "dega/ft",
                "dega/ft(100)",
                "dega/m",
                "dega/m(30)",
                "rad/ft",
            ],
        )
        db.AddCategory(
            "angle per volume",
            "angle per volume",
            override=override_categories,
            valid_units=["rad/m3", "rad/ft3"],
        )
        db.AddCategory(
            "angular acceleration",
            "angular acceleration",
            override=override_categories,
            valid_units=["rad/s2", "rpm/s", "dega/s2", "dega/min2", "rev/s2", "rev/min2", "Hz/s"],
        )
        db.AddCategory(
            "admittance",
            "electric conductance",
            override=override_categories,
            valid_units=["S", "GS", "kS", "mho", "mS", "pS", "uS"],
        )
        db.AddCategory(
            "electric conductance",
            "electric conductance",
            override=override_categories,
            valid_units=["S", "GS", "kS", "mho", "mS", "pS", "uS"],
        )
        db.AddCategory(
            "susceptance",
            "electric conductance",
            override=override_categories,
            valid_units=["S", "GS", "kS", "mho", "mS", "pS", "uS"],
        )
        db.AddCategory(
            "time",
            "time",
            override=override_categories,
            valid_units=["s", "a", "d", "Ga", "h", "Ma", "min", "ms", "MY", "us", "wk"],
        )
        db.AddCategory(
            "conductivity",
            "conductivity",
            override=override_categories,
            valid_units=["S/m", "mho/m", "mmho/m", "mS/m", "uS/m", "cS/m", "kS/m"],
        )
        db.AddCategory(
            "interval transit time",
            "time per length",
            override=override_categories,
            valid_units=["s/m"],
        )
        db.AddCategory(
            "slowness",
            "time per length",
            override=override_categories,
            valid_units=[
                "s/m",
                "ms/cm",
                "ms/ft",
                "ms/in",
                "ms/m",
                "ns/ft",
                "ns/m",
                "s/cm",
                "s/ft",
                "us/ft",
                "us/m",
            ],
        )
        db.AddCategory(
            "time per length",
            "time per length",
            override=override_categories,
            valid_units=[
                "s/m",
                "h/kft",
                "h/km",
                "min/ft",
                "min/m",
                "ms/cm",
                "ms/ft",
                "ms/in",
                "ms/m",
                "ns/ft",
                "ns/m",
                "s/cm",
                "s/ft",
                "s/in",
                "us/ft",
                "us/m",
            ],
        )
        db.AddCategory(
            "time per volume",
            "time per volume",
            override=override_categories,
            valid_units=[
                "s/m3",
                "d/bbl",
                "d/ft3",
                "d/Mcf",
                "d/m3",
                "h/ft3",
                "h/m3",
                "s/ft3",
                "s/L",
                "s/qtUK",
                "s/qtUS",
                "d/Mscf",
            ],
        )
        db.AddCategory(
            "standard volume per area",
            "standard volume per area",
            override=override_categories,
            valid_units=["scm(15C)/m2", "MMstb/acre", "scf(60F)/ft2", "stb(60F)/acre"],
        )
        db.AddCategory(
            "standard volume per volume",
            "standard volume per volume",
            override=override_categories,
            valid_units=[
                "scm(15C)/m3",
                "MMstb/acre.ft",
                "scf(60F)/bbl",
                "scf(60F)/ft3",
                "stb(60F)/bbl",
                "sm3/m3",
                "scm3/cm3",
                "stb/bbl",
                "Mscf/bbl",
                "scf/bbl",
            ],
        )
        db.AddCategory(
            "standard volume per standard volume",
            "standard volume per standard volume",
            override=override_categories,
            valid_units=[
                "scm(15C)/scm(15C)",
                "scf(60F)/stb",
                "scf(60F)/scf",
                "stb(60F)/stb",
                "sm3/sm3",
                "scm3/scm3",
                "stb/stb",
                "Mscf/stb",
                "MMscf/stb",
                "scf/stb",
                "stb/scf",
                "stb/MMscf",
            ],
        )
        db.AddCategory(
            "standard volume per time",
            "standard volume per time",
            override=override_categories,
            valid_units=[
                "scm(15C)/s",
                "ksm3/d",
                "MMscf(60F)/d",
                "MMscm(15C)/d",
                "MMstb(60F)/d",
                "Mscf(60F)/d",
                "Mscm(15C)/d",
                "Mstb(60F)/d",
                "scf(60F)/d",
                "scm(15C)/d",
                "stb(60F)/d",
                "MMscf/d",
                "MMsm3/d",
                "MMstb/d",
                "Mscf/d",
                "Msm3/d",
                "Mstb/d",
                "scf/d",
                "sm3/d",
                "stb/d",
                "sm3/s",
            ],
        )
        db.AddCategory(
            "solid angle", "solid angle", override=override_categories, valid_units=["sr"]
        )
        db.AddCategory(
            "dose equivalent",
            "dose equivalent",
            override=override_categories,
            valid_units=["Sv", "mrem", "mSv", "rem"],
        )
        db.AddCategory(
            "dose equivalent rate",
            "dose equivalent rate",
            override=override_categories,
            valid_units=["Sv/s", "mrem/h", "mSv/h", "rem/h", "Sv/h"],
        )
        db.AddCategory(
            "magnetic flux density",
            "magnetic induction",
            override=override_categories,
            valid_units=["T", "gauss", "mgauss", "mT", "nT", "uT"],
        )
        db.AddCategory(
            "magnetic induction",
            "magnetic induction",
            override=override_categories,
            valid_units=["T", "gauss", "mgauss", "mT", "nT", "uT"],
        )
        db.AddCategory(
            "electric potential",
            "electric potential",
            override=override_categories,
            valid_units=["V", "kV", "MV", "mV", "uV"],
        )
        db.AddCategory(
            "potential difference per per power drop",
            "potential difference per per power drop",
            override=override_categories,
            valid_units=["V/B", "V/dB"],
        )
        db.AddCategory(
            "electric field strength",
            "electric field strength",
            override=override_categories,
            valid_units=["V/m", "mV/ft", "mV/m", "uV/ft", "uV/m", "KV/mm"],
        )
        db.AddCategory(
            "heat flow rate",
            "power",
            override=override_categories,
            valid_units=[
                "W",
                "Btu(million)/hr",
                "Btu/hr",
                "Btu/min",
                "Btu/s",
                "EJ/a",
                "erg/a",
                "ft.lbf/min",
                "ft.lbf/s",
                "GW",
                "kW",
                "MBtu/hr",
                "MW",
                "mW",
                "nW",
                "quad/yr",
                "TJ/a",
                "TW",
                "uW",
                "J/s",
                "kJ/d",
                "J/d",
                "Btu/d",
            ],
        )
        db.AddCategory(
            "power",
            "power",
            override=override_categories,
            valid_units=[
                "W",
                "ch",
                "CV",
                "ehp",
                "GW",
                "hhp",
                "hp",
                "kcal/h",
                "kW",
                "MJ/a",
                "MW",
                "mW",
                "nW",
                "ton of refrig",
                "TW",
                "uW",
            ],
        )
        db.AddCategory(
            "thermal conductance",
            "thermal conductance",
            override=override_categories,
            valid_units=["W/K"],
        )
        db.AddCategory(
            "energy length per time area temperature",
            "thermal conductivity",
            override=override_categories,
            valid_units=["W/m.K", "Btu.in/hr.ft2.F", "kJ.m/h.m2.K"],
        )
        db.AddCategory(
            "thermal conductivity",
            "thermal conductivity",
            override=override_categories,
            valid_units=[
                "W/m.K",
                "Btu/hr.ft.degF",
                "cal/h.cm.degC",
                "cal/s.cm.degC",
                "cal/m.h.degC",
                "kcal/h.m.degC",
                "Btu/d.ft.degF",
                "kJ/d.m.K",
                "W/m.degC",
            ],
        )
        db.AddCategory(
            "density of heat flow rate",
            "density of heat flow rate",
            override=override_categories,
            valid_units=[
                "W/m2",
                "Btu/hr.ft2",
                "Btu/s.ft2",
                "cal/h.cm2",
                "hhp/in2",
                "hp/in2",
                "kW/cm2",
                "kW/m2",
                "mW/m2",
                "ucal/s.cm2",
                "W/cm2",
                "W/mm2",
            ],
        )
        db.AddCategory(
            "energy fluence rate",
            "density of heat flow rate",
            override=override_categories,
            valid_units=[
                "W/m2",
                "Btu/hr.ft2",
                "Btu/s.ft2",
                "cal/h.cm2",
                "hhp/in2",
                "hp/in2",
                "kW/cm2",
                "kW/m2",
                "mW/m2",
                "ucal/s.cm2",
                "W/cm2",
                "W/mm2",
            ],
        )
        db.AddCategory(
            "fluence rate",
            "density of heat flow rate",
            override=override_categories,
            valid_units=[
                "W/m2",
                "Btu/hr.ft2",
                "Btu/s.ft2",
                "cal/h.cm2",
                "hhp/in2",
                "hp/in2",
                "kW/cm2",
                "kW/m2",
                "mW/m2",
                "ucal/s.cm2",
                "W/cm2",
                "W/mm2",
            ],
        )
        db.AddCategory(
            "irradiance",
            "density of heat flow rate",
            override=override_categories,
            valid_units=[
                "W/m2",
                "Btu/hr.ft2",
                "Btu/s.ft2",
                "cal/h.cm2",
                "hhp/in2",
                "hp/in2",
                "kW/cm2",
                "kW/m2",
                "mW/m2",
                "ucal/s.cm2",
                "W/cm2",
                "W/mm2",
            ],
        )
        db.AddCategory(
            "poynting vector",
            "density of heat flow rate",
            override=override_categories,
            valid_units=[
                "W/m2",
                "Btu/hr.ft2",
                "Btu/s.ft2",
                "cal/h.cm2",
                "hhp/in2",
                "hp/in2",
                "kW/cm2",
                "kW/m2",
                "mW/m2",
                "ucal/s.cm2",
                "W/cm2",
                "W/mm2",
            ],
        )
        db.AddCategory(
            "radiant energy",
            "density of heat flow rate",
            override=override_categories,
            valid_units=[
                "W/m2",
                "Btu/hr.ft2",
                "Btu/s.ft2",
                "cal/h.cm2",
                "hhp/in2",
                "hp/in2",
                "kW/cm2",
                "kW/m2",
                "mW/m2",
                "ucal/s.cm2",
                "W/cm2",
                "W/mm2",
            ],
        )
        db.AddCategory(
            "radiant exitance",
            "density of heat flow rate",
            override=override_categories,
            valid_units=[
                "W/m2",
                "Btu/hr.ft2",
                "Btu/s.ft2",
                "cal/h.cm2",
                "hhp/in2",
                "hp/in2",
                "kW/cm2",
                "kW/m2",
                "mW/m2",
                "ucal/s.cm2",
                "W/cm2",
                "W/mm2",
            ],
        )
        db.AddCategory(
            "sound intensity",
            "density of heat flow rate",
            override=override_categories,
            valid_units=[
                "W/m2",
                "Btu/hr.ft2",
                "Btu/s.ft2",
                "cal/h.cm2",
                "hhp/in2",
                "hp/in2",
                "kW/cm2",
                "kW/m2",
                "mW/m2",
                "ucal/s.cm2",
                "W/cm2",
                "W/mm2",
            ],
        )
        db.AddCategory(
            "heat transfer coefficient",
            "heat transfer coefficient",
            override=override_categories,
            valid_units=[
                "W/m2.K",
                "Btu/hr.ft2.degF",
                "Btu/hr.ft2.degR",
                "Btu/hr.m2.degC",
                "Btu/s.ft2.degF",
                "cal/h.cm2.degC",
                "cal/s.cm2.degC",
                "J/s.m2.degC",
                "kcal/h.m2.degC",
                "cal/h.m2.degC",
                "kJ/h.m2.K",
                "kW/m2.K",
            ],
        )
        db.AddCategory(
            "radiance", "radiance", override=override_categories, valid_units=["W/m2.sr"]
        )
        db.AddCategory(
            "power per volume",
            "power per volume",
            override=override_categories,
            valid_units=[
                "W/m3",
                "Btu/hr.ft3",
                "Btu/s.ft3",
                "cal/h.cm3",
                "cal/s.cm3",
                "hp/ft3",
                "kW/m3",
                "uW/m3",
            ],
        )
        db.AddCategory(
            "volumetric heat transfer coefficient",
            "volumetric heat transfer coefficient",
            override=override_categories,
            valid_units=["W/m3.K", "Btu/hr.ft3.degF", "Btu/s.ft3.degF", "kW/m3.K"],
        )
        db.AddCategory(
            "radiant intensity",
            "radiant intensity",
            override=override_categories,
            valid_units=["W/sr"],
        )
        db.AddCategory(
            "magnetic flux",
            "magnetic flux",
            override=override_categories,
            valid_units=["Wb", "mWb", "uWb"],
        )
        db.AddCategory(
            "magnetic dipole moment",
            "magnetic dipole moment",
            override=override_categories,
            valid_units=["Wb.m"],
        )
        db.AddCategory(
            "magnetic vector potential",
            "magnetic vector potential",
            override=override_categories,
            valid_units=["Wb/m", "Wb/mm"],
        )
        db.AddCategory(
            "standard volume",
            "standard volume",
            override=override_categories,
            valid_units=[
                "ft3(std,60F)",
                "MMscf(60F)",
                "MMscm(15C)",
                "MMstb(60F)",
                "Mscf(60F)",
                "Mstb(60F)",
                "scf(60F)",
                "stb(60F)",
                "stb",
                "scf",
                "sm3",
            ],
        )
        db.AddCategory(
            "injectivity factor",
            "injectivity factor",
            override=override_categories,
            valid_units=["m3/s.Pa", "bbl/min.psi", "(m3/d)/(kgf/cm2)"],
        )
        db.AddCategory(
            "datetime", "datetime", override=override_categories, valid_units=["datetime"]
        )
        db.AddCategory(
            "Unknown", "Unknown", override=override_categories, valid_units=["<unknown>"]
        )
        db.AddCategory(
            "bare number", "dimensionless", override=override_categories, valid_units=["-"]
        )
        db.AddCategory("category", "dimensionless", override=override_categories, valid_units=["-"])
        db.AddCategory("count", "dimensionless", override=override_categories, valid_units=["-"])
        db.AddCategory(
            "transmissibility",
            "transmissibility",
            override=override_categories,
            valid_units=[
                "cp.m3/day/bar",
                "cp.bbl/day/psi",
                "cp.ft3/day/psi",
                "cp.cm3/h/psi",
                "cp.m3/day/kPa",
                "cp.m3/day/kgf/cm2",
                "cp.cm3/h/Atm",
            ],
        )
        db.AddCategory(
            "solubility product",
            "solubility product",
            override=override_categories,
            valid_units=["(mol/m3)^2", "(mol/L)^2"],
        )
        db.AddCategory(
            "fraction", "fraction", override=override_categories, valid_units=["<fraction>"]
        )
        db.AddCategory(
            "porosity", "fraction", override=override_categories, valid_units=["<fraction>"]
        )
        db.AddCategory(
            "relative permeability",
            "fraction",
            override=override_categories,
            valid_units=["<fraction>"],
        )
        db.AddCategory(
            "per time squared",
            "per time squared",
            override=override_categories,
            valid_units=["1/d^2"],
        )
        db.AddCategory(
            "adsorption rate",
            "adsorption rate",
            override=override_categories,
            valid_units=["mg/kg/d", "kg/kg/d"],
        )
        db.AddCategory(
            "concentration ratio",
            "mass consumption efficiency",
            override=override_categories,
            valid_units=["mg/l/mg/l", "kg/m3/kg/m3"],
        )
        db.AddCategory(
            "mass consumption efficiency",
            "mass consumption efficiency",
            override=override_categories,
            valid_units=["mg/l/mg/l", "kg/m3/kg/m3"],
        )
        db.AddCategory(
            "density generation",
            "density generation",
            override=override_categories,
            valid_units=["kg/m3/d", "mg/l/d"],
        )
        db.AddCategory(
            "volumetric concentration",
            "volumetric concentration",
            override=override_categories,
            valid_units=["ppm/kg/m3"],
        )
        db.AddCategory(
            "efficiency of nutrient consumption for biomass building",
            "efficiency of nutrient consumption for biomass building",
            override=override_categories,
            valid_units=["kg/m3/d/kg/m3"],
        )
        db.AddCategory(
            "parts per million by volume per concentration",
            "parts per million by volume per concentration",
            override=override_categories,
            valid_units=["ppmv/mg/l", "ppmv/kg/m3"],
        )
        db.AddCategory(
            "fluid consistency",
            "fluid consistency",
            override=override_categories,
            valid_units=["Pa.s^n", "lbf.s^n/ft2", "lbf.s^n/100ft2", "eq.cp"],
        )
        db.AddCategory(
            "volume fraction per temperature",
            "volume fraction per temperature",
            override=override_categories,
            valid_units=["(m3/m3)/degC", "(m3/m3)/degF", "(m3/m3)/K"],
        )
        db.AddCategory(
            "per weight percent",
            "per weight percent",
            override=override_categories,
            valid_units=["1/wtpercent"],
        )
        db.AddCategory(
            "per square weight percent",
            "per square weight percent",
            override=override_categories,
            valid_units=["1/wtpercent*wtpercent"],
        )
        db.AddCategory(
            "per cubic weight percent",
            "per cubic weight percent",
            override=override_categories,
            valid_units=["1/wtpercent*wtpercent*wtpercent"],
        )
        db.AddCategory(
            "volume per equivalent",
            "volume per equivalent",
            override=override_categories,
            valid_units=["mL/meq"],
        )
        db.AddCategory(
            "volume per wtpercent",
            "volume per wtpercent",
            override=override_categories,
            valid_units=["ft3/wtpercent", "m3/wtpercent"],
        )
        db.AddCategory(
            "mass per mol",
            "mass per mol",
            override=override_categories,
            valid_units=["g/mol", "lb/lbmol", "kg/mol"],
        )
        db.AddCategory(
            "viscosity per pressure",
            "viscosity per pressure",
            override=override_categories,
            valid_units=["Pa.s/Pa", "cP/kPa", "cP/psi", "cP/(kgf/cm2)"],
        )
        db.AddCategory(
            "volt ampere",
            "volt ampere",
            override=override_categories,
            valid_units=["MVA", "kVA", "VA"],
        )
        db.AddCategory(
            "volt ampere reactive",
            "volt ampere reactive",
            override=override_categories,
            valid_units=["MVAr", "kVAr", "VAr"],
        )
        db.AddCategory(
            "stroke frequency",
            "stroke frequency",
            override=override_categories,
            valid_units=["spm", "sps"],
        )
        db.AddCategory(
            "power per mass",
            "power per mass",
            override=override_categories,
            valid_units=["W/kg", "kW/kg"],
        )
        db.AddCategory(
            "power per weight",
            "power per mass",
            override=override_categories,
            valid_units=["W/kg", "kW/kg"],
        )
        db.AddCategory(
            "concentration per square time",
            "concentration per square time",
            override=override_categories,
            valid_units=["kg/m3/d2", "mg/l/d2"],
        )
        db.AddCategory(
            "power per length",
            "power per length",
            override=override_categories,
            valid_units=["W/m"],
        )
        db.AddCategory(
            "density derivative in respect to pressure",
            "density derivative in respect to pressure",
            override=override_categories,
            valid_units=["kg/m3.Pa"],
        )
        db.AddCategory(
            "density derivative in respect to temperature",
            "density derivative in respect to temperature",
            override=override_categories,
            valid_units=["kg/m3.degC", "kg/m3.K"],
        )
        db.AddCategory(
            "computer binary memory",
            "computer binary memory",
            override=override_categories,
            valid_units=["Byte", "kByte", "MByte", "GByte", "TByte"],
        )
        db.AddCategory(
            "flow coefficient",
            "flow coefficient",
            override=override_categories,
            valid_units=["(m3/s)/(Pa^0.5)", "(m3/h)/(bar^0.5)", "(galUS/min)/(psi^0.5)"],
        )
        db.AddCategory(
            "temperature per area",
            "temperature per area",
            override=override_categories,
            valid_units=["degC/m2"],
        )
        db.AddCategory(
            "force per velocity",
            "force per velocity",
            override=override_categories,
            valid_units=["N.s/m", "lbf.s/ft", "lbf.s/in", "kgf.s/m"],
        )
        db.AddCategory(
            "force per angle",
            "force per angle",
            override=override_categories,
            valid_units=["N/rad"],
        )
        db.AddCategory(
            "force per angular velocity",
            "force per angular velocity",
            override=override_categories,
            valid_units=["Ns/rad"],
        )
        db.AddCategory(
            "moment per angle",
            "moment per angle",
            override=override_categories,
            valid_units=[
                "Nm/rad",
                "Nm/dega",
                "lbf.ft/dega",
                "lbf.ft/rad",
                "lbf.in/dega",
                "lbf.in/rad",
                "kgf.m/dega",
                "kgf.m/rad",
            ],
        )
        db.AddCategory(
            "moment per angular velocity",
            "moment per angular velocity",
            override=override_categories,
            valid_units=[
                "Nms/rad",
                "Nms/dega",
                "lbf.ft.s/dega",
                "lbf.ft.s/rad",
                "lbf.in.s/dega",
                "lbf.in.s/rad",
                "kgf.m.s/dega",
                "kgf.m.s/rad",
            ],
        )
        db.AddCategory(
            "mass temperature per mol",
            "mass temperature per mol",
            override=override_categories,
            valid_units=[
                "kg.K/mol",
                "g.K/mol",
                "kg.degC/mol",
                "g.degC/mol",
                "kg.K/kmol",
                "kg.degC/kmol",
                "g.degF/mol",
                "kg.degF/mol",
                "kg.degF/kmol",
            ],
        )
        db.AddCategory(
            "joule-thomson coefficient",
            "joule-thomson coefficient",
            override=override_categories,
            valid_units=[
                "K/Pa",
                "K/bar",
                "K/MPa",
                "degC/Pa",
                "degC/bar",
                "degC/MPa",
                "degF/Pa",
                "degF/bar",
                "degF/MPa",
                "degR/Pa",
                "degR/bar",
                "degR/MPa",
            ],
        )
        db.AddCategory(
            "force per velocity squared",
            "force per velocity squared",
            valid_units=["N.s2/m2", "lbf.s2/ft2", "lbf.s2/in2", "kgf.s2/m2"],
            override=True,
        )

    return db


def CreateVolumeQuantityFromLengthQuantity(length_quantity: "Quantity") -> "Quantity":
    """
    Creates a volume quantity based on the given length quantity.

    :param length_quantity:
        The length quantity that must be taken as base to create the volume quantity.

    :returns:
        THe created volume quantity.
    """

    from collections import OrderedDict

    from ._quantity import Quantity

    category = length_quantity.GetCategory()
    assert category == "length", (
        "The given quantity must have length as category. %s was given." % category
    )

    volume_unit = "%s3" % length_quantity.GetUnit()
    volume_units = UnitDatabase.GetSingleton().GetUnits("volume")

    if volume_unit not in volume_units:
        return Quantity.CreateDerived(OrderedDict([("length", (length_quantity.GetUnit(), 3))]))
    else:
        return ObtainQuantity(volume_unit, "volume")


def CreateAreaQuantityFromLengthQuantity(length_quantity: "Quantity") -> "Quantity":
    """
    Creates a area quantity based on the given length quantity.

    :param length_quantity:
        The length quantity that must be taken as base to create the volume quantity.

    :returns:
        THe created area quantity.
    """

    from collections import OrderedDict

    from ._quantity import Quantity

    category = length_quantity.GetCategory()
    assert category == "length", (
        "The given quantity must have length as category. %s was given." % category
    )

    area_unit = "%s2" % length_quantity.GetUnit()
    area_units = UnitDatabase.GetSingleton().GetUnits("area")

    if area_unit not in area_units:
        return Quantity.CreateDerived(OrderedDict([("length", (length_quantity.GetUnit(), 2))]))
    else:
        return ObtainQuantity(area_unit, "area")
