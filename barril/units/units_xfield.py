from __future__ import absolute_import, unicode_literals

from ben10.foundation.decorators import Implements
from ben10.interface import ImplementsInterface
from coilib50.basic.xfield import IXFieldWithConvertion, XField

from ._fraction_scalar import FractionScalar
from ._scalar import Scalar


@ImplementsInterface(IXFieldWithConvertion)
class XAbstractValueWithQuantity(XField):
    '''
    XField for handling Scalar, FractionScalar and Array assign operations.
    The field is able to handle numbers, and tuples to properly assign a value to the attribute.

    e.g.
        model.scalar = Scalar('length', 0.0, 'm')
        # Change scalar value to 10 m
        model.scalar = 10
        # Change scalar value to 10 cm
        model.scalar = 10, cm
        # Change scalar value to 20 psi pressure
        model.scalar = 10, cm, pressure
    '''

    def __init__(self, category=None, value=None, unit=None):
        if isinstance(category, self.FIELD_CLASS):
            XField.__init__(self, self.FIELD_CLASS, category)

        else:
            XField.__init__(
                self,
                self.FIELD_CLASS,
                self.FIELD_CLASS(category, value=value, unit=unit),
            )

    def CreateInstance(self, value=XField.NoValue):
        if value is self.NoValue:
            return self.initial_value
        else:
            return self.ConvertValue(self.initial_value, value)

    @Implements(IXFieldWithConvertion.ConvertValue)
    def ConvertValue(self, old_value, new_value):
        '''

        :param old_value:
        :param new_value:
        '''
        if isinstance(new_value, self.FIELD_CLASS):
            return new_value

        elif isinstance(new_value, tuple):
            return old_value.CreateCopy(*new_value)

        elif new_value is None:
            return new_value

        else:
            return old_value.CreateCopy(value=new_value)


#===================================================================================================
# XScalar
#===================================================================================================
class XScalar(XAbstractValueWithQuantity):
    '''
    Scalar XField
    '''

    FIELD_CLASS = Scalar

    def __init__(self, category=None, value=None, unit=None):
        if category is None and unit is None:
            XAbstractValueWithQuantity.__init__(self, Scalar.CreateEmptyScalar(value=value))

        else:
            XAbstractValueWithQuantity.__init__(self, category=category, value=value, unit=unit)


XField.RegisterFactory(Scalar, XScalar)


#===================================================================================================
# XFractionScalar
#===================================================================================================
class XFractionScalar(XAbstractValueWithQuantity):
    '''
    FractionScalar XField
    '''

    FIELD_CLASS = FractionScalar


XField.RegisterFactory(FractionScalar, XFractionScalar)
