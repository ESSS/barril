from __future__ import absolute_import, division, unicode_literals

from fractions import Fraction as StdFraction
from functools import total_ordering

import six

SMALL = 1e-8

NumberType = (six.integer_types, float)
SequenceType = (tuple, list)


@total_ordering
class Fraction(object):
    '''
    Numerator, denominator similar to standard fraction with support to
    float values in numerator and denominator which will be automatically
    reduced to a simpler fraction. Class has also an special handling for
    rounding and representation issues for numbers.
    '''

    def __init__(self, a, b=None):
        if a == float('inf') or a == float('-inf'):
            raise ValueError('Numerator cannot be an infinite value')

        if b == float('inf') or b == float('-inf'):
            raise ValueError('Denominator cannot be an infinite value')

        assert (isinstance(a, NumberType) and ((isinstance(b, NumberType) and b != 0) or b is None)), (a, b)
        if b is None:
            b = 1
        elif b < 0:
            a, b = -a, -b

        while abs(a - round(a)) > SMALL:
            a *= 10
            b *= 10
        a = round(a)

        if isinstance(a, float) or isinstance(b, float):
            a = StdFraction(a)
            b = StdFraction(b)
            self.x = a / b
        else:
            self.x = StdFraction(a, b)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        x = tuple([self.numerator, self.denominator])
        return x[key]

    def __setitem__(self, key, value):
        assert (isinstance(value, NumberType) and (value or key != 1)), value
        x = list([self.numerator, self.denominator])
        x[key] = value
        self.x = StdFraction(*x)

    def __str__(self):
        from barril.basic.format_float import FormatFloat
        return FormatFloat('%g', self.numerator) + '/' + FormatFloat('%g', self.denominator)

    if six.PY2:
        __unicode__ = __str__
        del __str__

    def __repr__(self):
        return repr(self.x)

    def __float__(self):
        return float(self.x)

    def __add__(self, other):
        if isinstance(other, NumberType): other = Fraction(other)
        x = self.x + other.x
        return Fraction(x.numerator, x.denominator)

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        x = -self.x
        return Fraction(x.numerator, x.denominator)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        if classify(other) == -1: return other * self  # hope a list structure can sort itself out
        if isinstance(other, NumberType): other = Fraction(other)
        x = Fraction(self.numerator * other.numerator, self.denominator * other.denominator)
        x.reduce()
        return x

    def __rmul__(self, other):
        if classify(other) == -1: raise ValueError(self, other)
        return self * other

    def __truediv__(self, other):
        if isinstance(other, NumberType): other = Fraction(other)
        return self * other.inv()

    def __rtruediv__(self, other):
        return self.inv() * other

    def __pow__(self, other):
        if abs(other - other) < SMALL:
            if other < 0:
                return Fraction(self.denominator ** -other, self.numerator ** -other)
            else:
                return Fraction(self.numerator ** other, self.denominator ** other)
        else:
            return Fraction(float(self) ** other)

    def __old_cmp__(self, other):
        if other == float('inf'):
            return -1
        if other == float('-inf'):
            return 1

        if isinstance(other, NumberType): other = Fraction(other)
        t = self.numerator * other.denominator - other.numerator * self.denominator
        if t < 0:
            return -1
        if t > 0:
            return 1
        return 0

    def __eq__(self, other):
        return self.__old_cmp__(other) == 0

    if six.PY2:

        def __ne__(self, other):
            return not self == other

    def __lt__(self, other):
        return self.__old_cmp__(other) == -1

    def __abs__(self):
        return Fraction(abs(self.numerator), self.denominator)

    def __mod__(self, other):
        if isinstance(other, NumberType): other = Fraction(other)
        x = self.x % other.x
        return Fraction(x.numerator, x.denominator)

    def reduce(self):
        "Express the fraction in it's lowest form.  Changes the object, no return."
        self.x = StdFraction(self.numerator, self.denominator)

    def inv(self):
        "return 1/self as a fraction"
        x = 1 / self.x
        return Fraction(x.numerator, x.denominator)

    def copy(self):
        "Returns a copy of the fraction"
        return Fraction(self.numerator, self.denominator)

    def get_numerator(self):
        '''
        Returns the numerator of the fraction.

        :rtype: C{float}
        :returns:
            the numerator
        '''
        return self.x.numerator

    def set_numerator(self, numerator):
        '''
        Sets the numerator of the fraction.

        :type numerator: C{float}
        :param numerator:
            the numerator
        '''
        if numerator == float('inf') or numerator == float('-inf'):
            raise ValueError('Numerator cannot be an infinite value')

        if isinstance(numerator, float):
            a = Fraction(numerator)
            b = Fraction(self.denominator)
            self.x = a.x / b.x
        else:
            self.x = StdFraction(numerator, self.denominator)

    numerator = property(get_numerator, set_numerator)

    def get_denominator(self):
        '''
        Returns the denominator of the fraction.

        :rtype: C{float}
        :returns:
            the numerator
        '''
        return self.x.denominator

    def set_denominator(self, denominator):
        '''
        Sets the denominator of the fraction.

        :type denominator: C{float}
        :param denominator:
            the numerator
        '''
        if denominator == float('inf') or denominator == float('-inf'):
            raise ValueError('Denominator cannot be an infinite value')

        if isinstance(denominator, float):
            a = Fraction(self.numerator)
            b = Fraction(denominator)
            self.x = a.x / b.x
        else:
            self.x = StdFraction(self.numerator, denominator)

    denominator = property(get_denominator, set_denominator)


def classify(instance):
    "Decide if instance is a sequence or a number. Returns 1 for number, -1 for sequence"
    if isinstance(instance, NumberType) or isinstance(instance, Fraction): return 1
    if isinstance(instance, SequenceType): return -1
    try:
        iter(instance)
        return -1
    except TypeError:
        return 1
