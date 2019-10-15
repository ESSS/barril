import pytest

from barril._util.types_ import CheckFormatString, CheckType, IsNumber, _GetKnownNumberTypes


def testPassing():
    class Foo:
        pass

    CheckType(Foo(), Foo)
    CheckType(Foo(), (int, Foo))
    CheckType(99, (int, Foo))


def testRaising():
    with pytest.raises(TypeError):
        CheckType("hellou", int)

    with pytest.raises(TypeError):
        CheckType("hellou", (int, float))

    with pytest.raises(TypeError):
        CheckType(99, (str, float))


def testCheckFormatString():
    CheckFormatString("%s", 1)
    CheckFormatString("%s m", 1)

    with pytest.raises(ValueError):
        CheckFormatString("%s m %s", 1)

    with pytest.raises(ValueError):
        CheckFormatString("%s m %s", 1, 3, 3)


def testIfCustomMessageIsAppendedToDefaultMessage():
    message = "Zero is not unicode!"

    with pytest.raises(TypeError) as exception:
        CheckType(0, str, message)

    assert message in str(exception.value)


def testCheckNumber():
    numpy = pytest.importorskip("numpy")

    for number_class in [float] + list((int,)):
        converted = number_class(1)
        assert IsNumber(converted)

    # Checking numpy numbers
    collection = numpy.zeros(1, numpy.float32)
    assert IsNumber(collection[0])


def testGetKnownNumberTypes(monkeypatch):
    import sys

    numpy = pytest.importorskip("numpy")

    expected = {float, complex, numpy.number}
    expected.update({int})
    assert set(_GetKnownNumberTypes()) == expected

    monkeypatch.setitem(sys.modules, "numpy", None)
    expected.remove(numpy.number)
    assert set(_GetKnownNumberTypes()) == expected
