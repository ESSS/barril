from __future__ import absolute_import, unicode_literals

from ._definitions import IQuantity


#===================================================================================================
# IScalarInfo
#===================================================================================================
class IScalarInfo(IQuantity):
    '''
    Info that has meta-information about a scalar value.
    '''

    def GetSemanticAssociation(self):
        '''
        :rtype: SemanticAssociation
        :returns:
            The semantic association that represents this value.
        '''
