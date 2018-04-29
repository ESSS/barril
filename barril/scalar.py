
class Scalar(object):
    '''
    This object represents a scalar (a value that has an associated quantity).

    Scalar Creation
    ===============

    Scalars can be created by giving a value, unit or category, in some combinations.

    Assuming the default value for category "length" is 10[m], all the example below create
    equal scalars:

        Scalar('length')
        Scalar(10.0, 'm', 'length')
        Scalar(10.0, 'm')
        Scalar((10.0, 'm')) # tuple of (value, unit)

    The last form is useful if you want to make a convenient interface for users of a class or method,
    accepting either a tuple or Scalar:

        def Compute(x, y):
            x, y = Scalar(x), Scalar(y)

    Which allows the user of the method to just pass a tuple, without having to create a Scalar explicitly:

        Compute(x=(10, 'm'), y=(15, 'm')) # is equivalent to Compute(x=Scalar(10, 'm'), y=Scalar(15, 'm'))

    Note that the following form is invalid, because if category and value is given, unit is mandatory.

        Scalar('length', 1.0)

    Variables
    =========

    :type _internal_unit: This is the unit in which the value has been set (but not necessarily the
    :ivar _internal_unit:
    unit which is visible to the outside world)

    .. note:: in case you're wondering, we cannot make a Scalar with __slots__ because our callback
    system (i.e.: callback.After) won't work with it.
    '''


    def __init__(self, category, value=None, unit=None):
        if isinstance(category, (float, int)):
            value, unit = category, value or unit
            category = '<unknown>'
        self.category = category
        self.unit = unit
        self.value = value

    def GetValue(self):
        return self.value
