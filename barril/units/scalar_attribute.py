from __future__ import absolute_import, unicode_literals

from ben10.foundation.decorators import Override
from ben10.foundation.klass import IsInstance
from ben10.interface import Attribute, CacheInterfaceAttrs


#===================================================================================================
# ScalarAttribute
#===================================================================================================
class ScalarAttribute(Attribute):
    '''
    '''

    def __init__(self, category):
        '''
        :param str quantity_type:
            String with the category of the Scalar.
        '''
        self.category = category

    @Override(Attribute.Match)
    def Match(self, attribute):
        if not IsInstance(attribute, 'Scalar'):
            return (False, 'The attribute is not a Scalar instance.')
        elif attribute.GetCategory() != self.category:
            return (
                False,
                'The Scalar category (%s) does not match the expected category of the'
                ' interface (%s).' % (attribute.GetCategory(), self.category)
            )

        return (True, None)


CacheInterfaceAttrs.RegisterAttributeClass(ScalarAttribute)
