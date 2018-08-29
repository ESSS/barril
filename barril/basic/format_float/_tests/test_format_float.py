# coding: utf-8
from __future__ import absolute_import, unicode_literals

import locale
import platform
import sys
from decimal import Decimal

import pytest
import six

from coilib50 import unittest
from coilib50.basic.constants import MINUS_INFINITY, NAN, PLUS_INFINITY
from coilib50.basic.format_float import (
    FloatFromString, FormatFloat, PlatformIndependentFormat, ToDecimal)
from coilib50.units import Scalar
from coilib50.unittest_tools.locale_memento import LocaleMemento


#===================================================================================================
# Test
#===================================================================================================
class Test(unittest.TestCase):

    def testFormatFloat(self):
        '''
        0011709: Ao converter a unidade de um scalar cujo valor e "0.0" o XGUI apresenta "-0.0"
        '''
        self.assertEqual(FormatFloat('%g', 0.0), '0')
        self.assertEqual(FormatFloat('%g', -0.0), '0')

        scalar = Scalar('length', 0.0, 'm')
        self.assertEqual(FormatFloat('%g', scalar.GetValue()), '0')

        self.assertEqual(locale.format('%g', scalar.GetValue('ft')), '-0')
        self.assertEqual(FormatFloat('%g', scalar.GetValue('ft')), '0')

        # Large float numbers on integer format.
        large_float_number = 1e+010 * 1.0
        self.assertEquals(FormatFloat('%d', large_float_number), '10000000000')

        # Infinity
        self.assertEqual(FormatFloat('%.3g', PLUS_INFINITY), '+INF')
        self.assertEqual(FormatFloat('%.3g', MINUS_INFINITY), '-INF')
        self.assertEqual(FormatFloat('%.3g', NAN), '-1.#IND')

        # Digit grouping
        self.assertEqual(FormatFloat('%.2f', 1234567, False), '1234567.00')
        self.assertEqual(FormatFloat('%.2f', 1234567, True), '1234567.00')

        # exponential values representation will have only two digits, just like Linux.
        usa_locale_expected_float = '1.23e+06'
        brazilian_locale_expected_float = '1,23e+06'

        memento = LocaleMemento()
        memento.SetUsaLocale()
        try:
            self.assertEqual(FormatFloat('%.2f', 1234567, True, use_locale=False), '1234567.00')
            self.assertEqual(FormatFloat('%.2f', 1234567, True), '1,234,567.00')
            self.assertEqual(FormatFloat('%.3g', 1234567, True), usa_locale_expected_float)
        finally:
            memento.Restore()

        memento.SetBrazilianLocale()
        try:
            self.assertEqual(FormatFloat('%.2f', 1234567, True, use_locale=False), '1234567.00')
            self.assertEqual(FormatFloat('%.2f', 1234567, True), '1.234.567,00')
            self.assertEqual(FormatFloat('%.3g', 1234567, True), brazilian_locale_expected_float)
        finally:
            memento.Restore()

    def testFloatFromString(self):

        self.assertEqual(FloatFromString('1.25'), 1.25)

        with LocaleMemento.AsUsa():
            self.assertEqual(FloatFromString('1.25'), 1.25)

        with LocaleMemento.AsBrazilian():
            self.assertEqual(FloatFromString('1,25'), 1.25)
            self.assertEqual(FloatFromString('1.25', use_locale=False), 1.25)

        # Check using Russian locale.
        # Russian locale settings use a non ascii letter as thousands_sep
        # If a unicode string is used within locale.atof if will fail with
        # decode error.
        with LocaleMemento.AsRussian():
            float_text = locale.format(b'%f' if six.PY2 else '%f', 123456.25, grouping=True)
            if six.PY2:
                float_text = float_text.decode(locale.getpreferredencoding())
            self.assertEqual(FloatFromString(float_text), 123456.25)

            # for some reason, on Windu the string returned from locale.format() is
            # b'123 0456,250000' (that's a space char in there). Seems like a configuration problem in
            # Windu, but decided to not investigate this further because we plan to ditch
            # redhat64 (centos5) soon.
            if sys.platform.startswith('win'):
                cyrillic_sep = '\xa0'
                self.assertEqual(float_text, '123{}456,250000'.format(cyrillic_sep))

        # Infinity
        self.assertEqual(FloatFromString('+INF'), PLUS_INFINITY)
        self.assertEqual(FloatFromString('-INF'), MINUS_INFINITY)
        self.assertAlmostEqual(FloatFromString('-1.#IND'), NAN, may_have_nans=True)

    @pytest.mark.xfail('linux' in sys.platform and 'SUSE' in platform.linux_distribution()[0],
                       reason="For unknown reasons fails with OverflowError: (34, " \
                              "'Numerical result out of range') on CI on SUSE 11")
    def testToDecimal(self):
        self.assertEqual(ToDecimal(2.0 ** -1074), Decimal('4.9406564584124654417656879286822137236505980261433980114452873216E-324'))  # '4.940656458412465441765687929E-324'))

        self.assertEqual(ToDecimal(0.25), Decimal('0.25'))
        self.assertEqual(ToDecimal(0.1), Decimal('0.10000000000000000555111512312578270211815834045410156250'))  # '0.1000000000000000055511151231'))
        self.assertEqual(ToDecimal(0.5), Decimal('0.5'))
        self.assertEqual(ToDecimal(1.0), Decimal('1.0'))
        self.assertEqual(ToDecimal(2.0), Decimal('2.0'))
        self.assertEqual(ToDecimal(4.25), Decimal('4.25'))

        self.assertEqual(ToDecimal(-7147.5355), Decimal('-7147.5354999999999563442543148994445800781250'))
        self.assertEqual(ToDecimal(1.0e23), Decimal('99999999999999991611392'))

        self.assertEqual(
            ToDecimal(1.999999999999999 * 2.0 ** 1023),
            Decimal('1.79769313486231490980915042342911890543162046052306178222333198385E+308')
        )

    def testPlatformIndependentFormat(self):
        value = 2.2204460492503131e-0016
        obtained_text = PlatformIndependentFormat('%.17g', value)
        self.assertEqual(obtained_text, '2.2204460492503131e-16')

        value = 1.4901161193847656e-8
        obtained_text = PlatformIndependentFormat('%.17g', value)
        self.assertEqual(obtained_text, '1.4901161193847656e-08')

        value = 3.25e250
        obtained_text = PlatformIndependentFormat('%.17g', value)
        self.assertEqual(obtained_text, '3.2500000000000002e250')


#===================================================================================================
# main
#===================================================================================================
if __name__ == '__main__':
#    import sys; sys.argv = ['', 'Test.testFormatFloat']
    unittest.main()
