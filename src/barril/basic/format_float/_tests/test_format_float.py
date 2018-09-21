# coding: utf-8
from __future__ import absolute_import, unicode_literals

import locale

from barril.basic.format_float import FormatFloat, MINUS_INFINITY, NAN, PLUS_INFINITY
from barril.units import Scalar


def testFormatFloat():
    '''
    Convert unit of scalar where value is "0.0".
    '''
    assert FormatFloat('%g', 0.0) == '0'
    assert FormatFloat('%g', -0.0) == '0'

    scalar = Scalar('length', 0.0, 'm')
    assert FormatFloat('%g', scalar.GetValue()) == '0'

    assert locale.format_string('%g', scalar.GetValue('ft')) == '-0'
    assert FormatFloat('%g', scalar.GetValue('ft')) == '0'

    # Large float numbers on integer format.
    large_float_number = 1e+010 * 1.0
    assert FormatFloat('%d', large_float_number) == '10000000000'

    # Infinity
    assert FormatFloat('%.3g', PLUS_INFINITY) == '+INF'
    assert FormatFloat('%.3g', MINUS_INFINITY) == '-INF'
    assert FormatFloat('%.3g', NAN) == '-1.#IND'

    # Digit grouping
    assert FormatFloat('%.2f', 1234567, False) == '1234567.00'
    assert FormatFloat('%.2f', 1234567, True) == '1234567.00'

