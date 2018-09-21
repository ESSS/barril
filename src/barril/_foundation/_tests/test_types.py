from __future__ import unicode_literals

import pytest
import six
from six.moves import range  # @UnresolvedImport

from barril._foundation.types_ import (
    AsList, Boolean, CheckBasicType, CheckEnum, CheckFormatString, CheckIsNumber, CheckType,
    Flatten, Intersection, IsBasicType, IsNumber, MergeDictsRecursively,
    OrderedIntersection, StructMap, _GetKnownNumberTypes)


def testBoolean():
    assert Boolean('TRUE') == True
    assert Boolean('true') == True
    assert Boolean('yes') == True
    assert Boolean('1') == True
    assert Boolean('false') == False
    assert Boolean('no') == False
    assert Boolean('0') == False

    with pytest.raises(ValueError):
        Boolean('INVALID')


def testPassing():

    class Foo(object):
        pass

    CheckType(Foo(), Foo)
    CheckType(Foo(), (int, Foo))
    CheckType(99, (int, Foo))


def testRaising():
    with pytest.raises(TypeError):
        CheckType('hellou', int)

    with pytest.raises(TypeError):
        CheckType('hellou', (int, float))

    with pytest.raises(TypeError):
        CheckType(99, (six.text_type, float))


def testCheckFormatString():
    CheckFormatString('%s', 1)
    CheckFormatString('%s m', 1)

    with pytest.raises(ValueError):
        CheckFormatString('%s m %s', 1)

    with pytest.raises(ValueError):
        CheckFormatString('%s m %s', 1, 3, 3)


def testIfCustomMessageIsAppendedToDefaultMessage():
    message = 'Zero is not unicode!'

    with pytest.raises(TypeError) as exception:
        CheckType(0, six.text_type, message)

    assert message in six.text_type(exception.value)


def testBasicType():

    class NonBasic(object):
        ''

    assert IsBasicType(1)
    assert not IsBasicType([1])
    assert IsBasicType([1], accept_compound=True)
    assert IsBasicType({1: [1]}, accept_compound=True)
    assert IsBasicType({1: set([1])}, accept_compound=True)
    assert IsBasicType(frozenset([1, 2]), accept_compound=True)
    assert IsBasicType([1, [2, [3]]], accept_compound=True)
    assert not IsBasicType({1: NonBasic()}, accept_compound=True)
    assert not IsBasicType({NonBasic(): 1}, accept_compound=True)

    assert IsBasicType(NonBasic(), accept_compound=True) == False
    assert IsBasicType([NonBasic()], accept_compound=True) == False
    assert IsBasicType([1, [NonBasic()]], accept_compound=True) == False

    assert CheckBasicType(0) == True
    with pytest.raises(TypeError):
        CheckBasicType([0])


def testCheckEnum():
    for i in range(10):
        CheckEnum(i, list(range(10)))

    with pytest.raises(ValueError):
        CheckEnum(-1, list(range(10)))
    with pytest.raises(ValueError):
        CheckEnum(11, list(range(10)))
    with pytest.raises(ValueError):
        CheckEnum('foo', list(range(10)))


def testCheckNumber():
    numpy = pytest.importorskip('numpy')

    for number_class in [float] + list(six.integer_types):
        converted = number_class(1)
        assert IsNumber(converted)

    # Checking numpy numbers
    collection = numpy.zeros(1, numpy.float32)
    assert IsNumber(collection[0])


def testGetKnownNumberTypes(monkeypatch):
    import sys
    numpy = pytest.importorskip('numpy')

    expected = {float, complex, numpy.number}
    expected.update(set(six.integer_types))
    assert set(_GetKnownNumberTypes()) == expected

    monkeypatch.setitem(sys.modules, 'numpy', None)
    expected.remove(numpy.number)
    assert set(_GetKnownNumberTypes()) == expected


def testCheckIsNumber():
    assert CheckIsNumber(1)
    assert CheckIsNumber(1.)
    if six.PY2:
        assert CheckIsNumber(long(1))  # noqa
    with pytest.raises(TypeError):
        CheckIsNumber('alpha')


class ListWithoutIter(object):

    def __init__(self, *args, **kwargs):
        self.contents = []
        for item in args:
            self.contents.append(item)

    def __getitem__(self, index):
        return self.contents[index]


def testAsList():
    a = [1, 2, 3]
    assert a is AsList(a)
    assert ['a'] == AsList('a')
    assert ['a'] == AsList(('a',))
    assert ['a'] == AsList(set('a'))


def testFlatten():
    a = [[[1], [2]], [3]]
    assert Flatten(a) == [1, 2, 3]

    a = [1, 2, [3, 4], (5, 6)]
    assert Flatten(a) == [1, 2, 3, 4, 5, 6]


def testFlattenOnClassWithoutIter():
    a = ListWithoutIter(ListWithoutIter(0, 1), 2, 3)
    assert Flatten(a) == [0, 1, 2, 3]


def testFlattenOnClassWithoutIterForStrings():
    a = ListWithoutIter(ListWithoutIter("a", "bb"), "ccc")
    assert Flatten(a) == ["a", "bb", "ccc"]


def testFlattenForStrings():
    a = [["a", "bb"], "ccc"]
    assert Flatten(a) == ["a", "bb", "ccc"]


def testFlattenForUnicodeStrings():
    a = [[u"a", u"bb"], u"ccc"]
    assert Flatten(a) == [u"a", u"bb", u"ccc"]


def testFlattenForTuples():
    a = [(0, "a"), (1, "b"), ((2, "c"), 42)]
    assert Flatten(a) == [0, "a", 1, "b", 2, "c", 42]


def testFlattenSkipSpecificClass():
    obj = ListWithoutIter('a', 'b')
    a = [obj, 'c', ['d', 'e']]
    assert Flatten(a, skip_types=[ListWithoutIter]) == [obj, 'c', 'd', 'e']


def testFlattenSkipTypeOfSubclass():

    class Foo(ListWithoutIter):

        def __init__(self, *args, **kwargs):
            super(Foo, self).__init__(*args, **kwargs)

    obj = Foo()
    a = [obj, 'c', 'd']
    assert Flatten(a, skip_types=[ListWithoutIter]) == [obj, 'c', 'd']


def testMergeDictsRecursively():
    dict_1 = { 'a' : 1, 'b' : 2 }
    dict_2 = { 'c' : 3, 'd' : 4 }
    assert MergeDictsRecursively(dict_1, dict_2) == { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4 }


def testMergeDictsRecursivelyDictsOnTheRightHaveHigherPrecedence():
    dict_1 = { 'a' : 1, 'b' : 2 }
    dict_2 = { 'b' : 3, 'd' : 4 }
    assert MergeDictsRecursively(dict_1, dict_2) == { 'a' : 1, 'b' : 3, 'd' : 4 }


def testMergeDictsRecursivelyManyLevelsOfRecursion():
    dict_1 = {
        'a' : 0,
        'b' : {
            'replaced_inner_b' : 0,
            'kept_inner_b' : 0,
        },
        'c' : {
            'inner_c' : {
                'replaced_inner_c' : 0,
                'kept_inner_c' : 0,
            },
        },
    }
    dict_2 = {
        'b' : {
            'replaced_inner_b' : 42,
            'added_inner_b' : 0,
        },
        'c' : {
            'inner_c' : {
                'replaced_inner_c' : 42,
                'added_inner_c' : 0,
            }
        }
    }
    assert (
        MergeDictsRecursively(dict_1, dict_2)
        == {
            'a' : 0,
            'b' : {
                'kept_inner_b' : 0,
                'replaced_inner_b' : 42,
                'added_inner_b' : 0,
            },
            'c' : {
                'inner_c' : {
                    'replaced_inner_c' : 42,
                    'added_inner_c' : 0,
                    'kept_inner_c' : 0,
                }
            },
        }
    )


def testMergeDictsRecursivelyWhenLeftHasDictKeyButRightDoesnt():
    dict_1 = {
        'a' : {
            'inner_a' : 0
        }
    }
    dict_2 = {
        'a' : 42
    }
    assert MergeDictsRecursively(dict_1, dict_2) == { 'a' : 42 }


def testMergeDictsRecursivelyWhenRightHasDictKeyButLeftDoesnt():
    dict_1 = {
        'a' : 42
    }
    dict_2 = {
        'a' : {
            'inner_a' : 0
        }
    }
    assert (
        MergeDictsRecursively(dict_1, dict_2)
        == {
            'a' : {
                'inner_a' : 0
            }
        }
    )


def testMergeDictsWithWrongTypes():
    with pytest.raises(AttributeError):
        MergeDictsRecursively('Foo', {})

    with pytest.raises(TypeError):
        MergeDictsRecursively({}, 'Foo')

    with pytest.raises(TypeError) as excinfo:
        MergeDictsRecursively({}, 'Foo')

    if six.PY2:
        expected = 'Wrong types passed. Expecting two dictionaries, got: "dict" and "unicode"'
    else:
        expected = 'Wrong types passed. Expecting two dictionaries, got: "dict" and "str"'
    assert six.text_type(excinfo.value) == expected


def testIntersection():
    alpha = [3, 2, 1]
    bravo = [2, 3, 4]
    assert Intersection(alpha, bravo) == {2, 3}

    assert Intersection() == set()


def testOrderedIntersection():
    alpha = [1, 2, 3]
    bravo = [2, 3, 4]
    assert OrderedIntersection(alpha, bravo) == [2, 3]

    alpha = [3, 1, 2]
    bravo = [2, 3, 4]
    assert OrderedIntersection(alpha, bravo) == [3, 2]

    alpha = [1, 2, 3]
    bravo = [4, 5, 6]
    assert OrderedIntersection(alpha, bravo) == []


def testStructMap():

    a = {'alpha' : [1, 2, 3], 'bravo' : (1, 2, 3)}

    obtained = StructMap(
        a,
        func=six.text_type,
        conditional=lambda x: isinstance(x, int)
    )
    expected = {'alpha' : ['1', '2', '3'], 'bravo' : ('1', '2', '3')}
    assert obtained == expected

