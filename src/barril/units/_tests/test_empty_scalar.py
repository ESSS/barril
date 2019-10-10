from barril.units import Scalar
from barril.units.unit_database import InvalidQuantityTypeError
import pytest


def testEmptyScalar():
    scalar = Scalar.CreateEmptyScalar()
    assert not scalar.HasCategory()
    assert scalar == scalar.Copy()

    scalar = scalar.CreateCopy(category="pressure", unit="psi")
    assert scalar.HasCategory()
    assert scalar.GetValue() == 0.0

    assert scalar == scalar.Copy()


def testEmptyScalarWithInitialValue():
    # An empty scalar doesn't have a category defined
    scalar_1 = Scalar.CreateEmptyScalar(20.0)

    # When try to retrieve an empty scalar value using any unit a exception
    # is being raised
    with pytest.raises(InvalidQuantityTypeError):
        _ = scalar_1.GetValue("m")

    assert scalar_1.GetUnit() == ""
