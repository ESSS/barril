from __future__ import unicode_literals

import copy

import pytest
import six
from six.moves import range  # @UnresolvedImport

from ben10.filesystem import CreateFile, GetFileContents
from ben10.foundation.is_frozen import IsDevelopment, SetIsDevelopment
from ben10.foundation.odict import odict
from ben10.foundation.types_ import (
    AsList, Boolean, CheckBasicType, CheckEnum, CheckFormatString, CheckIsNumber, CheckType,
    CreateDevelopmentCheckType, Flatten, FlattenDictValues, Intersection, IsBasicType, IsNumber,
    MergeDictsRecursively, Null, OrderedIntersection, RemoveDuplicates, RemoveDuplicatesById,
    StringDictIO, StructMap, _GetKnownNumberTypes)


#===================================================================================================
# Test
#===================================================================================================
class Test(object):

    def testBoolean(self):
        assert Boolean('TRUE') == True
        assert Boolean('true') == True
        assert Boolean('yes') == True
        assert Boolean('1') == True
        assert Boolean('false') == False
        assert Boolean('no') == False
        assert Boolean('0') == False

        with pytest.raises(ValueError):
            Boolean('INVALID')

    def testDevelopmentCheckType(self):
        was_dev = IsDevelopment()
        try:
            assert CreateDevelopmentCheckType() is CheckType

            SetIsDevelopment(False)
            func = CreateDevelopmentCheckType()
            assert isinstance(func, type(lambda: None)) and func.__name__ == '<lambda>'

            SetIsDevelopment(True)
            func = CreateDevelopmentCheckType()
            assert not (isinstance(func, type(lambda: None)) and func.__name__ == '<lambda>')

        finally:
            SetIsDevelopment(was_dev)

    def testPassing(self):

        class Foo(object):
            pass

        CheckType(Foo(), Foo)
        CheckType(Foo(), (int, Foo))
        CheckType(99, (int, Foo))

    def testRaising(self):
        with pytest.raises(TypeError):
            CheckType('hellou', int)

        with pytest.raises(TypeError):
            CheckType('hellou', (int, float))

        with pytest.raises(TypeError):
            CheckType(99, (six.text_type, float))

    def testCheckFormatString(self):
        CheckFormatString('%s', 1)
        CheckFormatString('%s m', 1)

        with pytest.raises(ValueError):
            CheckFormatString('%s m %s', 1)

        with pytest.raises(ValueError):
            CheckFormatString('%s m %s', 1, 3, 3)

    def testIfCustomMessageIsAppendedToDefaultMessage(self):
        message = 'Zero is not unicode!'

        with pytest.raises(TypeError) as exception:
            CheckType(0, six.text_type, message)

        assert message in six.text_type(exception.value)

    def testBasicType(self):

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

    def testCheckEnum(self):
        for i in range(10):
            CheckEnum(i, list(range(10)))

        with pytest.raises(ValueError):
            CheckEnum(-1, list(range(10)))
        with pytest.raises(ValueError):
            CheckEnum(11, list(range(10)))
        with pytest.raises(ValueError):
            CheckEnum('foo', list(range(10)))

    def testCheckNumber(self):
        numpy = pytest.importorskip('numpy')

        for number_class in [float] + list(six.integer_types):
            converted = number_class(1)
            assert IsNumber(converted)

        # Checking numpy numbers
        collection = numpy.zeros(1, numpy.float32)
        assert IsNumber(collection[0])

    def testGetKnownNumberTypes(self, monkeypatch):
        import sys
        numpy = pytest.importorskip('numpy')

        expected = {float, complex, numpy.number}
        expected.update(set(six.integer_types))
        assert set(_GetKnownNumberTypes()) == expected

        monkeypatch.setitem(sys.modules, 'numpy', None)
        expected.remove(numpy.number)
        assert set(_GetKnownNumberTypes()) == expected

    def testCheckIsNumber(self):
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

    def testAsList(self):
        a = [1, 2, 3]
        assert a is AsList(a)
        assert ['a'] == AsList('a')
        assert ['a'] == AsList(('a',))
        assert ['a'] == AsList(set('a'))

    def testFlatten(self):
        a = [[[1], [2]], [3]]
        assert Flatten(a) == [1, 2, 3]

        a = [1, 2, [3, 4], (5, 6)]
        assert Flatten(a) == [1, 2, 3, 4, 5, 6]

    def testFlattenOnClassWithoutIter(self):
        a = self.ListWithoutIter(self.ListWithoutIter(0, 1), 2, 3)
        assert Flatten(a) == [0, 1, 2, 3]

    def testFlattenOnClassWithoutIterForStrings(self):
        a = self.ListWithoutIter(self.ListWithoutIter("a", "bb"), "ccc")
        assert Flatten(a) == ["a", "bb", "ccc"]

    def testFlattenForStrings(self):
        a = [["a", "bb"], "ccc"]
        assert Flatten(a) == ["a", "bb", "ccc"]

    def testFlattenForUnicodeStrings(self):
        a = [[u"a", u"bb"], u"ccc"]
        assert Flatten(a) == [u"a", u"bb", u"ccc"]

    def testFlattenForTuples(self):
        a = [(0, "a"), (1, "b"), ((2, "c"), 42)]
        assert Flatten(a) == [0, "a", 1, "b", 2, "c", 42]

    def testFlattenSkipSpecificClass(self):
        obj = self.ListWithoutIter('a', 'b')
        a = [obj, 'c', ['d', 'e']]
        assert Flatten(a, skip_types=[self.ListWithoutIter]) == [obj, 'c', 'd', 'e']

    def testFlattenSkipTypeOfSubclass(self):

        class Foo(self.ListWithoutIter):

            def __init__(self, *args, **kwargs):
                super(Foo, self).__init__(*args, **kwargs)

        obj = Foo()
        a = [obj, 'c', 'd']
        assert Flatten(a, skip_types=[self.ListWithoutIter]) == [obj, 'c', 'd']

    def testMergeDictsRecursively(self):
        dict_1 = { 'a' : 1, 'b' : 2 }
        dict_2 = { 'c' : 3, 'd' : 4 }
        assert MergeDictsRecursively(dict_1, dict_2) == { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4 }

    def testMergeDictsRecursivelyDictsOnTheRightHaveHigherPrecedence(self):
        dict_1 = { 'a' : 1, 'b' : 2 }
        dict_2 = { 'b' : 3, 'd' : 4 }
        assert MergeDictsRecursively(dict_1, dict_2) == { 'a' : 1, 'b' : 3, 'd' : 4 }

    def testMergeDictsRecursivelyManyLevelsOfRecursion(self):
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

    def testMergeDictsRecursivelyWhenLeftHasDictKeyButRightDoesnt(self):
        dict_1 = {
            'a' : {
                'inner_a' : 0
            }
        }
        dict_2 = {
            'a' : 42
        }
        assert MergeDictsRecursively(dict_1, dict_2) == { 'a' : 42 }

    def testMergeDictsRecursivelyWhenRightHasDictKeyButLeftDoesnt(self):
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

    def testMergeDictsWithWrongTypes(self):
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

    def testIntersection(self):
        alpha = [3, 2, 1]
        bravo = [2, 3, 4]
        assert Intersection(alpha, bravo) == {2, 3}

        assert Intersection() == set()

    def testOrderedIntersection(self):
        alpha = [1, 2, 3]
        bravo = [2, 3, 4]
        assert OrderedIntersection(alpha, bravo) == [2, 3]

        alpha = [3, 1, 2]
        bravo = [2, 3, 4]
        assert OrderedIntersection(alpha, bravo) == [3, 2]

        alpha = [1, 2, 3]
        bravo = [4, 5, 6]
        assert OrderedIntersection(alpha, bravo) == []

    def testNull(self):
        # constructing and calling

        dummy = Null()
        dummy = Null('value')
        n = Null('value', param='value')

        n()
        n('value')
        n('value', param='value')

        # attribute handling
        n.attr1
        n.attr1.attr2
        n.method1()
        n.method1().method2()
        n.method('value')
        n.method(param='value')
        n.method('value', param='value')
        n.attr1.method1()
        n.method1().attr1

        n.attr1 = 'value'
        n.attr1.attr2 = 'value'

        del n.attr1
        del n.attr1.attr2.attr3

        # Iteration
        for i in n:
            'Not executed'

        # representation and conversion to a string
        assert repr(n) == '<Null>'
        assert six.text_type(n) == 'Null'

        # truth value
        assert bool(n) == False
        assert bool(n.foo()) == False

        dummy = Null()
        # context manager
        with dummy:
            assert dummy.__name__ == 'Null'  # Name should return a six.text_type

        # Null objects are always equal to other null object
        assert n != 1
        assert n == dummy

    def testNullCopy(self):
        n = Null()
        n1 = copy.copy(n)
        assert six.text_type(n) == six.text_type(n1)

    def testStringDictIO(self, embed_data):
        # Create a regular dict
        dictionary = dict(foo='bar', key='value')

        # Save it to a file
        obtained_file = embed_data.GetDataFilename('obtained_file.txt')
        StringDictIO.Save(dictionary, obtained_file, sort_items=True)

        # Create a file by hand
        expected_file = embed_data.GetDataFilename('expected_file.txt')
        CreateFile(expected_file, 'foo = bar\nkey = value\n')

        # Syntax should match
        embed_data.AssertEqualFiles(obtained_file, expected_file)

        # Load a dict from our file
        new_dictionary = StringDictIO.Load(obtained_file)

        # That dict should match the original
        assert new_dictionary == dictionary

        filename = embed_data['testStringDictIO.txt']
        CreateFile(filename, 'first=alpha\nsecond = bravo\nthird =   charlie')
        loaded_dictionary = StringDictIO.Load(filename)
        assert loaded_dictionary == dict(first='alpha', second='bravo', third='charlie')

        loaded_dictionary = StringDictIO.Load(filename, inverted=True)
        assert loaded_dictionary == dict(alpha='first', bravo='second', charlie='third')

    def testStringDictIOEmptyFile(self, embed_data):
        # Make sure this works with empty files.
        filename = embed_data.GetDataFilename('empty_dict')
        CreateFile(filename, contents='')

        dictionary = StringDictIO.Load(filename)

        assert len(dictionary) == 0

    def testStringDictIODictWithSpaces(self, embed_data):
        filename = embed_data.GetDataFilename('dict_with_spaces.txt')

        dict_with_spaces = {'key with spaces' : 'value with spaces'}

        StringDictIO.Save(dict_with_spaces, filename)

        assert GetFileContents(filename) == 'key with spaces = value with spaces\n'
        assert StringDictIO.Load(filename) == dict_with_spaces

    def testStringDictIOOrderAndSorted(self, embed_data):
        filename = embed_data.GetDataFilename('dict.txt')

        from ben10.foundation import odict
        ordered_dict = odict.odict()
        ordered_dict['z'] = 'first'
        ordered_dict['a'] = 'last'

        # Test order
        StringDictIO.Save(ordered_dict, filename)
        assert GetFileContents(filename) == 'z = first\na = last\n'

        # Test sorted
        StringDictIO.Save(ordered_dict, filename, sort_items=True)
        assert GetFileContents(filename) == 'a = last\nz = first\n'

    def testStructMap(self):

        a = {'alpha' : [1, 2, 3], 'bravo' : (1, 2, 3)}

        obtained = StructMap(
            a,
            func=six.text_type,
            conditional=lambda x: isinstance(x, int)
        )
        expected = {'alpha' : ['1', '2', '3'], 'bravo' : ('1', '2', '3')}
        assert obtained == expected

    def testFlattenDictValues(self):
        assert sorted(FlattenDictValues({'a' : 1, 'b' : 2})) == list(range(1, 3))
        assert sorted(FlattenDictValues({'a' : 1, 'b' : { 'c' : 2 }})) == list(range(1, 3))
        assert sorted(FlattenDictValues({'a' : 1, 'b' : [2, 3]})) == list(range(1, 4))
        assert sorted(FlattenDictValues({'a' : 1, 'b' : { 'c' : [2, 3]}})) == list(range(1, 4))
        assert sorted(FlattenDictValues({'a' : 1, 'b' : { 'c' : [2, {'d' : 3}]}})) == list(range(1, 4))
        assert sorted(FlattenDictValues({'a' : 1, 'b' : [{'c' : 2}, 3, [4, [5]]]})) == list(range(1, 6))

        with pytest.raises(ValueError):
            FlattenDictValues([1, 2])
        with pytest.raises(ValueError):
            FlattenDictValues(1)

    def testFlattenDictValuesWithODict(self):
        d = odict()
        d['z'] = 1

        inner_dict = odict()
        inner_dict['key'] = 2

        d['a'] = [
            inner_dict,
            3,
            [
                4,
                [5]
            ]
        ]
        assert FlattenDictValues(d) == list(range(1, 6))


def testRemoveDuplicates():
    elements = [(1,), (1,), (7,), (3,), (1,)]
    assert len(elements) == 5
    no_duplicates = RemoveDuplicates(elements)
    assert len(no_duplicates) == 3
    # Keep order.
    order = [elements.index(x) for x in no_duplicates]
    assert all(order[i] < order[i + 1] for i in range(len(order) - 1))


def testRemoveDuplicatesById():
    elements = [(1,), (1,), (7,), (3,), (1,)]
    assert len(elements) == 5
    no_duplicates = RemoveDuplicatesById(elements)
    assert len(no_duplicates) == 5

    elements[1] = elements[0]
    elements[4] = elements[0]
    no_duplicates = RemoveDuplicatesById(elements)
    assert len(no_duplicates) == 3
    # Keep order.
    order = [elements.index(x) for x in no_duplicates]
    assert all(order[i] < order[i + 1] for i in range(len(order) - 1))
