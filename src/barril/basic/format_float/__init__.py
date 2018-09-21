'''
Locale-aware methods that convert to and from float values, trying to give the best representation
possible.
'''
from __future__ import absolute_import, unicode_literals

import math
from decimal import ROUND_HALF_EVEN, Decimal

import six

#===================================================================================================
# Constants
#===================================================================================================

PLUS_INFINITY = float('inf')
PLUS_INFINITY_STR = "+INF"

MINUS_INFINITY = float('-inf')
MINUS_INFINITY_STR = "-INF"

NAN = float('nan')
NAN_STR = "-1.#IND"


#===================================================================================================
# FormatFloat
#===================================================================================================
def FormatFloat(pattern, value, grouping=False, use_locale=True):
    '''
    Formats the value given according to the current LC_NUMERIC setting. The format follows the
    conventions of the % operator. For floating point values, the decimal point is modified if
    appropriate. If grouping is True, the thousands separator set in locale settings is also taken
    into account.

    @note:
        This function is used to format float values. There are known issues like convert unit
        from scalar where value is "0.0", it can get representation "-0.0"

    :param unicode pattern:
        The pattern used to format the value.

    :param float value:
        The value to be formated.

    :param bool grouping:
        True if the thousands separator must be used on formating the number. The locale settings
        must be explicitly set in order to make sure the thousands separator will be applied. The
        default value for thousands separator is "", so that the value formated won't have thousands
        separator.

    :param bool use_locale:
        Use locale.format or unicode % operator (locale-independent output).

    :rtype: unicode
    :returns:
        The formated value.
    '''
    # Handling INFINITY
    # - locale.format tries to round the infinity value:
    #   ( ".3g", 9e999 ) ==> +1.#J
    import locale

    if value == PLUS_INFINITY:
        return PLUS_INFINITY_STR
    elif value == MINUS_INFINITY:
        return MINUS_INFINITY_STR
    elif value != value:  # Not a Number
        # numpy.isnan(x) is more readable, but it doesn't work here because FractionValue-s seem to
        # pass numpy arrays to FormatFloat, and numpy.isnan doesn't accept them.
        return NAN_STR

    # This removes the minus sign from the string representation of the float
    if value == 0.0:
        value = 0.0

    if use_locale:
        try:
            result = locale.format_string(pattern, value, grouping)
        except TypeError:
            # Python has a limitation to convert large float numbers to integer format.
            # To avoid this the values will be forced to int when requesting for the integer format.
            result = locale.format_string(pattern, int(value), grouping)
    else:
        result = pattern % value

    return result


#===================================================================================================
# FloatFromString
#===================================================================================================
def FloatFromString(str_value, use_locale=True):
    '''
    Converts the given string value into a float, taking in account the current locale.

    :param unicode str_value:

    :rtype: float
    :returns:
        The equivalent float value

    :param bool use_locale:
        Use locale.atof or standard float conversion (default python output, locale-independent).

    :raises ValueError:
        If given string is not a valid float literal in the current locale
    '''
    import locale

    if str_value.__class__ != six.text_type:
        from barril._foundation.types_ import CheckType
        CheckType(str_value, six.text_type)

    if str_value == PLUS_INFINITY_STR:
        return PLUS_INFINITY
    elif str_value == MINUS_INFINITY_STR:
        return MINUS_INFINITY
    elif str_value == NAN_STR:
        return NAN
    elif use_locale:
        # In Python 2 use byte string within locale's atof, so to avoid any decode error.
        if six.PY2:
            str_value = str_value.encode(locale.getpreferredencoding())
        return locale.atof(str_value)
    else:
        return float(str_value)

