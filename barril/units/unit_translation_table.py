#===================================================================================================
# TranslateUnit
#===================================================================================================
from __future__ import absolute_import, print_function, unicode_literals

'''
Module that explicitly states all the units in the UnitDatabase, so gen_translation can pick them
to translate units.
'''


def TranslateUnit(unit):
    '''
    Translates the given unit using the translation table. Always call this method when displaying
    an unit to the user.

    :param unicode unit:
        Unit to translate

    :rtype: unicode
    '''
    return tr(unit, CONTEXT)


# : context that should be passed to tr() for units to be translated (normally just use TranslateUnit())
CONTEXT = 'unit_translation_table'


#===================================================================================================
# PrintTranslatedUnits
#===================================================================================================
def PrintTranslatedUnits():
    '''
    Dummy function that only calls the tr() function around the units we want translated, so
    Qt can pick them up for translation.
    '''
    import coilib50  # isort:skip @UnusedImport: install tr() function

    # volume -------------------------------------------------------------------------------------------
    print(tr("bbl"))
    print(tr("in3"))

    # volume flow rate ---------------------------------------------------------------------------------
    print(tr("bbl/min"))
    print(tr("galUS/min"))

    # angle per length ---------------------------------------------------------------------------------
    print(tr("dega/100ft"))
    print(tr("dega/30ft"))
    print(tr("dega/30m"))
    print(tr("dega/ft"))

    # plane angle --------------------------------------------------------------------------------------
    print(tr("dega"))

    # length -------------------------------------------------------------------------------------------
    print(tr("ft"))
    print(tr("in"))

    # area ---------------------------------------------------------------------------------------------
    print(tr("in2"))
    print(tr("m2"))

    # second moment of area ----------------------------------------------------------------------------
    print(tr("in4"))

    # temperature --------------------------------------------------------------------------------------
    print(tr("degC"))
    print(tr("degF"))
    print(tr("degR"))

    #===============================================================================================
    # From PWDa
    #===============================================================================================

    # Length ---------------------------------------------------------------------------------------
    print(tr('in/32'))

    # Density --------------------------------------------------------------------------------------
    print(tr('lbm/galUS'))

    # Velocity --------------------------------------------------------------------------------------
    print(tr('ft/s'))
    print(tr('ft/min'))
    print(tr('ft/h'))
    print(tr('ft/d'))

    # Volume
    print(tr('galUS'))
    print(tr('ft3'))

    # Flow Rate
    print(tr('galUS/s'))
    print(tr('galUS/hr'))
    print(tr('ft3/s'))
    print(tr('ft3/min'))
    print(tr('ft3/h'))

    # Force
    print(tr('tonf'))

    # Torque
    print(tr('kft.lbf'))
    print(tr('lbf.ft'))

    print(tr('us/ft'))
    print(tr('unitless'))
    print(tr('<fraction>'))
    print(tr('<unknown>'))

    print(tr('date'))

    # Geothermal Gradient
    print(tr('degC/m'))
    print(tr('degF/m'))
    print(tr('degC/km'))
    print(tr('degC/30m'))
    print(tr('degF/100ft'))
    print(tr('K/m'))

    print(tr('(galUS/min)/(psi^0.5)'))

    # Total Gas Unit
    print(tr('tgu'))


#===================================================================================================
# main
#===================================================================================================
if __name__ == '__main__':
    PrintTranslatedUnits()
