from __future__ import unicode_literals

# constants for unknown quantities
UNKNOWN_QUANTITY_TYPE = 'Unknown'
UNKNOWN_UNIT = '<unknown>'

LENGTH_QUANTITY_TYPE = 'length'


#===================================================================================================
# CreateUnknwonwReadOnlyQuantity
#===================================================================================================
def CreateUnknwonwReadOnlyQuantity():
    '''
    :rtype: Quantity
    :returns:
        Returns a read only quantity for an unknown quantity.
    '''
    from ._quantity import ObtainQuantity
    return ObtainQuantity(UNKNOWN_UNIT, UNKNOWN_QUANTITY_TYPE)
