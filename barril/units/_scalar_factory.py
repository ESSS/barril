from __future__ import absolute_import, unicode_literals

from ._scalar import Scalar as _Scalar


#===================================================================================================
# ScalarFactory
#===================================================================================================
def ScalarFactory(category):

    class Scalar(_Scalar):

        def __init__(self, *args, **kwargs):
            pass

    return Scalar
