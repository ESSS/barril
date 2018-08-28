#===================================================================================================
# TranslateCategory
#===================================================================================================
from __future__ import absolute_import, print_function, unicode_literals

'''
Module that explicitly states some categories in the UnitDatabase, so gen_translation can pick them
for translation.
'''


def TranslateCategory(category):
    '''
    Translates the given category using the translation table. Always call this method when
    displaying an category to the user.

    :param unicode category:
        Category to translate

    :rtype: unicode
    '''
    return tr(category, CONTEXT)


# : context that should be passed to tr() for category to be translated (normally just use TranslateCategory())
CONTEXT = 'category_translation_table'


#===================================================================================================
# PrintTranslatedCategories
#===================================================================================================
def PrintTranslatedCategories():
    '''
    Dummy function that only calls the tr() function around the categories we want translated, so
    Qt can pick them up for translation.
    '''
    import coilib50  # isort:skip @UnusedImport: install tr() function

    print(tr("Angle per Time"))
    print(tr("Area"))
    print(tr("Date"))
    print(tr("Density"))
    print(tr("Depth"))
    print(tr("Diameter"))
    print(tr("Dimensionless"))
    print(tr("Dynamic Viscosity"))
    print(tr("Elasticity Modulus"))
    print(tr("Force"))
    print(tr("Flow Pattern"))
    print(tr("Fraction"))
    print(tr("Geothermal Gradient"))
    print(tr("Hydration Heat"))
    print(tr("Length"))
    print(tr("Linear Density"))
    print(tr("Mass"))
    print(tr("Plane Angle"))
    print(tr("Porosity"))
    print(tr("Power"))
    print(tr("Pressure"))
    print(tr('Pressure Gradient'))
    print(tr('Pressure Increasing Rate'))
    print(tr('Saturation'))
    print(tr("Specific Energy"))
    print(tr('Specific Heat Capacity'))
    print(tr('Standoff'))
    print(tr('Temperature Increasing Rate'))
    print(tr('Temperature'))
    print(tr('Time'))
    print(tr('Torque'))
    print(tr('Unknown'))
    print(tr('Velocity'))
    print(tr('Volume'))
    print(tr('Volume Flow Rate'))
    print(tr('Yield Stress'))
    print(tr('Volume per Time per Length'))
    print(tr('Injectivity Factor'))
    print(tr('Moment of Force'))
    print(tr('Drag'))
    print(tr('Bit Depth'))
    print(tr('Mass Concentration'))
    print(tr('Volumetric Concentration'))
    print(tr('Count'))
    print(tr('Radius'))
    print(tr('per Length'))
    print(tr('Permeability Rock'))
    print(tr('Permeability Length'))
    print(tr('Relative Permeability'))
    print(tr('Stroke Frequency'))


#===================================================================================================
# main
#===================================================================================================
if __name__ == '__main__':
    PrintTranslatedCategories()
