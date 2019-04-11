
from ._scalar import Scalar as _Scalar


def ScalarFactory(category):
    class Scalar(_Scalar):
        def __init__(self, *args, **kwargs):
            pass

    return Scalar
