from barril.units import Scalar


def testEmptyScalar() -> None:
    scalar = Scalar.CreateEmptyScalar()
    assert not scalar.HasCategory()
    assert scalar == scalar.Copy()

    scalar = scalar.CreateCopy(category="pressure", unit="psi")
    assert scalar.HasCategory()
    assert scalar.GetValue() == 0.0

    assert scalar == scalar.Copy()
