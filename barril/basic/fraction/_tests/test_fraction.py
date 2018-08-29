from __future__ import absolute_import, division, unicode_literals

import copy

import six

from coilib50 import unittest
from coilib50.basic.fraction import Fraction
from coilib50.unittest_tools.locale_memento import LocaleMemento


#===================================================================================================
# Test
#===================================================================================================
class Test(unittest.TestCase):

    def testBasicUsage(self):
        f = Fraction(5, 3)
        self.assertEqual(tuple(f), (5, 3))
        self.assertEqual(len(f), 2)
        self.assertEqual(f[0], 5)
        self.assertEqual(f[1], 3)
        self.assertEqual(f.numerator, 5)
        self.assertEqual(f.denominator, 3)
        f.numerator = 10
        f.denominator = 4
        self.assertEqual(tuple(f), (10, 4))

    def testStr(self):
        self.assertEqual(six.text_type(Fraction(5, 3)), '5/3')
        self.assertEqual(repr(Fraction(5, 3)), 'Fraction(5,3)')

        self.assertEqual(six.text_type(Fraction(3 / 1000.0, 4)), '0.003/4')

    def testReduce(self):
        f = Fraction(5, 3)
        f[0] = 15
        self.assertEqual(tuple(f), (15, 3))
        f.reduce()
        self.assertEqual(tuple(f), (5, 1))

    def testOperations(self):
        # float operator
        self.assertEqual(float(Fraction(5, 3)), 5.0 / 3.0)

        # sum
        self.assertEqual(Fraction(5, 3) + Fraction(2, 3), Fraction(7, 3))
        self.assertEqual(Fraction(5, 3) + 5.0, Fraction(20, 3))
        self.assertEqual(5.0 + Fraction(5, 3), Fraction(20, 3))

        # sub
        self.assertEqual(Fraction(5, 3) - Fraction(2, 3), Fraction(3, 3))
        self.assertEqual(Fraction(5, 3) - 1.0, Fraction(2, 3))
        self.assertEqual(1.0 - Fraction(5, 3), Fraction(-2, 3))

        # mul
        self.assertEqual(Fraction(5, 3) * Fraction(4, 3), Fraction(20, 9))
        self.assertEqual(3 * Fraction(5, 3), Fraction(15, 3))
        self.assertEqual(Fraction(5, 3) * 3, Fraction(15, 3))

        # div
        self.assertEqual(Fraction(5, 3) / Fraction(5, 3), Fraction(15, 15))
        self.assertEqual(Fraction(5, 3) / 3, Fraction(5, 9))
        self.assertEqual(3 / Fraction(5, 3), Fraction(9, 5))

        # inv
        self.assertEqual(Fraction(5, 3).inv(), Fraction(3, 5))

        # neg
        self.assertEqual(-Fraction(5, 3), Fraction(-5, 3))

    def testCopy(self):
        f = Fraction(5, 3)
        cf = copy.copy(f)
        self.assertTrue(f == cf)
        self.assertTrue(not f != cf)
        self.assertIsNotSame(f, cf)

        self.assertTrue(f != Fraction(3, 5))
        self.assertTrue(not f == Fraction(3, 5))

    def testStrFormat(self):
        '''
        0013266: Scalar field behavior
        In this test we make sure that the Fraction.__str__ method calls FormatFloat, which handles
        the locale properly.
        '''
        import coilib50.basic.format_float

        # By default, the numbers are formatted using "%g"
        f = Fraction(5, 3)
        self.assertTrue(six.text_type(f), '5/3')

        # Test the use of FormatFloat
        f = Fraction(5.6, 3)
        self.assertEqual(six.text_type(f), '5.6/3')

        original_format_float = coilib50.basic.format_float.FormatFloat
        coilib50.basic.format_float.FormatFloat = lambda x, y: 'X%.2fX' % y
        try:
            self.assertEqual(six.text_type(f), 'X5.60X/X3.00X')
        finally:
            coilib50.basic.format_float.FormatFloat = original_format_float

        self.assertEqual(six.text_type(f), '5.6/3')

        locale_memento = LocaleMemento()
        locale_memento.SetBrazilianLocale()
        try:
            f = Fraction(5.6, 3)
            self.assertEqual(six.text_type(f), '5,6/3')
        finally:
            locale_memento.Restore()


#===================================================================================================
# main
#===================================================================================================
if __name__ == '__main__':
#    import sys
#    sys.argv = ['','Test.testStrFormat']
    unittest.main()
