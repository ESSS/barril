from __future__ import absolute_import, unicode_literals

from ben10.interface import AssertImplements, BadImplementationError, ImplementsInterface, Interface
from coilib50.units.scalar_attribute import ScalarAttribute

import pytest

def testScalarAttribute():
    from coilib50.units import Scalar

    class IFluid(Interface):
        plastic_viscosity = ScalarAttribute('dynamic viscosity')
        yield_point = ScalarAttribute('pressure')
        density = ScalarAttribute('density')

    @ImplementsInterface(IFluid)
    class MyFluid(object):

        def __init__(self, plastic_viscosity, yield_point, density):
            self.plastic_viscosity = Scalar('dynamic viscosity', *plastic_viscosity)
            self.yield_point = Scalar('pressure', *yield_point)
            self.density = Scalar('density', *density)

    fluid = MyFluid(
        plastic_viscosity=(2.0, 'Pa.s'),
        yield_point=(4.0, 'lbf/100ft2'),
        density=(1.2, 'kg/m3'),
    )

    AssertImplements(fluid, IFluid)

    @ImplementsInterface(IFluid)
    class OtherFluid(object):

        def __init__(self, plastic_viscosity, yield_point, density):
            self.plastic_viscosity = Scalar('kinematic viscosity', *plastic_viscosity)  # Oops
            self.yield_point = Scalar('pressure', *yield_point)
            self.density = Scalar('density', *density)

    other_fluid = OtherFluid(
        plastic_viscosity=(1.0, 'm2/s'),  # Wrong!
        yield_point=(4.0, 'lbf/100ft2'),
        density=(1.2, 'kg/m3'),
    )

    # NOTE: Testing private methods here
    from ben10.interface._interface import _AssertImplementsFullChecking

    message = r'.* The Scalar category \(kinematic viscosity\) .* not match .* interface \(dynamic viscosity\).'
    with pytest.raises(BadImplementationError, match=message):
        _AssertImplementsFullChecking(other_fluid, IFluid)

    # NOTE: Different behaviour
    AssertImplements(other_fluid, IFluid)

def testScalarAttributeWithBaseSubjectProperty():
    from coilib50.basic.xfield import XFactory
    from coilib50.subject import BaseSubject
    from coilib50.units import Scalar

    class IFluid(Interface):
        plastic_viscosity = ScalarAttribute('dynamic viscosity')
        yield_point = ScalarAttribute('pressure')
        density = ScalarAttribute('density')

    @ImplementsInterface(IFluid)
    class MyFluid(BaseSubject):

        BaseSubject.Properties(
            plastic_viscosity=XFactory(Scalar, category='dynamic viscosity'),
            yield_point=XFactory(Scalar, category='pressure'),
            density=XFactory(Scalar, category='density'),
        )

        def __init__(self, plastic_viscosity, yield_point, density, **kwargs):
            BaseSubject.__init__(self, **kwargs)
            self.plastic_viscosity = Scalar(*plastic_viscosity)
            self.yield_point = Scalar(*yield_point)
            self.density = Scalar(*density)

    fluid = MyFluid(
        plastic_viscosity=(2.0, 'Pa.s'),
        yield_point=(4.0, 'lbf/100ft2'),
        density=(1.2, 'kg/m3'),
    )

    AssertImplements(fluid, IFluid)

