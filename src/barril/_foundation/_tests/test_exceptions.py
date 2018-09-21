# coding: UTF-8
from __future__ import unicode_literals

import locale
import sys

import pytest
import six

from barril._foundation.exceptions import ExceptionToUnicode

skip_py3_obsolete_unicode = pytest.mark.skipif(
    condition=not six.PY2, reason='Python 3 turned unicode conversions obsolete')


@skip_py3_obsolete_unicode
def testExceptionToUnicode(exception_message, lpe_exception_message, fse_exception_message):
    assert ExceptionToUnicode(Exception(exception_message)) == exception_message
    assert ExceptionToUnicode(Exception(fse_exception_message)) == exception_message
    assert ExceptionToUnicode(Exception(lpe_exception_message)) == exception_message


@skip_py3_obsolete_unicode
def testExceptionToUnicodeOSError(exception_message, lpe_exception_message, fse_exception_message):
    assert ExceptionToUnicode(OSError(2, exception_message)) == '[Errno 2] ' + exception_message
    assert ExceptionToUnicode(OSError(2, fse_exception_message)) == '[Errno 2] ' + exception_message
    assert ExceptionToUnicode(OSError(2, lpe_exception_message)) == '[Errno 2] ' + exception_message


@skip_py3_obsolete_unicode
def testExceptionToUnicodeIOError(exception_message, lpe_exception_message, fse_exception_message):
    # IOError is really stupid, unicode(IOError('á')) actually raises UnicodeEncodeError
    # (not UnicodeDecodeError!)
    assert ExceptionToUnicode(IOError(exception_message)) == exception_message
    assert ExceptionToUnicode(IOError(fse_exception_message)) == exception_message
    assert ExceptionToUnicode(IOError(lpe_exception_message)) == exception_message


@skip_py3_obsolete_unicode
def testExceptionToUnicodeCustomException(exception_message, lpe_exception_message, fse_exception_message):

    class MyException(Exception):

        def __unicode__(self):
            return 'hardcoded unicode repr'

    assert ExceptionToUnicode(MyException(exception_message)) == 'hardcoded unicode repr'


@skip_py3_obsolete_unicode
def testExceptionToUnicodeBadEncoding(exception_message, lpe_exception_message, fse_exception_message):
    assert ExceptionToUnicode(Exception(b'random \x90\xa1\xa2')) == 'random \ufffd\ufffd\ufffd'


@skip_py3_obsolete_unicode
def testExceptionToUnicodeUTF8():
    assert ExceptionToUnicode(Exception('Ação'.encode('utf-8'))) == 'Ação'


def testExceptionToUnicodeWithReraise():
    first_caption = 'first'
    second_caption = 'second'
    third_caption = 'third'

    def FunctionWithReraise():
        from barril._foundation.reraise import Reraise
        try:
            raise RuntimeError(first_caption)
        except RuntimeError as e:
            try:
                Reraise(e, second_caption)
            except RuntimeError as e2:
                Reraise(e2, third_caption)

    with pytest.raises(RuntimeError) as ex_info:
        FunctionWithReraise()

    exception_message = ExceptionToUnicode(ex_info.value)
    for caption in [first_caption, second_caption, third_caption]:
        assert caption in exception_message


@pytest.mark.skipif(condition=six.PY2, reason='Python 3 exception context')
def testExceptionToUnicodeWithRaiseContext():
    """Ensure ExceptionToUnicode builds a message with all context/causes of an exception"""
    with pytest.raises(RuntimeError) as exc_info:

        def Original():
            raise RuntimeError('Original Error')

        try:
            Original()
        except RuntimeError:
            raise RuntimeError('While handling error')

    assert ExceptionToUnicode(exc_info.value) == 'While handling error\nOriginal Error'


#===================================================================================================
# Fixtures
#===================================================================================================
@pytest.fixture
def exception_message():
    exception_message = 'кодирование'
    # Use another message if this machine's locale does not support cyrilic
    try:
        exception_message.encode(locale.getpreferredencoding())
    except UnicodeEncodeError:
        exception_message = 'látïn-1'

    return exception_message


@pytest.fixture
def lpe_exception_message(exception_message):
    return exception_message.encode(locale.getpreferredencoding())


@pytest.fixture
def fse_exception_message(exception_message):
    return exception_message.encode(sys.getfilesystemencoding())
