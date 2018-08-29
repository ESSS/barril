'''
Extensions to python native types.
'''

from __future__ import unicode_literals

import collections

import six

from ben10.foundation.compat import FixUnicodeStrInClassScope
from ben10.foundation.is_frozen import IsDevelopment
from ben10.foundation.klass import IsInstance
from ben10.foundation.weak_ref import WeakList

_TRUE_VALUES = ['TRUE', 'YES', '1']
_FALSE_VALUES = ['FALSE', 'NO', '0']
_TRUE_FALSE_VALUES = _TRUE_VALUES + _FALSE_VALUES
_KNOWN_NUMBER_TYPES = None


def _GetKnownNumberTypes():
    '''
    Dynamically obtain the tuple with the types considered number, including numpy.number if
    possible.

    This code replaces an old implementation with "code replacement". Not checked if we have any
    performance penalties.
    '''
    result = {float, complex}
    result.update(set(six.integer_types))
    try:
        import numpy
    except ImportError:
        pass
    else:
        result.add(numpy.number)
    return tuple(result)


#===================================================================================================
# Boolean
#===================================================================================================
def Boolean(text):
    '''
    :param str text:
        A text semantically representing a boolean value.

    :rtype: bool
    :returns:
        Returns a boolean represented by the given text.
    '''
    text_upper = text.upper()
    if text_upper not in _TRUE_FALSE_VALUES:
        raise ValueError(
            "The value does not match any known value (case insensitive): %s (%s)"
            % (text, _TRUE_FALSE_VALUES)
        )
    return text_upper in _TRUE_VALUES


#===================================================================================================
# MakeTuple
#===================================================================================================
def MakeTuple(object_):
    '''
    Returns the given object as a tuple, if it is not, creates one with it inside.

    @param: Any object or tuple
        The object to tupleIZE
    '''
    if isinstance(object_, tuple):
        return object_
    else:
        return (object_,)


#===================================================================================================
# CheckType
#===================================================================================================
def CheckType(object_, type_, message=None):
    '''
    Check if the given object is of the given type, raising a descriptive "TypeError" if it is
    not.

    :type object_: Any object
    :param object_:
        The object to check the type

    :type type_: type, tuple of types, type name, tuple of type names
    :param type_:
        The type or types to check.
        This can be a actual type or the name of the type.
        This can be one type or a list of types.

    :param str message:
        The error message shown if the check does not pass.
        By default, generates the following message:

            CheckType: Expecting <expected type(s)>, got <object type>: <object>

    @raise: TypeError:
        Raises type-error if the object does not matches the given type(s).
    '''
    result = IsInstance(object_, type_)
    if not result:
        # 001) The list of the types names.
        type_names = [x if isinstance(x, str) else x.__name__ for x in MakeTuple(type_)]
        type_names = '" or "'.join(type_names)

        # 002) Build the error message
        exception_message = 'CheckType: Expecting "%s", got "%s": %s' % (
            type_names,
            object_.__class__.__name__,
            repr(object_))

        # 003) Appends the user message at the end
        if message:
            exception_message += '\n%s' % message

        # 004) Raises the exception
        raise TypeError(exception_message)

    return result

# Either testit or removeit
# #===================================================================================================
# # Used for debugging who is calling CheckType too much.
# #===================================================================================================
# DEBUG_CALLS = False
# if DEBUG_CALLS:
#     _OriginalCheckType = CheckType
#     _called_from = {}
#
#     def CheckType(*args, **kwargs):  # @DuplicatedSignature
#         import sys
#         frame = sys._getframe()
#         code = frame.f_back.f_code
#         key = (code.co_filename, code.co_name)
#         v = _called_from.setdefault(key, 0)
#         _called_from[key] = v + 1
#         return _OriginalCheckType(*args, **kwargs)
#
#     def PrintCheckTypeStatistics():
#         for value, key in sorted((value, key) for key, value in _called_from.iteritems()):
#             print '%s: %s' % (value, key)


#===================================================================================================
# DevelopmentCheckType
# CheckType only in development mode.
#===================================================================================================
def CreateDevelopmentCheckType():
    if not IsDevelopment():
        return lambda *args, **kwargs: None  # it's a no-op if we're not in dev mode!
    else:
        return CheckType


DevelopmentCheckType = CreateDevelopmentCheckType()


#===================================================================================================
# CheckFormatString
#===================================================================================================
def CheckFormatString(format, *arguments):
    '''
    Checks if the given format string (for instance, "%.g") is valid for the given arguments.
    :type format: a string in "%" format.
    :param format:
    :type arguments: the arguments to check against.
    :param arguments:
    :raises ValueError:
        if the format is invalid.
    '''
    try:
        format % arguments
    except (TypeError, ValueError):
        raise ValueError(tr('%r is not a valid format string.') % format)


#===================================================================================================
# _IsNumber
#===================================================================================================
def _IsNumber(v):
    '''
    Actual function code for IsNumber.

    Checks if the given value is a number

    @return bool
        True if the given value is a number, False otherwise
    '''
    return isinstance(v, _KNOWN_NUMBER_TYPES)


#===================================================================================================
# IsNumber
#===================================================================================================
def IsNumber(v):
    '''
    Checks if the given value is a number

    :return bool:
        True if the given value is a number, False otherwise

    .. note:: This function will replace it's implementation to a lighter code, but first it must
        define which types are known as a number.
        The code replacement is made to avoid the call to import and listing the know numeric types.
    '''
    # There are cases were the numpy will not be available (for example when the aasimar is building
    # the environment the numpy is not available yet). Delegate this import to the IsNumber would
    # cause a severe performance impact. So we will attempt to import the numpy, but if the lib is
    # not available let us move on the know number types.
    global _KNOWN_NUMBER_TYPES
    _KNOWN_NUMBER_TYPES = _GetKnownNumberTypes()

    # Replaces this function by an optimized version _IsNumber.
    IsNumber.__code__ = _IsNumber.__code__

    return _IsNumber(v)


#===================================================================================================
# CheckIsNumber
#===================================================================================================
def CheckIsNumber(v):
    if not IsNumber(v):
        raise TypeError('Expecting a number. Received:%s (%s)' % (v, type(v)))
    return True


#===================================================================================================
# IsBasicType
#===================================================================================================
def IsBasicType(value, accept_compound=False, additional=None):
    '''
    :param object value:
        The value we want to check

    :param bool accept_compound:
        Whether lists, tuples, sets and dicts should be considered basic types

    :type additional: class or tuple(classes)
    :param additional:
        Any classes in this additional list will also be considered as basic types.

    :rtype: bool
    :returns:
        True if the passed value is from a basic python type
    '''
    if isinstance(value, _ACCEPTED_BASIC_TYPES) or \
        value is None or (additional and IsInstance(value, additional)):
        return True

    if accept_compound:
        if isinstance(value, dict):
            for key, val in six.iteritems(value):
                if (
                    not IsBasicType(key, accept_compound, additional)
                    or
                    not IsBasicType(val, accept_compound, additional)
                ):
                    return False
            return True

        if isinstance(value, (tuple, list, set, frozenset)):
            for val in value:
                if not IsBasicType(val, accept_compound, additional):
                    return False
            return True

    return False


_ACCEPTED_BASIC_TYPES = tuple(
    list(six.string_types) + list(six.integer_types) + [bytes, float, bool, complex])


#===================================================================================================
# CheckBasicType
#===================================================================================================
def CheckBasicType(value, accept_compound=False, additional=None):
    '''
    .. see:: IsBasicType for parameters descriptions.

    :rtype: True
    :returns:
        True if the passed value is from a basic python type

    :raises TypeError:
        if the value passed is not a basic type
    '''
    if not IsBasicType(value, accept_compound, additional):
        raise TypeError('Expecting a basic type. Received:%s (%s)' % (value, type(value)))
    return True


#===================================================================================================
# CheckEnum
#===================================================================================================
def CheckEnum(value, enum_values):
    '''
    Checks if the given value belongs to the given enum. This function is meant to replace code like
    this:

    ENUM_VALUE_1 = 'value1'
    ENUM_VALUE_2 = 'value2'
    ENUM_VALUES = set([ENUM_VALUE_1, ENUM_VALUE_2])

    def Foo(value):
        if value not in ENUM_VALUES:
            raise ValueError(...)

    :param object value:
        The value to test membership in the enum

    :type values: sequence of objects
    :param values:
        The values that are acceptable for this enum.

    :raises ValueError:
        if the given value does not belong to the enum.
    '''
    if value not in enum_values:
        msg = 'The value %r is not valid for the expected num: %s'
        raise ValueError(msg % (value, list(enum_values)))


#===================================================================================================
# Intersection
#===================================================================================================
def Intersection(*sequences):
    '''
    Return the intersection of all the elements in the given sequences, ie, the items common to all
    the sequences.

    :type sequences: a list of sequences.
    :param sequences:
    :rtype: a set() with the intersection.
    '''
    if not sequences:
        return set()
    result = set(sequences[0])
    for seq in sequences[1:]:
        result.intersection_update(seq)
    return result


#===================================================================================================
# OrderedIntersection
#===================================================================================================
def OrderedIntersection(*sequences):
    '''
    Like Intersection, but the returned sequence is in the order of the first one.
    '''
    intersection = Intersection(*sequences)
    if not intersection:
        return []

    return [x for x in sequences[0] if x in intersection]


#===================================================================================================
# AsList
#===================================================================================================
def AsList(arg):
    '''Returns the given argument as a list; if already a list, return it unchanged, otherwise
    return a list with the arg as only element.
    '''
    if isinstance(arg, (list, WeakList)):
        return arg

    if isinstance(arg, (tuple, set)):
        return list(arg)

    return [arg]


#===================================================================================================
# Flatten
#===================================================================================================
def Flatten(iterable, skip_types=None):
    '''
    :rtype: list
    :returns:
        A list with the elements of the initial iterable flattened.
    '''
    return list(IterFlattened(iterable, skip_types))


#===================================================================================================
# IterFlattened
#===================================================================================================
def IterFlattened(iterable, skip_types=None):
    """
    Flattens recursively the passed iterable with subsequences into a flat iterator.

    Warning: This method also flattens tuples

    :type iterable: an iterable object, ie, an object that iter() can handle
    :param iterable:
        The iterable to be flattened.

    :param list(type) skip_types:
        These types won't be flattened if they happen to be iterable.

    :rtype: iterator
    :returns: Iterator over the flattened given iterable.
    """
    if skip_types is None:
        skip_types = []

    for s in six.string_types:
        if s not in skip_types:
            # Exceptional case: we want to treat strings as elements!
            skip_types.append(s)

    skip_types_tuple = tuple(skip_types)

    for element in iterable:
        element_iter = None  # will be None if element is not iterable, or hold an iterator otherwise

        if not isinstance(element, skip_types_tuple):
            try:
                element_iter = iter(element)
            except TypeError:
                pass

        if element_iter is None:
            yield element
        else:
            for x in IterFlattened(element_iter, skip_types):
                yield x


#===================================================================================================
# IterFlattenedDictValues
#===================================================================================================
def IterFlattenedDictValues(dictionary):
    '''
    Flattens a dictionary values() recursively.

    If the outer dictionary contains an inner dictionary the inner dictionary values are also flattened.

    Other inner values that are containers will be flattened too, not only the dicts.

    :param collections.Mapping dictionary:
    :return: sequence(object)
    '''
    if not isinstance(dictionary, collections.Mapping):
        raise ValueError('Parameter "dictionary" must be a dict')
    values = IterFlattened(iter(dictionary.values()), skip_types=[collections.Mapping])
    for v in values:
        if isinstance(v, collections.Mapping):
            for v2 in IterFlattenedDictValues(v):
                yield v2
        else:
            yield v


#===================================================================================================
# FlattenDictValues
#===================================================================================================
def FlattenDictValues(dictionary):
    '''
    :param dict dictionary:
    :return: list(object)
    :see: IterFlattenedDictValues
    '''
    return list(IterFlattenedDictValues(dictionary))


#===================================================================================================
# MergeDictsRecursively
#===================================================================================================
def MergeDictsRecursively(original_dict, merging_dict):
    '''
    Merges two dictionaries by iterating over both of their keys and returning the merge
    of each dict contained within both dictionaries.
    The outer dict is also merged.

    ATTENTION: The :param(merging_dict) is modified in the process!

    :param dict original_dict
    :param dict merging_dict
    '''
    items = iter(original_dict.items())

    for key, value in items:
        try:
            other_value = merging_dict[key]
            MergeDictsRecursively(value, other_value)
            del merging_dict[key]
        except KeyError:
            continue
        except TypeError:
            continue
        except AttributeError:
            continue

    try:
        original_dict.update(merging_dict)
    except ValueError:
        raise TypeError('Wrong types passed. Expecting two dictionaries, got: "%s" and "%s"' % (type(original_dict).__name__, type(merging_dict).__name__))

    return original_dict


#===================================================================================================
# ListDuplicates
#===================================================================================================
def ListDuplicates(iterable):
    '''
    Given a sequence, returns a list containing all the items in 'iterable' that appear more than
    once. E.g. ListDuplicates([1,2,3,1]) returns [1].

    :type iterable: an iterable object, ie, an object that iter() can handle.
    '''
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set(x for x in iterable if x in seen or seen_add(x))
    # turn the set into a list (as requested)
    return list(seen_twice)


#===================================================================================================
# RemoveDuplicates
#===================================================================================================
def RemoveDuplicates(iterable):
    '''
    Given a sequence, returns a list with duplicate elements removed (only the first appearance
    of the element is kept). Preserves order.

    :type iterable: an iterable object, ie, an object that iter() can handle.
    '''
    seen = set()
    seen_add = seen.add
    return [ x for x in iterable if x not in seen and not seen_add(x)]


#===================================================================================================
# RemoveDuplicatesById
#===================================================================================================
def RemoveDuplicatesById(iterable):
    '''
    Similar to `RemoveDuplicates` but using the object `id` as filter.

    :type iterable: an iterable object, ie, an object that iter() can handle.
    '''
    seen = set()
    seen_add = seen.add
    result = []
    result_append = result.append
    for x in iterable:
        x_id = id(x)
        if x_id not in seen:
            seen_add(x_id)
            result_append(x)
    return result


#===================================================================================================
# Method
#===================================================================================================
class Method(object):
    '''
    This class is an 'organization' class, so that subclasses are considered as methods
    (and its __call__ method is checked for the parameters)
    '''


#===================================================================================================
# Null
#===================================================================================================
class Null(object):
    '''
    This is a sample implementation of the 'Null Object' design pattern.

    Roughly, the goal with Null objects is to provide an 'intelligent'
    replacement for the often used primitive data type None in Python or
    Null (or Null pointers) in other languages. These are used for many
    purposes including the important case where one member of some group
    of otherwise similar elements is special for whatever reason. Most
    often this results in conditional statements to distinguish between
    ordinary elements and the primitive Null value.

    Among the advantages of using Null objects are the following:

      - Superfluous conditional statements can be avoided
        by providing a first class object alternative for
        the primitive value None.

      - Code readability is improved.

      - Null objects can act as a placeholder for objects
        with behaviour that is not yet implemented.

      - Null objects can be replaced for any other class.

      - Null objects are very predictable at what they do.

    To cope with the disadvantage of creating large numbers of passive
    objects that do nothing but occupy memory space Null objects are
    often combined with the Singleton pattern.

    For more information use any internet search engine and look for
    combinations of these words: Null, object, design and pattern.

    Dinu C. Gherman,
    August 2001

    ---

    A class for implementing Null objects.

    This class ignores all parameters passed when constructing or
    calling instances and traps all attribute and method requests.
    Instances of it always (and reliably) do 'nothing'.

    The code might benefit from implementing some further special
    Python methods depending on the context in which its instances
    are used. Especially when comparing and coercing Null objects
    the respective methods' implementation will depend very much
    on the environment and, hence, these special methods are not
    provided here.
    '''

    # object constructing

    def __init__(self, *_args, **_kwargs):
        "Ignore parameters."
        # Setting the name of what's gotten (so that __name__ is properly preserved).
        self.__dict__['_Null__name__'] = 'Null'
        return None

    # object calling

    def __call__(self, *_args, **_kwargs):
        "Ignore method calls."
        return self

    # attribute handling

    def __getattr__(self, mname):
        "Ignore attribute requests."
        if mname == '__getnewargs__':
            raise AttributeError('No support for that (pickle causes error if it returns self in this case.)')

        if mname == '__name__':
            return self.__dict__['_Null__name__']

        return self

    def __setattr__(self, _name, _value):
        "Ignore attribute setting."
        return self

    def __delattr__(self, _name):
        "Ignore deleting attributes."
        return self

    # context manager

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return self

    # misc.

    def __repr__(self):
        "Return a string representation."
        return "<Null>"

    def __str__(self):
        "Convert to a string and return it."
        return "Null"

    FixUnicodeStrInClassScope()

    def __bool__(self):
        "Null objects are always false"
        return False

    def __nonzero__(self):
        # Py 2 compatibility
        return self.__bool__()

    # iter

    def __iter__(self):
        "I will stop it in the first iteration"
        return self

    def __next__(self):
        "Stop the iteration right now"
        raise StopIteration()

    def next(self):
        # Py 2 compatibility
        return self.__next__()

    def __eq__(self, o):
        "It is just equal to another Null object."
        return self.__class__ == o.__class__


NULL = Null()  # Create a default instance to be used.


#===================================================================================================
# StringDictIO
#===================================================================================================
class StringDictIO(object):
    '''
    Saves dictionaries into plain text files.

    Assumes all keys and values are strings.

    e.g.:
        my_dict = {'Ak':'Av', 'Bk':'Bv'}

        would save as:

        Ak = Av
        Bk = Bv
    '''

    @classmethod
    def Save(cls, dictionary, target_filename, sort_items=False):
        '''
        Writes a dictionary into a file.

        :param str filename:
            Path and filename for target file.

        :param bool sort_items:
            If True, saved dict will be sorted alphabetically
        '''
        items = list(six.iteritems(dictionary))
        if sort_items:
            items = sorted(items)

        contents = '\n'.join(['%s = %s' % i for i in items]) + '\n'

        from ben10.filesystem import CreateFile
        CreateFile(target_filename, contents)

    @classmethod
    def Load(cls, filename, inverted=False):
        '''
        Loads a dictionary from a file.

        :param str filename:
            Path and filename for source file.

        :param bool inverted:
            If True inverts the key/value order.

        :returns dict:
            Dictionary that was loaded
        '''
        from ben10.filesystem import GetFileContents
        contents = GetFileContents(filename)

        contents_dict = dict()
        import re

        for line in contents.split('\n'):
            search_result = re.search('(.*?)\s*=\s*(.*)', line)
            if search_result is not None:
                key, value = search_result.groups()
                if inverted:
                    contents_dict[value] = key
                else:
                    contents_dict[key] = value

        return contents_dict


#===================================================================================================
# StructMap
#===================================================================================================
def StructMap(obj, func, conditional=lambda x:True):
    '''
    Maps an object recursively for dict/tuple/list types.

    :param callable func:
        Called for each non-container value IF conditional returns True.

    :param callable conditional:
        Filters which values to execute func.

    :return object:
        Returns a copy of the object with all non-container types mapped via func.

    Example:
        Converts all "bytes" instances to "str" inside nested container objects

        struct = {
            'name' : 'Alpha',
            'numbers' : (1,2,3),
            'surnames' : ('Bravo', 'Charlie'),
        }

        struct = StructMap(
            struct,
            lambda x: x.decode('UTF-8'),
            lambda x: isinstance(x, str)
        )

        struct = {
            u'name' : u'Alpha',
            u'numbers' : (1,2,3),
            u'surnames' : (u'Bravo', u'Charlie'),
        }
    '''
    if isinstance(obj, dict):
        return {
            StructMap(i, func, conditional):StructMap(j, func, conditional)
            for i, j in obj.items()
        }
    if isinstance(obj, tuple):
        return tuple(
            StructMap(i, func, conditional)
            for i in obj
        )
    if isinstance(obj, list):
        return [
            StructMap(i, func, conditional)
            for i in obj
        ]
    if conditional(obj):
        obj = func(obj)
    return obj
