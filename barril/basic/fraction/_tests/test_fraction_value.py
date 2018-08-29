from __future__ import absolute_import, division, unicode_literals

import copy

import six

from coilib50 import unittest
from coilib50.basic.fraction import Fraction, FractionValue
from coilib50.unittest_tools.locale_memento import LocaleMemento


#===================================================================================================
# Test
#===================================================================================================
class Test(unittest.TestCase):

    def testBasicUsage(self):
        f = FractionValue(3, Fraction(5, 3))
        self.assertEqual(f.number, 3)
        self.assertEqual(f.fraction, Fraction(5, 3))

        f.number = 5.5
        f.fraction = Fraction(6, 5)
        self.assertEqual(f.number, 5.5)
        self.assertEqual(f.fraction, Fraction(6, 5))

        self.assertRaises(TypeError, f.SetNumber, 'hello')
        self.assertRaises(TypeError, f.SetFraction, 'hello')
        self.assertRaises(ValueError, f.SetFraction, (1, 2, 3))

        self.assertEqual(FractionValue(3).fraction, Fraction(0, 1))

    def testDefault(self):
        f = FractionValue()
        self.assertEqual(f.number, 0.0)
        self.assertEqual(f.fraction, Fraction(0, 1))

    def testPartsArentNone(self):
        '''
        FractionValue can't be initialized nor modified to have None as number or fraction part.
        '''
        self.assertRaises(TypeError, FractionValue, 1, None)
        self.assertRaises(TypeError, FractionValue, None, (0 / 1))
        self.assertRaises(TypeError, FractionValue, None, None)

        f = FractionValue(1, Fraction(0, 1))
        self.assertRaises(TypeError, f.SetNumber, None)
        self.assertRaises(TypeError, f.SetFraction, None)

    def testMatchFractionPart(self):
        # Text Ok, should not raise error
        FractionValue.MatchFractionPart('3/4')
        self.assertRaises(ValueError, FractionValue.MatchFractionPart, '2 3/4')

    def testStr(self):
        f = FractionValue(3, Fraction(5, 3))
        self.assertEqual(six.text_type(f), '3 5/3')
        self.assertEqual(repr(f), 'FractionValue(3, 5/3)')

        f = FractionValue(3)
        self.assertEqual(six.text_type(f), '3')
        self.assertEqual(repr(f), 'FractionValue(3, 0/1)')

    def testLocalizedString(self):
        with LocaleMemento.AsBrazilian():
            f = FractionValue(4.2, Fraction(1.1, 2))
            self.assertEqual(f.GetLocalizedString(), '4,2 1,1/2')
            self.assertEqual(f.GetLocalizedFraction(), '1,1/2')

    def testEquality(self):
        self.assertTrue(FractionValue(3, Fraction(5, 3)) == FractionValue(3, Fraction(5, 3)))
        self.assertTrue(not FractionValue(3, Fraction(5, 3)) != FractionValue(3, Fraction(5, 3)))

        self.assertTrue(FractionValue(3) == FractionValue(3))
        self.assertTrue(not FractionValue(3) != FractionValue(3))

        self.assertTrue(FractionValue(10, Fraction(5, 3)) != FractionValue(3, Fraction(5, 3)))
        self.assertTrue(not FractionValue(10, Fraction(5, 3)) == FractionValue(3, Fraction(5, 3)))

        self.assertEqual(FractionValue(10, (5, 3)), FractionValue(10, Fraction(5, 3)))

    def testFloat(self):
        self.assertEqual(float(FractionValue(3, Fraction(5, 3))), 3 + 5 / 3.0)
        self.assertEqual(float(FractionValue(3)), 3.0)

    def testCopy(self):
        f = FractionValue(3, (5, 3))
        cf = copy.copy(f)
        self.assertTrue(f == cf)
        self.assertIsNotSame(f, cf)

        cf.fraction.numerator = 10
        cf.fraction.denominator = 4
        self.assertEqual(f, FractionValue(3, (5, 3)))

    def testComparison(self):
        self.assertTrue(FractionValue(3) < FractionValue(3, (3, 4)))
        self.assertTrue(FractionValue(3) <= FractionValue(3, (3, 4)))
        self.assertTrue(FractionValue(3, (3, 4)) > FractionValue(3))
        self.assertTrue(FractionValue(3, (3, 4)) >= FractionValue(3))

    def testCreateFromString(self):
        '''
        0014254: [SubjectTable] Allow the user enter only the fraction value
        '''

        def AssertCreateFromString(text, whole, fraction=None):
            self.assertEqual(
                FractionValue.CreateFromString(text),
                FractionValue(whole, fraction) if fraction is not None else FractionValue(whole),
            )

        AssertCreateFromString('1 1/2', 1, (1, 2))
        AssertCreateFromString('1', 1)
        AssertCreateFromString('1.2 1.1/3', 1.2, (1.1, 3))
        AssertCreateFromString('1.2', 1.2)
        AssertCreateFromString('1/3', 0, (1, 3))
        AssertCreateFromString('3.3/4', 0, (3.3, 4))

        AssertCreateFromString('33/4', 0, (33, 4))
        AssertCreateFromString('  35/4', 0, (35, 4))
        AssertCreateFromString('3 36/4', 3, (36, 4))

        # creating a string with a diferent locale
        locale_memento = LocaleMemento()
        locale_memento.SetBrazilianLocale()
        try:
            AssertCreateFromString('1,2 1,1/3', 1.2, (1.1, 3))
            AssertCreateFromString('1,2', 1.2)
            AssertCreateFromString('1,2/3', 0, (1.2, 3))
        finally:
            locale_memento.Restore()


#===================================================================================================
# main
#===================================================================================================
if __name__ == '__main__':
    unittest.main()
