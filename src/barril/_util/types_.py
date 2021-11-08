"""
Extensions to python native types.
"""
from typing import Any
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

_TRUE_VALUES = ["TRUE", "YES", "1"]
_FALSE_VALUES = ["FALSE", "NO", "0"]
_TRUE_FALSE_VALUES = _TRUE_VALUES + _FALSE_VALUES
_KNOWN_NUMBER_TYPES: Any = None


def _GetKnownNumberTypes() -> Tuple[type, ...]:
    """
    Dynamically obtain the tuple with the types considered number, including numpy.number if
    possible.

    This code replaces an old implementation with "code replacement". Not checked if we have any
    performance penalties.
    """
    result = {float, complex, int}
    try:
        import numpy
    except ImportError:
        pass
    else:
        result.add(numpy.number)
    return tuple(result)


def CheckType(
    object_: Any, type_: Union[type, Tuple[type, ...]], message: Optional[str] = None
) -> None:
    """
    Check if the given object is of the given type, raising a descriptive "TypeError" if it is
    not.

    :param object_:
        The object to check the type

    :param type_:
        The type or types to check.

    :param message:
        The error message shown if the check does not pass.
        By default, generates the following message:

            CheckType: Expecting <expected type(s)>, got <object type>: <object>

    @raise: TypeError:
        Raises type-error if the object does not matches the given type(s).
    """
    if not isinstance(object_, type_):
        # 001) The list of the types names.
        type_names_parts = [x if isinstance(x, str) else x.__name__ for x in MakeTuple(type_)]
        type_names = '" or "'.join(type_names_parts)

        # 002) Build the error message
        exception_message = 'CheckType: Expecting "{}", got "{}": {}'.format(
            type_names, object_.__class__.__name__, repr(object_)
        )

        # 003) Appends the user message at the end
        if message:
            exception_message += "\n%s" % message

        # 004) Raises the exception
        raise TypeError(exception_message)


def CheckFormatString(pattern: str, *arguments: Any) -> None:
    """
    Checks if the given format string (for instance, "%.g") is valid for the given arguments.
    :param pattern: a string in "%" format
    :param arguments: the arguments to check against
    :raises ValueError:
        if the format is invalid.
    """
    try:
        pattern % arguments
    except (TypeError, ValueError):
        raise ValueError("%r is not a valid format string." % pattern)


def IsNumber(v: object) -> bool:
    """
    Checks if the given value is a number

    :return:
        True if the given value is a number, False otherwise
    """
    global _KNOWN_NUMBER_TYPES
    if not _KNOWN_NUMBER_TYPES:
        _KNOWN_NUMBER_TYPES = _GetKnownNumberTypes()

    return isinstance(v, _KNOWN_NUMBER_TYPES)


def MakeTuple(object_: Any) -> Tuple[Any, ...]:
    """
    Returns the given object as a tuple, if it is not, creates one with it inside.

    @param:
        The object to tupleIZE
    """
    if isinstance(object_, tuple):
        return object_
    else:
        return (object_,)
