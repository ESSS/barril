'''
This module provides an interface for filling the unit-manager with the units defined
in a posc file.
'''
from __future__ import absolute_import, division, unicode_literals

import six
from six.moves import map  # @UnresolvedImport

from ben10.foundation.odict import odict as odict  # This can be updated to odict when the new version of Builds is released
from ben10.foundation.types_ import AsList

# namespace for posc
_NS = "{http://www.posc.org/schemas}"


#===================================================================================================
# GenerateDatabaseCodeCOG
#===================================================================================================
def GenerateDatabaseCodeCOG(cog, xml_contents, db_var='db'):
    '''
    Generates code that fills a local UnitDatabase instance with the posc units defined in the given
    xml. Used to generate python code that fills a UnitDatabase.

    :param cog cog:
        The cog object used to write code to.

    :type xml_contents: unicode or list(unicode)
    :param xml_contents:
        The xml containing the units in posc format or a list of xmls.

    :param unicode db_var:
        The name of the UnitDatabase local variable to generate code for.

    .. note:: the namespace must also contain the local variables "fill_categories" and
        "override_categories". See FillUnitDatabaseWithPosc for description of those parameters.
    '''
    from xml.etree import ElementTree
    import io

    xml_contents = AsList(xml_contents)
    all_units = []
    for content in xml_contents:
        f = io.StringIO(content)
        try:
            tree = ElementTree.parse(f)  # @UndefinedVariable
        finally:
            f.close()

        all_units.extend(tree.getroot().findall('*/%sUnitOfMeasure' % _NS))

    # This is a set of unusual units (arbitrarily decided). They are still in the unit database so that
    # a value in those units can be read. Also should an application need any of those units they
    # can still be added.
    ignore_units = set([
        # length
        'Mm',  # 'megameter'
        'angstrom',  # 'Angstrom'
        'chBnA',  # 'Benoit chain (1895 A)'
        'chBnB',  # 'Benoit chain (1895 B)'
        'chCla',  # 'Clarke chain'
        'chSe',  # 'Sears chain'
        'chUS',  # 'US Survey chain'
        'fathom',  # 'fathoms'
        'fm',  # 'femtometer'
        'ftBnA',  # 'British Foot (Benoit 1895 A)'
        'ftBnB',  # 'British Foot (Benoit 1895 B)'
        'ftBr(65)',  # 'British Foot 1865'
        'ftCla',  # 'Imperial Foot'
        'ftGC',  # 'Gold Coast Foot'
        'ftInd',  # 'Indian Foot'
        'ftInd(37)',  # 'Indian Foot, 1937'
        'ftInd(62)',  # 'Indian Foot, 1962'
        'ftInd(75)',  # 'Indian Foot, 1975'
        'ftMA',  # 'Modified American Foot'
        'ftSe',  # 'Sears Foot'
        'ftUS',  # 'US Survey Foot'
        'in/10',  # 'tenth of an inch'
        'in/16',  # '16th of an inch'
        'in/32',  # '32nd of an inch'
        'in/64',  # '64th of an inch'
        'inUS',  # 'US Survey inch'
        'lkBnA',  # 'British link 1895 A'
        'lkBnB',  # 'British link 1895 B'
        'lkCla',  # 'Clarke link'
        'lkSe',  # 'Sears link'
        'lkUS',  # 'US Survey link'
        'mGer',  # 'German legal metre'
        'miUS',  # 'U.S. Survey mile'
        'mil',  # 'mil, a thousandth of an inch'
        'nautmi',  # 'nautical mile'
        'ydBnA',  # 'Benoits yard (1895 A)'
        'ydBnB',  # 'Benoits yard (1895 B)'
        'ydCla',  # 'Clarkes yard'
        'ydIm',  # 'imperial yard'
        'ydInd',  # 'Indian yard'
        'ydInd(37)',  # 'Indian yard (1937)'
        'ydInd(62)',  # 'Indian yard (1962)'
        'ydInd(75)',  # 'Indian yard (1975)'
        'ydSe',  # 'Sears yard'

        # pressure
        'Mpsi',  # 'mega pounds per square inch'
        'Pa(g)',  # 'pascal gauge'
        'at',  # 'Technical atmosphere'
        'lbf/ft2(100)',  # 'pounds force/100 square foot'
        'mmHg(0C)',  # 'millimetres of Mercury at 0 deg C'
        'pPa',  # 'picopascal'
        'umHg(0C)',  # 'microns of Mercury at 0 deg C'

        # time
        '100ka',  # '100000 years'
        'cs',  # 'ten milli second'
        'ms/2',  # 'half a millisecond'
        'hs',  # 'hundred seconds'
        'yr(100k)',  # '100000 years'
        'ns',  # 'nanoseconds'
        'ps',  # 'picosecond'

        # mass
        'oz(av)',  # 'avoirdupois ounces'
        'oz(troy)',  # 'troy ounces'
        'sack94',  # 'sacks'
        'cwtUK',  # 'UK hundredweight'
        'cwtUS',  # 'US hundredweight'
        'Mg',  # 'megagram'
        'ag',  # 'attogram'

        # volume
        'acre.ft',  # 'acre foot'
        'cu yd',  # 'cubic yard'
        'cubem',  # 'cubic mile'
        'fl ozUK',  # 'UK fluid ounce'
        'fl ozUS',  # 'US fluid ounces'
        'flozUK',  # 'UK fluid ounce'
        'flozUS',  # 'US fluid ounces'
        'ha.m',  # 'hectare metres'
        'km3',  # 'cubic kilometres'
        'mi3',  # 'cubic mile'
        'ptUK',  # 'UK pint'
        'ptUS',  # 'US pints'
        'qtUK',  # 'UK quarts'
        'qtUS',  # 'US quarts'
        'um2.m',  # 'square micron metres'
        'yd3',  # 'cubic yard'

        # standard volume
        'Gsm3',  # 'giga standard cubic metres 15C'
        'Msm3',  # 'mega standard cubic metres 15C'
        'ksm3',  # 'kilo standard cubic metres 15C'
        'scm(15C)',  # 'standard cubic metres at 15 deg Celsius'

        # volume per volume
        'L/10bbl',  # 'liter per ten barrel'
        'M(ft3)/acre.ft',  # 'million cubic feet per acre-foot'
        'MMbbl/acre.ft',  # 'million barrels/acre foot'
        'bbl/acre.ft',  # 'barrel/acre foot'
        'galUK/Mbbl',  # 'UK gallons/1000 barrels'
        'galUK/ft3',  # 'UK gallons/cubic foot'
        'galUK/kgalUK',  # 'UK gallons per thousand UK gallons'
        'galUS/10bbl',  # 'US gallons per ten barrels'
        'galUS/Mbbl',  # 'US gallons/1000 barrels'
        'galUS/bbl',  # 'US gallons/barrels'
        'galUS/ft3',  # 'US gallons/cubic foot'
        'galUS/kgalUS',  # 'US gallons per thousand US gallons'
        'm3/ha.m',  # 'cubic metres/hectare metre'
        'mL/galUK',  # 'millilitres/UK gallon'
        'mL/galUS',  # 'millilitres/US gallon'
        'ptUK/Mbbl',  # 'UK pints/1000 barrels'
        'ptUS/10bbl',  # 'US pint per ten barrel'
        'scm15/stb60',  # 'std cubic metres / stock tank barrel'
        'sm3/ksm3',  # 'std cubic metres/ 1000 std cubic metre'
        'stb60/MMscf60',  # 'stock tank barrels/ million std cu ft'
        'stb60/MMscm15',  # 'stock tank barrels/ million std cu mts'
        'stb60/Mscf60',  # 'stock tank barrels/ 1000 std cu ft'
        'stb60/Mscm15',  # 'stock tank barrels/ 1000 std cu metres'
        'stb60/scm15',  # 'stock tank barrels/ std cu metres'

        # plane angle
        'Grad',  # 'gigaradian'
        'Mrad',  # 'megaradian'
        'c',  # 'cycle'
        'gon',  # 'gons'
        'krad',  # 'kiloradian'
    ])

    added_quantity_types = set()
    quantity_type_to_units = {}
    base_units_to_add = []
    derived_units_to_add = []

    # Collect all quantity types that are unique, have only one quantity type
    preferred_categories = {}

    posc_info = []
    base_unit_to_quantity_types = odict()
    for u in all_units:
        conv_to_base_unit = u.findall('%sConversionToBaseUnit' % _NS)
        name = u.findall('%sName' % _NS)
        assert len(name) == 1
        name = name[0].text
        symbol = u.find('%sCatalogSymbol' % _NS).text
        quantity_type_nodes = u.findall('%sQuantityType' % _NS)
        if quantity_type_nodes:

            quantity_types = [' '.join(c.text.split()) for c in quantity_type_nodes if c.text]
            if len(quantity_types) == 1:
                quantity_type = quantity_types[0]
                if quantity_type in preferred_categories:
                    preferred_categories[quantity_type].append(symbol)
                else:
                    preferred_categories[quantity_type] = [symbol]

            assert len(conv_to_base_unit) <= 1, 'Name: %s Found: %s (types: %s)' % (
                name, conv_to_base_unit, quantity_types)

            if not conv_to_base_unit:  # Base unit.
                base_unit = symbol
            else:
                base_unit = conv_to_base_unit[0].get('baseUnit')

            assert base_unit.strip()
            if conv_to_base_unit:
                conversion_node = conv_to_base_unit[0]
            else:
                conversion_node = None
            posc_info.append((base_unit, symbol, name, conversion_node))

            if symbol in ignore_units:
                continue
            types = base_unit_to_quantity_types.setdefault(base_unit, [])
            for quantity_type in quantity_types:
                quantity_type_to_units.setdefault(quantity_type, []).append(symbol)

                if quantity_type not in types:
                    types.append(quantity_type)

    # Now, validate: a given quantity type may only appear in one base unit.
    quantity_type_to_base_unit = {}
    for base, quant_types in six.iteritems(base_unit_to_quantity_types):
        # print
        # print 'Base:', base
        for q in quant_types:
            if q in quantity_type_to_base_unit:
                raise AssertionError('The quantity type: %s was already found in the unit: %s (and now: %s)' %
                    (q, base, quantity_type_to_base_unit[q]))
            # print '    ',q
            quantity_type_to_base_unit[q] = base

    priority_dict = {
        'Pa': 'pressure',
        '1/Pa': 'compressibility',
        'W/m.K': 'thermal conductivity',
        'mol': 'molar mass',
        '-': 'dimensionless',
        'A/m': 'magnetization',
        'Pa.s': 'mass per time per length',
        'm2/s': 'volume per time per length',
        'K': 'temperature',
        'm3/kg': 'specific volume',
    }

    def TranslateBaseUnitToQuantityType(base_unit):
        '''
        :param unicode base_unit:
            The base unit for which we want the quantity type.

        :rtype: unicode
        :returns:
            Returns the quantity type to be used for the given unit.
        '''
        if base_unit in priority_dict:
            return priority_dict[base_unit]
        else:
            return base_unit_to_quantity_types[base_unit][0]

    for base_unit, symbol, name, conversion_node in posc_info:
        quantity_type = TranslateBaseUnitToQuantityType(base_unit)

        if conversion_node is None:
            # Base Units DON'T HAVE <ConversionToBaseUnit>
            base_units_to_add.append((db_var, quantity_type, name, symbol))
            added_quantity_types.add(quantity_type)
        else:
            # Customary Units HAVE <ConversionToBaseUnit>
            a, b, c, base = _ExtractFormulaCoefficients(conversion_node)
            derived_units_to_add.append(((a, b, c, base), (db_var, quantity_type, name, symbol)))
            added_quantity_types.add(quantity_type)

    already_added = set()
    quantity_type_2_base_unit = {}
    for base_unit in base_units_to_add:
        if base_unit not in already_added:
            already_added.add(base_unit)
            db_var, text, name, symbol = base_unit
            quantity_type_2_base_unit[text] = symbol
            cog.outl("%s.AddUnitBase('%s', '%s', '%s')" % (db_var, text, name, symbol))

    unit_2_default_category = {}
    for quantity_type, units in six.iteritems(preferred_categories):
        if quantity_type not in quantity_type_2_base_unit:
            base_unit = quantity_type_to_base_unit[q]
            if quantity_type != TranslateBaseUnitToQuantityType(base_unit):
                for unit in units:
                    unit_2_default_category[unit] = quantity_type

    for (a, b, c, base), unit in derived_units_to_add:
        if unit not in already_added:
            already_added.add(unit)
            db_var, text, name, symbol = unit
            cog.outl("f_unit_to_base = MakeCustomaryToBase(%s, %s, %s, %s)" % (a, b, c, base))
            cog.outl("f_base_to_unit = MakeBaseToCustomary(%s, %s, %s, %s)" % (a, b, c, base))
            if symbol in unit_2_default_category:
                category = "'%s'" % unit_2_default_category[symbol]
            else:
                category = None
            cog.outl("%s.AddUnit('%s', '%s', '%s', f_base_to_unit, f_unit_to_base, default_category=%s)" % \
                (db_var, text, name, symbol, category))

    # if we should create one category for each quantity type
    cog.outl()
    cog.outl('if fill_categories:')
    for dimensional_class, quantity_types in six.iteritems(base_unit_to_quantity_types):
        for quantity_type in sorted(quantity_types):
            cog.outl("    %s.AddCategory('%s', '%s', override=override_categories, valid_units=%s)" % (
                db_var, quantity_type, TranslateBaseUnitToQuantityType(dimensional_class), quantity_type_to_units[quantity_type]))

    cog.outl()


#===================================================================================================
# _ExtractFormulaCoefficients
#===================================================================================================
def _ExtractFormulaCoefficients(conversion_node):
    '''
    Extracts the coefficients of the conversion formule from the given conversion node, as strings
    as defined in the given node element of the posc xml file. This coefficients are used
    by MakeCustomaryToBase and MakeBaseToCustomary to convert a unit from and to the unit base of
    a category.

    :param Element conversion_node:
        The xml element that defines the conversion for a unit

    :rtype: (unicode, unicode, unicode, unicode)
    :returns:
        The (a, b, c, d) coefficients
    '''
    if conversion_node.find('%sFormula' % _NS) is not None:
        a = conversion_node.find('*/%sA' % _NS).text
        b = conversion_node.find('*/%sB' % _NS).text
        c = conversion_node.find('*/%sC' % _NS).text
        d = conversion_node.find('*/%sD' % _NS).text

    elif conversion_node.find('%sFactor' % _NS) is not None:
        # A = 0; B = factor; C = 1; D = 0
        a = '0.0'
        b = conversion_node.find('%sFactor' % _NS).text
        c = '1.0'
        d = '0.0'

    elif conversion_node.find('%sFraction' % _NS) is not None:
        # A = 0; B = numerator; C = denominator; D = 0
        a = '0.0'
        b = conversion_node.find('*/%sNumerator' % _NS).text
        c = conversion_node.find('*/%sDenominator' % _NS).text
        d = '0.0'
    else:
        raise TypeError('Invalid ConversionToBaseUnit Node')

    return a, b, c, d


#===================================================================================================
# _MakeFormulas
#===================================================================================================
def _MakeFormulas(conversion_node):
    '''
   Extracts values of coefficients A, B, C and D according to the
   type of conversion: Formula, Factor or Fraction

   :type conversion_node: ElementTree node
   :param conversion_node:
       <ConversionToBaseUnit> ElementTree Element node object

   :rtype: tuple(callable, callable)
   :returns:
       (to_base, from_base) which are functions to convert from the base unit and to base unit.
    '''
    coefficients = list(map(float, _ExtractFormulaCoefficients(conversion_node)))

    f_unit_to_base = MakeCustomaryToBase(*coefficients)
    f_base_to_unit = MakeBaseToCustomary(*coefficients)

    return (f_base_to_unit, f_unit_to_base)


#===================================================================================================
# MakeCustomaryToBase
#===================================================================================================
def MakeCustomaryToBase(a, b, c, d):
    '''
    Formula to convert some value from Customary Unit to Base Unit
    (A + BX) / (C + DX)
    X can be any single numeric value or a numpy array
    Integer values are correctly handled, once a, b, c and d parameters
    are always floats

    :rtype: callable
    :returns:
        Returns a callable with the conversion to the base.
    '''
    ret = lambda x:(a + b * x) / (c + d * x)
    ret.__a__ = a
    ret.__b__ = b
    ret.__c__ = c
    ret.__d__ = d
    ret.__has_conversion__ = True

    return ret


#===================================================================================================
# MakeBaseToCustomary
#===================================================================================================
def MakeBaseToCustomary(a, b, c, d):
    '''
    Formula to convert some value from Derivate Unit to Base Unit
   (A - CY) / (DY - B)
   Y can be any single numeric value or a numpy array
   Integer values are correctly handled, once a, b, c and d parameters
   are always floats

    :rtype: callable
    :returns:
        Returns a callable with the conversion from the base to a unit (depending on the
        coefficients).
    '''
    ret = lambda y:(a - c * y) / (d * y - b)
    ret.__a__ = a
    ret.__b__ = b
    ret.__c__ = c
    ret.__d__ = d
    ret.__has_conversion__ = True

    return ret

# The final definition was
#
# Base: V/B
#     potential difference per per power drop
#
# Base: 1/Pa
#     bulk compressibility
#     compressibility
#     viscosibility
#
# Base: V
#     electric potential
#
# Base: cp.m3/day/bar
#     transmissibility
#
# Base: W/m3
#     power per volume
#
# Base: W/m2
#     density of heat flow rate
#     poynting vector
#     radiant energy
#     fluence rate
#     radiant exitance
#     irradiance
#     sound intensity
#     energy fluence rate
#
# Base: mg/l/mg/l
#     mass consumption efficiency
#
# Base: N.m2
#     force area
#
# Base: J/mol
#     molar thermodynamic energy
#     chemical potential
#     affinity of a chemical reaction
#
# Base: s/m3
#     time per volume
#
# Base: Pa
#     force per area
#     pressure
#
# Base: Wb
#     magnetic flux
#
# Base: gAPI
#     gamma ray API unit
#
# Base: lm
#     luminous flux
#
# Base: Pa.s^n
#     fluid consistency
#
# Base: Bq
#     activity (of radioactivity)
#
# Base: J/mol.K
#     molar heat capacity
#     molar entropy
#     molar gas constant
#
# Base: kg.m
#     mass length
#
# Base: lx
#     illuminance
#     luminous exitance
#
# Base: 1/wtpercent*wtpercent
#     per square weight percent
#
# Base: mol/m2.s
#     mole per time per area
#
# Base: kg/m3/d
#     density generation
#
# Base: m3/s2
#     volume per time per time
#
# Base: W/m.K
#     energy length per time area temperature
#     thermal conductivity
#
# Base: mol/s
#     mole per time
#
# Base: rad/m3
#     angle per volume
#
# Base: mol
#     amount of substance
#     molar mass
#
# Base: W/m2.K
#     heat transfer coefficient
#
# Base: kg/m2.s
#     mass per time per area
#
# Base: W/m3.K
#     volumetric heat transfer coefficient
#
# Base: eq/m3
#     equivalent per volume
#
# Base: -
#     category
#     count
#     no unit
#
# Base: m3/scm(15C)
#     volume per standard volume
#
# Base: C/kg
#     exposure (radioactivity)
#
# Base: A/m
#     linear electric current density
#     magnetic field strength
#     magnetization
#
# Base: Gy
#     absorbed dose
#
# Base: bps
#     data transmission speed
#
# Base: mg/kg/d
#     adsorption rate
#
# Base: scm(15C)
#     standard volume
#
# Base: 1/wtpercent*wtpercent*wtpercent
#     per cubic weight percent
#
# Base: lm.s
#     quantity of light
#
# Base: 1/wtpercent
#     per weight percent
#
# Base: N/m3
#     force per volume
#
# Base: m2/kg
#     mass attenuation coefficient
#
# Base: m4/s
#     volume length per time
#
# Base: Sv
#     dose equivalent
#
# Base: m3/J
#     isothermal compressibility
#
# Base: ppmv/mg/l
#     parts per million by volume per concentration
#
# Base: eq
#     electrochemical equivalent
#
# Base: pH
#     pH
#
# Base: Pa.s
#     dynamic viscosity
#     mass per time per length
#
# Base: scm(15C)/m3
#     standard volume per volume
#
# Base: m2/s
#     kinematic viscosity
#     thermal diffusivity
#     diffusion coefficient
#     area per time
#     volume per time per length
#
# Base: S/m
#     conductivity
#
# Base: m3/s
#     volume flow rate
#
# Base: Pa.s/m6
#     nonDarcy flow coefficient
#
# Base: Bq/kg
#     specific activity (of radioactivity)
#
# Base: eq/kg
#     equivalent per mass
#
# Base: C
#     electric capacity
#     electric charge
#     electric flux
#
# Base: K/m
#     temperature per length
#
# Base: A.m2
#     electromagnetic moment
#
# Base: K
#     thermodynamic temperature
#     delta temperature
#     temperature
#
# Base: H/m
#     magnetic permeability
#
# Base: s/m
#     time per length
#     slowness
#     interval transit time
#
# Base: O
#     frequency interval
#
# Base: rad/s2
#     angular acceleration
#
# Base: S
#     electric conductance
#     admittance
#     susceptance
#
# Base: m2/Pa.s
#     unit productivity index
#     mobility
#
# Base: W
#     power
#     heat flow rate
#
# Base: kg/J
#     mass per energy
#
# Base: K/s
#     temperature per time
#
# Base: kg.m2
#     moment of inertia
#
# Base: kg/m3/d/kg/m3
#     efficiency of nutrient consumption for biomass building
#
# Base: kg/s
#     mass flow rate
#
# Base: Pa/s
#     pressure per time
#     pressure squared per (dynamic viscosity)
#
# Base: W/sr
#     radiant intensity
#
# Base: lm/W
#     luminous efficacy
#
# Base: s
#     time
#
# Base: m3/kg
#     specific volume
#     massic volume
#
# Base: V/m
#     electric field strength
#
# Base: Pa/m
#     pressure per length
#
# Base: K/W
#     thermal resistance
#
# Base: 1/s
#     per time
#     operations per time
#     volume per time per volume
#
# Base: m3/wtpercent
#     volume per wtpercent
#
# Base: m/s
#     velocity
#     volume per time per area
#
# Base: ppm/kg/m3
#     volumetric concentration
#
# Base: Euc
#     dimensionless
#     volumic concentration
#     mass concentration
#     linear strain
#     shear strain
#     poisson ratio
#     area per area
#     force per force
#     relative elongation
#     relative power
#     length per length
#     volume per volume
#     scale
#     linear concentration
#     relative time
#     mole per mole
#     index
#     multiplier
#     status
#     relative proportion
#
# Base: cd
#     luminous intensity
#
# Base: ohm.m
#     electrical resistivity
#
# Base: <unknown>
#     Unknown
#
# Base: B/m
#     attenuation per length
#
# Base: Pa.s/m3
#     pressure time per volume
#     acoustic impedance
#
# Base: 1/m
#     per length
#     wave number
#     area per volume
#
# Base: kg.m/s
#     momentum
#     impulse
#
# Base: 1/V
#     per electric potential
#
# Base: m2/mol
#     cross section absorption
#
# Base: kg/mol
#     mass per mol
#
# Base: m/K
#     length per temperature
#
# Base: m4
#     second moment of area
#     moment of section
#
# Base: Pa/m3
#     Darcy flow coefficient
#
# Base: m3
#     volume
#     permeability length
#
# Base: m2
#     area
#     permeability rock
#     volume per length
#
# Base: lx.s
#     light exposure
#
# Base: K.m2/W
#     thermal insulance
#     coefficient of thermal insulation
#
# Base: 1/K
#     volumetric thermal expansion
#     linear thermal expansion
#
# Base: 1/H
#     reluctance
#
# Base: B
#     level of power intensity
#
# Base: F
#     capacitance
#
# Base: B/O
#     attenuation
#
# Base: A/m2
#     current density
#
# Base: N
#     force
#     energy per length
#     energy length per area
#     force length per length
#
# Base: 1/N
#     per force
#
# Base: kg/m3
#     density
#     mass density
#     volumic mass
#     concentration
#
# Base: kg/m2
#     surface density
#     areic mass
#
# Base: C.m
#     electric dipole moment
#
# Base: kg/m4
#     mass per volume per length
#
# Base: N/m
#     force per length
#     energy per area
#
# Base: cd/m2
#     luminance
#
# Base: Sv/s
#     dose equivalent rate
#
# Base: m3/mol
#     molar volume
#
# Base: Wb.m
#     magnetic dipole moment
#
# Base: 1/kg
#     per mass
#
# Base: ohm
#     resistance
#     impedance
#
# Base: rad
#     plane angle
#
# Base: m3/s.Pa
#     injectivity factor
#
# Base: J/kg
#     specific energy
#
# Base: (m3/m3)/K
#     volume fraction per temperature
#
# Base: W/m2.sr
#     radiance
#
# Base: nAPI
#     neutron API unit
#
# Base: %
#     fraction
#     porosity
#     relative permeability
#
# Base: mL/meq
#     volume per equivalent
#
# Base: C/m3
#     charge density
#
# Base: C/m2
#     electric polarization
#
# Base: m3/Pa2.s2
#     specific productivity index
#
# Base: rad/s
#     frequency
#     angular velocity
#     rotational frequency
#     circular frequency
#     angle per time
#     rotational velocity
#
# Base: H
#     self inductance
#     permeance
#
# Base: m3/Pa.s
#     productivity index
#
# Base: 1/m3
#     per volume
#
# Base: 1/m2
#     per area
#     length per volume
#
# Base: A
#     electric current
#     magnetic potential difference
#     magnetomotive force
#
# Base: scm(15C)/m2
#     standard volume  per area
#     standard volume per area
#
# Base: Pa2
#     pressure squared
#
# Base: J
#     moment of force
#     moment of couple
#     torque
#     energy
#     work
#
# Base: J/kg.K
#     specific heat capacity
#     massic heat capacity
#
# Base: mol/m2
#     mole per area
#
# Base: mol/m3
#     concentration of B
#     amount of a substance
#
# Base: J/m3
#     normal stress
#     shear stress
#     modulus of elasticity
#     shear modulus
#     modulus of rigidity
#     bulk modulus
#     modulus of compression
#     electromagnetic energy density
#     radiant energy density
#
# Base: ohm/m
#     resistivity per length
#
# Base: m/s2
#     acceleration linear
#
# Base: F/m
#     permittivity
#
# Base: J/K
#     heat capacity
#
# Base: kg
#     mass
#
# Base: scm(15C)/s
#     standard volume per time
#
# Base: byte
#     digital storage
#
# Base: sr
#     solid angle
#
# Base: Wb/m
#     magnetic vector potential
#
# Base: m
#     length
#     breadth
#     height
#     depth
#     thickness
#     radius
#     radius of curvature
#     Cartesian coordinates
#     diameter
#     length of path
#     distance
#     wavelength
#     mean free path
#     volume per area
#
# Base: N4/kg.m7
#     parachor
#
# Base: kg/m
#     linear density
#     linear mass
#     mass per length
#
# Base: W/K
#     thermal conductance
#
# Base: rad/m
#     angle per length
#
# Base: 1/d^2
#     per time squared
#
# Base: T
#     magnetic induction
#     magnetic flux density
