'''
    Definition for a Fraction object
    Copyright Neil Roques 2002
    Version 1.03
'''
from __future__ import absolute_import, division, unicode_literals

from functools import total_ordering

import six

SMALL = 1e-8

NumberType = (int, float, int)
SequenceType = (tuple, list)


@total_ordering
class Fraction(object):
    "Numerator, denominator"

    def __init__(self, a, b=None):
        assert (type(a) in NumberType and ((type(b) in NumberType and b != 0) or b is None)), (a, b)
        if b is None:
            b = 1
            if a != float('inf') and a != float('-inf'):
                while abs(a - round(a)) > SMALL:
                    a *= 10
                    b *= 10
                a = round(a)
        elif b < 0:
            a, b = -a, -b
        self.x = (a, b)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        return self.x[key]

    def __setitem__(self, key, value):
        assert (type(value) in NumberType and (value or key != 1)), value
        x = list(self.x)
        x[key] = value
        self.x = tuple(x)  # tuple not presently neccessary, but I'm playing it safe

    def __str__(self):
        from barril.basic.format_float import FormatFloat
        return FormatFloat('%g', self[0]) + '/' + FormatFloat('%g', self[1])

    if six.PY2:
        __unicode__ = __str__
        del __str__

    def __repr__(self):
        return 'Fraction(%g,%g)' % self.x

    def __float__(self):
        return float(self[0]) / self[1]

    def __add__(self, other):
        if type(other) in NumberType: other = Fraction(other)
        lcm_res = lcm(self[1], other[1])
        x = Fraction(self[0] * lcm_res / self[1] + other[0] * lcm_res / other[1], lcm_res)
        return x

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return Fraction(self[0] * -1, self[1])

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        if classify(other) == -1: return other * self  # hope a list structure can sort itself out
        if type(other) in NumberType: other = Fraction(other)
        x = Fraction(self[0] * other[0], self[1] * other[1])
        x.reduce()
        return x

    def __rmul__(self, other):
        if classify(other) == -1: raise ValueError(self, other)
        return self * other

    def __truediv__(self, other):
        if type(other) in NumberType: other = Fraction(other)
        return self * other.inv()

    def __rtruediv__(self, other):
        return self.inv() * other

    def __pow__(self, other):
        if abs(other - other) < SMALL:
            if other < 0:
                return Fraction(self[1] ** -other, self[0] ** -other)
            else:
                return Fraction(self[0] ** other, self[1] ** other)
        else:
            return Fraction(float(self) ** other)

    def __old_cmp__(self, other):
        if type(other) in NumberType: other = Fraction(other)
        t = self[0] * other[1] - other[0] * self[1]
        v = qmark(type(t) == int, 0, 0)
        if t < v:
            return -1
        if t > v:
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
        return Fraction(abs(self[0]), self[1])

    def __mod__(self, other):
        sign = qmark(self * other > 0, 1, -1)
        x = self.copy()
        while abs(x) >= abs(other) or x * other < 0: x -= sign * other
        return x

    def reduce(self):
        "Express the fraction in it's lowest form.  Changes the object, no return."
        if self[0] == 0:
            self.x = (0, 1)
        else:
            hcf_res = hcf(self)
            self.x = (self[0] / hcf_res, self[1] / hcf_res)

    def inv(self):
        "return 1/self as a fraction"
        assert self[0], ZeroDivisionError
        return Fraction(self[1], self[0])

    def copy(self):
        "Returns a copy of the fraction"
        return Fraction(self[0], self[1])

    def classify(self):
        "Used by Neil functions to see if it's a number or a sequence"
        return 1  # Number

    def get_numerator(self):
        '''
        Returns the numerator of the fraction.

        :rtype: C{float}
        :returns:
            the numerator
        '''
        return self[0]

    def set_numerator(self, numerator):
        '''
        Sets the numerator of the fraction.

        :type numerator: C{float}
        :param numerator:
            the numerator
        '''
        self[0] = numerator

    numerator = property(get_numerator, set_numerator)

    def get_denominator(self):
        '''
        Returns the denominator of the fraction.

        :rtype: C{float}
        :returns:
            the numerator
        '''
        return self[1]

    def set_denominator(self, denominator):
        '''
        Sets the denominator of the fraction.

        :type denominator: C{float}
        :param denominator:
            the numerator
        '''
        self[1] = denominator

    denominator = property(get_denominator, set_denominator)


def hcf(a, b=None):
    "(a,b)->highest common factor of a and b"
    if b == None: (a, b) = a
    a, b = abs(int(a)), abs(int(b))
    if a < b:
        a, b = b, a
    if a and b:
        while b:
            a, b = b, a % b
        return a
    else: return 1


def lcm(a, b):
    "a,b->Lowest common multiple of a and b"
    return a * b / hcf(a, b)


def classify(object):
    "Decide if object is a sequence or a number. Returns 1 for number, -1 for sequence"
    if type(object) in NumberType: return 1
    if type(object) in SequenceType: return -1
    try:
        return object.classify()
    except AttributeError:
        try:
            iter(object)
            return -1
        except TypeError:
            return 1


def isseq(object):
    "True for sequences"
    return classify(object) == -1


def qmark(expression, iftrue, iffalse):
    "like expression? iftrue:iffalse"
    if expression:
        return iftrue
    else:
        return iffalse
