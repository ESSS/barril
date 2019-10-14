from barril.units import Scalar


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
    scalar_2 = Scalar.CreateEmptyScalar(20.0)

    assert scalar_1 == scalar_2

    # ETK relies on the behavior of getting a value from an empty scalar
    # passing a unit
    _ = scalar_1.GetValue("m")

    assert scalar_1.GetUnit() == ""
