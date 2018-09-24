from __future__ import absolute_import, division, unicode_literals

import locale
import math
import re

import six

from barril._foundation.types_ import CheckType
from barril.basic.format_float import FloatFromString
from barril.basic.fraction import Fraction


#===================================================================================================
# FractionValue
#===================================================================================================
class FractionValue(object):
    '''
    Simple class that acts as a container for both a number and a fraction. Useful
    to aggregate both concepts in a single object.

    To get the actual value as a float, just call float() on the FractionValue object.

    Usage example:
        foo = FractionValue(1.25, Fraction(3, 4))
        print float(foo) # 2.0 == 1.25 + 3/4
        print unicode(foo) # '1.25 3/4'

    .. note:: neither number nor fractional part can be None, TypeError will be raised whenever an
           attempt to set any of these parts as None is performed.
    .. note:: there's no unit associated with this object. Check L{FractionScalar} for that.
    .. note:: no arithmetic operators have been implemented, but they're certainly interesting if the
           need arises.
    '''

    def __init__(self, number=0.0, fraction=(0.0, 1.0)):
        '''
        Constructor.

        :param float number:
            The number part for the FractionValue

        :type fraction: Fraction or tuple(float, float)
        :param fraction:
            The fraction for this FractionValue object. A pair (numerator, denominator)
            is also accepted.

        .. note:: Fraction default in init method is a tuple to avoid the caveat of sharing same
            default fraction instance among different instances of this class.
        '''
        self.SetNumber(number)
        self.SetFraction(fraction)

    # Number ---------------------------------------------------------------------------------------

    def SetNumber(self, number):
        '''
        Sets the number part.

        :type number: float or int
        :param number:
            The integer part.
        '''
        CheckType(number, (int, float))
        self._number = number

    def GetNumber(self):
        '''
        :rtype: float or int
        :returns:
            Returns the number part.
        '''
        return self._number

    number = property(GetNumber, SetNumber)

    # Fraction -------------------------------------------------------------------------------------

    def SetFraction(self, fraction):
        '''
        Sets the fractional part of this object.

        :type fraction: Fraction or tuple(float, float)
        :param fraction:
            The fraction for this FractionValue object. A pair (numerator, denominator)
            is also accepted.
        '''
        CheckType(fraction, (Fraction, tuple))

        # convert a tuple
        if isinstance(fraction, tuple):
            if len(fraction) != 2:
                raise ValueError('Expected a tuple (numerator, denominator), got %r' % (fraction,))
            fraction = Fraction(*fraction)

        self._fraction = fraction

    def GetFraction(self):
        '''
        Returns the fractional part for this object.

        :rtype: Fraction
        :returns:
            The fractional part.
        '''
        return self._fraction


    fraction = property(GetFraction, SetFraction)

    # Str/Repr -------------------------------------------------------------------------------------

    def GetLocalizedString(self):
        '''
        :rtype: unicode
        :returns:
            Returns a locale-dependent and user-friendly string representation.
        '''
        from barril.basic.format_float import FormatFloat
        return self.__FormatToString(FormatFloat)

    def GetLocalizedFraction(self):
        '''
        :rtype: unicode
        :returns:
            Returns a locale-dependent and user-friendly string representation only of fraction
            part.
        '''
        from barril.basic.format_float import FormatFloat
        return self.__FormatFractionToString(FormatFloat)

    def __str__(self):
        '''
        :rtype: unicode
        :returns:
            Returns a locale-agnostic and user-friendly string representation.
        '''
        return self.__FormatToString(lambda pattern, value : pattern % value)

    if six.PY2:
        __unicode__ = __str__
        del __str__

    def __FormatToString(self, formatter):
        '''
        :param callable formatter:
            A function that receives, respectively, string format to convert value and a float
            value. Must return a string representation of value.

        :rtype: unicode
        :returns:
            Fraction values follow format "%(number)g %(fraction)s".
        '''
        formatted = formatter('%g', self._number)
        if float(self._fraction) != 0.0:
            formatted = '%s %s' % (formatted, self.__FormatFractionToString(formatter))
        return formatted

    def __FormatFractionToString(self, formatter):
        '''
        :param callable formatter:
            A function that receives, respectively, string format to convert value and a float
            value. Must return a string representation of fractional part.

        :rtype: unicode
        :returns:
            Fractional part follows format "%(fraction)s". Whenever fractional part is equivalent to
            zero it is omitted from string to be more user-friendly.
        '''
        formatted = ''
        if float(self._fraction) != 0.0:
            formatted = formatter('%s', self._fraction)
        return formatted

    def __repr__(self):
        '''
        :rtype: unicode
        :returns:
            Returns the programmer-friendly string representation.
        '''
        return 'FractionValue(%g, %s)' % (self._number, self._fraction)

    # Equality -------------------------------------------------------------------------------------

    def __eq__(self, other):
        '''
        Implements '==' binary operator.

        :param FractionValue other:
            Other FractionValue object
        '''
        if type(self) is not type(other):
            return False
        return self._number == other._number and self._fraction == other._fraction

    def __ne__(self, other):
        '''
        Implements '!=' binary operator.

        :param FractionValue other:
            Other FractionValue object
        '''
        return not self == other

    # Comparisons ----------------------------------------------------------------------------------

    def __lt__(self, other):
        '''
        Implements '<' binary operator.

        :param FractionValue other:
            Other FractionValue object
        '''
        return float(self) < float(other)

    def __le__(self, other):
        '''
        Implements '<=' binary operator.

        :param FractionValue other:
            Other FractionValue object
        '''
        return float(self) <= float(other)

    def __gt__(self, other):
        '''
        Implements '>' binary operator.

        :param FractionValue other:
            Other FractionValue object
        '''
        return float(self) > float(other)

    def __ge__(self, other):
        '''
        Implements '>' binary operator.

        :param FractionValue other:
            Other FractionValue object
        '''
        return float(self) >= float(other)

    # Float ----------------------------------------------------------------------------------------

    def __float__(self):
        '''
        Implements float() operator.

        :rtype: float
        :returns:
            The float value of this FractionValue
        '''
        return self._number + float(self._fraction)

    # Copy -----------------------------------------------------------------------------------------

    def __copy__(self):
        '''
        Returns a copy of this fraction value object.

        :rtype: FractionValue
        :returns:
            The copy.
        '''
        return self.__class__(self._number, (self._fraction.numerator, self._fraction.denominator))

    # FromString -----------------------------------------------------------------------------------

    # : regular expression to validate input text as a FractionValue, accepting:
    # : "5.0" (single number, without fraction)
    # : "5.0 3/4" (number followed by a fraction)
    # : "3/4" (single fraction)
    NUMBER_EXPR = '''
        [-+]?\d+(?:(\.|\,)\d+)     # number, float, accepting "." or ",".
    '''

    FRACTION_PART_EXPR = '''
        (?:
        (?P<numerator>%s?)         # numerator
        \s*/\s*                    # '/' no matter if exist spaces
        (?P<denominator>\d+)       # only integers
        )?
    ''' % NUMBER_EXPR

    FRACTION_COMPLETE_EXPR = '''
        (?P<float>%s?)             # The whole number
        \s*                        # space between number and fraction
        (%s)?                      # entire fractional part is optional
        ''' % (NUMBER_EXPR, FRACTION_PART_EXPR)

    _FRACTION_RE = re.compile(
        "^" + FRACTION_COMPLETE_EXPR + "$",
        re.VERBOSE  # Enables the documentation in the regular expression.
    )

    _FRACTION_PARTIAL_RE = re.compile(
        "^" + FRACTION_PART_EXPR + "$",
        re.VERBOSE  # Enables the documentation in the regular expression.
    )

    @classmethod
    def CreateFromString(cls, text, consider_locale=True):
        '''
        Create a FractionValue from a string.

        :param unicode text:
            The text with a fraction-value, that is, three integers separated by space and slash
            respectively.
            <value> <value>/<value>

        :param bool consider_locale:
            Consider the locale on converting string to float

        :rtype: FractionValue
        :returns:
            The fraction value

        :raises ValueError:
            If the text is not convertible to a FractionValue
        '''
        text = six.text_type(text).strip()

        if consider_locale:
            string_to_float_callable = FloatFromString
        else:
            string_to_float_callable = float

        # First try to match only the fractional part.
        m = cls._FRACTION_PARTIAL_RE.match(text)
        if m is not None:
            number = None
        else:
            # If can't match a fraction try a mixed number
            m = cls._FRACTION_RE.match(text)
            if m is None:
                raise ValueError(tr('Please enter a text in the form: "5 3/4"'))
            number = m.group('float')

        if number is None:
            number = 0.0
        else:
            number = string_to_float_callable(number)

        if m.group('numerator') is not None and m.group('denominator') is not None:
            numerator = string_to_float_callable(m.group('numerator'))
            denominator = locale.atoi(m.group('denominator'))
            fraction = Fraction(numerator, denominator)
        else:
            fraction = Fraction(0.0, 1.0)

        return FractionValue(number, fraction)

    @classmethod
    def MatchFractionPart(cls, text):
        '''
        Verify if the given text matchs only the fractional part of a fraction value.

        :param unicode text:
            The given text to verify matching

        @raise: ValueError
            When the text not match the expression, like "3 1/2"
        '''
        text = six.text_type(text).strip()
        m = cls._FRACTION_PARTIAL_RE.match(text)
        if m is None:
            raise ValueError('Please enter a text in the form: "3/4"')

    @classmethod
    def CreateFromFloat(cls, value):
        '''
        Convert a float or integer value to their representation in fraction.

        Example:
            result = FractionValue.CreateFromFloat(0.375) // returns FractionValue(fraction=(3,8))

        :type value: float or int
        :param value:
            The value that will be converted to fraction.

        :rtype: FractionValue
        :returns:
            The fractional number.

        .. note:: This code was copied from Alan Hensel at http://www.mindspring.com/~alanh/fracs.html
        and changed to work with negative inputs.
        '''

        def FindNumerator(number_of_digits_past_decimal, dividend, divisor):
            result = dividend
            while number_of_digits_past_decimal > 0 and result % divisor == 0:
                result /= divisor
                number_of_digits_past_decimal -= 1
            return result

        def GetMaxNumerator(value):
            str_value = six.text_type(value)
            ixe = str_value.lower().find("e")

            # How many digits?
            if ixe == -1:
                f2 = str_value
            else:
                f2 = str_value[0:ixe]
            ix = f2.find(".")
            if ix == -1:
                digits = f2
            elif ix == 0:
                digits = f2[1:]
            elif ix < len(f2):
                digits = f2[0: ix] + f2[ix + 1:]
            else:
                digits = ""
            number_of_digits = len(digits)

            # How many integer digits?
            if value == 0.0:
                number_of_integer_digits = 0
            else:
                number_of_integer_digits = len(str_value)

            # How many digits past decimal?
            number_of_digits_past_decimal = number_of_digits - number_of_integer_digits

            # Find the numerator when the divisor is 2
            result = FindNumerator(
                number_of_digits_past_decimal, dividend=float(digits), divisor=2
            )

            # Find the numerator when the divisor is 5
            result = FindNumerator(
                number_of_digits_past_decimal, dividend=result, divisor=5
            )

            return int(result)

        def GetNaN():
            infinity = 1e10000
            return infinity / infinity

        def GetFractionalPart(value):
            str_value = six.text_type(value)
            pos = str_value.find(".");
            return float("0." + str_value[pos + 1:])

        # The value is None?
        if value is None:
            return None

        # The type is float or integer?
        value_type = type(value)
        if value_type != float and value_type != int:
            raise TypeError("The value type must be int or float")

        # The fractional part exist?
        if float(value) % 1 == 0.0:
            return FractionValue(value)

        # Keep the sign of the given value and work with its absolute value. The sign will be added
        # to the generated fraction at the end.
        sign = value / abs(value)
        value = abs(value)

        integer_part = int(value)
        fractional_part = GetFractionalPart(value)
        str_fractional_part = six.text_type(fractional_part)
        max_numerator = GetMaxNumerator(fractional_part)

        # Hold the calculation
        calculation = GetNaN()
        previous_calculation = GetNaN()

        # Numerators and denominators
        numerator = 0
        denominator = 0
        numerators = [0, 1]
        denominators = [1, 0]

        i = 2
        while i < 1000:

            L2 = int(math.floor(fractional_part))

            numerators.append(L2 * numerators[i - 1] + numerators[i - 2])
            if abs(numerators[i]) > max_numerator:
                break

            denominators.append(L2 * denominators[i - 1] + denominators[i - 2])

            calculation = numerators[i] / float(denominators[i])
            if six.text_type(calculation) == six.text_type(previous_calculation):
                break

            numerator = abs(numerators[i])
            denominator = abs(denominators[i])

            if six.text_type(calculation) == str_fractional_part:
                break

            previous_calculation = calculation

            fractional_part = 1 / float(fractional_part - L2)

            i += 1

        if six.text_type(numerator) == six.text_type(denominator):
            return FractionValue(integer_part)

        return FractionValue(sign * integer_part, (sign * numerator, denominator))
