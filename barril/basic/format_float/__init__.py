'''
Locale-aware methods that convert to and from float values, trying to give the best representation
possible.
'''
from __future__ import absolute_import, unicode_literals

import math
from decimal import ROUND_HALF_EVEN, Decimal

import six
from six import unichr as chr

#===================================================================================================
# Constants
#===================================================================================================
PLUS_INFINITY_STR = "+INF"
MINUS_INFINITY_STR = "-INF"
NAN_STR = "-1.#IND"

_C_DOUBLE_DIGITS = 53

_C_DOUBLE_MANTISSA = 2 ** _C_DOUBLE_DIGITS

_C_2POWERS_MINIMUM = (-1074 - _C_DOUBLE_DIGITS)
_C_2POWERS_MAXIMUM = 1023

_C_10POWERS_OFFSET = 50
_C_10POWERS = None


#===================================================================================================
# ToDecimal
#===================================================================================================
def ToDecimal(x):
    '''
    Converts a floating point number to Decimal format. Note: will convert to the TRUE value
    that this floating point number is representing (rounded to the current Decimal precision).

    @note This is still SLOW when used for conversion of many numbers, essentially because
          python Decimal is SLOW.

    Examples:
        ToDecimal(    0.1   ) -> Decimal("0.1000000000000000055511151231")
        ToDecimal(-7147.5355) -> Decimal("-7147.535499999999956344254315")
        ToDecimal(    1.0e23) -> Decimal("99999999999999991611392")

    :param float x:
        Floating point number to be converted to Decimal.

    :rtype: Decimal
    :returns:
        The number as a decimal.
    '''
    from coilib50.basic.format_float._format_float_data import _C_2POWERS_MANTISSA_AND_EXP

    m, e = math.frexp(x)  # mantissa, exponent
    sign = 0
    if m < 0:
        m = -m
        sign = 1

    result = int(m * _C_DOUBLE_MANTISSA)

    m2, e2 = _C_2POWERS_MANTISSA_AND_EXP[(e - _C_DOUBLE_DIGITS) - _C_2POWERS_MINIMUM]

    digits = tuple(ord(i) - ord('0') for i in format(result * m2, 'd'))
    result = Decimal((sign, digits, e2))

    return result


#===================================================================================================
# ToFixed
#===================================================================================================
def ToFixed(x, num_digits, after_decimal):
    '''
    Equivalent of '%*.*f' % (num_digits, after_decimal, x), but in a way that should give the
    same result on different platforms.

    Example:
        ToFixed(-7147.5355, 10, 3) -> " -7147.535"
                                       ^^^^^^^^^^ (num_digits=10)
                                              ^^^ (after_decimal=3)
                                       ^          (space padding before)

    :param float x:
        Floating point number to be converted to fixed precision

    :param int num_digits:
        Total number of characters (including sign and decimal separator!). Will left pad with
        spaces in case the generated is string have less characters.

    :param int after_decimal:
        Fixed number of decimal digits after the decimal separator.

    :rtype: unicode
    :returns:
        A string with the number formatted with "fixed precision".

    .. note:: The bug was fixed but this is slow now ;(
    @todo: Improve performance. All this formatting code should probably be moved to C++...
    '''
    d = ToDecimal(x)

    ################################################################################################
    # _rescale does not suffer from "quantize result has too many digits for current context"
    # (but currently does not work for some values as well...)
    #
    # if _C_10POWERS is None:
    #    _C_10POWERS = [_C_DECIMAL_10 ** i for i in xrange(-_C_10POWERS_OFFSET, _C_10POWERS_OFFSET + 1)]
    # d = d.quantize(_C_10POWERS[-after_decimal + _C_10POWERS_OFFSET])
    #
    # The commented code could be important in case we find some problem with _rescale...
    # (it took some time to dig into that)
    ################################################################################################

    if six.PY2:
        d = d._rescale(-after_decimal, rounding=ROUND_HALF_EVEN)
    else:
        global _C_10POWERS
        if _C_10POWERS is None:
            _C_10POWERS = [Decimal(10) ** i for i in range(-_C_10POWERS_OFFSET, _C_10POWERS_OFFSET + 1)]
        d = d.quantize(_C_10POWERS[-after_decimal + _C_10POWERS_OFFSET], rounding=ROUND_HALF_EVEN)

    sign, digits, exponent = d.as_tuple()

    if sign == 0:
        sign_str = ' '
    else:
        sign_str = '-'

    ord_0 = ord('0')
    digits_str = ''.join(chr(ord_0 + n) for n in digits)

    decimal_separator_pos = len(digits_str) + exponent

    if decimal_separator_pos > 0 and decimal_separator_pos <= len(digits):
        result = (
            sign_str + digits_str[0:decimal_separator_pos]
            +'.' + digits_str[decimal_separator_pos:]
        )
    elif decimal_separator_pos <= 0:
        result = sign_str + '0.' + '0' * (-decimal_separator_pos) + digits_str
    else:
        result = sign_str + digits_str + '0' * (exponent) + '.'

    result = result.rjust(num_digits)
    return result


#===================================================================================================
# FormatFloat
#===================================================================================================
def FormatFloat(format, value, grouping=False, use_locale=True):
    '''
    Formats the value given according to the current LC_NUMERIC setting. The format follows the
    conventions of the % operator. For floating point values, the decimal point is modified if
    appropriate. If grouping is True, the thousands separator set in locale settings is also taken
    into account.

    @note:
        This function is used to format float values. There are known issues like convert unit 
        from scalar where value is "0.0", it can get representation "-0.0"

    :param unicode format:
        The format used to format the value.

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
    from coilib50.basic.constants import MINUS_INFINITY, PLUS_INFINITY
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
            result = locale.format(format, value, grouping)

        # TODO: Mantis 0021011
        except TypeError:
            # Python has a limitation to convert large float numbers to integer format.
            # To avoid this the values will be forced to int when requesting for the integer format.
            result = locale.format(format, int(value), grouping)
    else:
        result = format % value

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
    from coilib50.basic.constants import MINUS_INFINITY, NAN, PLUS_INFINITY
    import locale

    if str_value.__class__ != six.text_type:
        from ben10.foundation.types_ import CheckType
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


#===================================================================================================
# PlatformIndependentFormat
#===================================================================================================
def PlatformIndependentFormat(format, value):
    '''
    Formats the given float value in a manner that results in the same string in all platforms.
    Useful mostly to write numbers using COG that provides the same results in all platforms.

    :param unicode format:
        The string formatting to use, for instance "%s" or "%0.3g".

    :param float value:
        The value to format

    :rtype: unicode
    :returns:
        The string formatted as requested.
    '''
    result = format % value

    # fix exponential differences between platforms:
    # windows: "1.0e016"
    # linux: "1.0e16"
    # fix: "1.0e16"
    # docs for fprintf:
    # "The exponent always contains at least two digits, and only as many more
    #  digits as necessary to represent the exponent."
    fields = result.split('e')
    if len(fields) == 2:
        exp_str = fields[1]
        exp_value = int(exp_str)
        if -10 < exp_value < 0:
            # if we have a single negative digit, use 03d to format the exponent because 02d would
            # generate "-8" for instance
            exp_str = '%03d' % exp_value
        else:
            exp_str = '%02d' % exp_value
        result = fields[0] + 'e' + exp_str

    return result


def FormatFloatLocalizedRepr(value, decimal):
    as_string = '%r' % (value,)
    if decimal == '.':
        return as_string
    return as_string.replace('.', decimal)