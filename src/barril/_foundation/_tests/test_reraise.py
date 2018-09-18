# coding=utf-8
from __future__ import unicode_literals

import traceback

import pytest
import six

from barril._foundation.exceptions import ExceptionToUnicode
from barril._foundation.reraise import Reraise

pytestmark = pytest.mark.skipif(
    condition=not six.PY2,
    reason="On Python 3, Reraise is just a redirection to Python's raise...from statement",
)


#===================================================================================================
# ExecutePythonCode
#===================================================================================================
def ExecutePythonCode(code):
    exec(compile(code, '<string>', 'exec'))


#===================================================================================================
# ExceptionTestConfiguration
#===================================================================================================
class ExceptionTestConfiguration():

    def __init__(self, exception_type, string_statement, expected_inner_exception_message='', expected_traceback_message=None):
        self.exception_type = exception_type
        self.string_statement = string_statement
        self.expected_inner_exception_message = expected_inner_exception_message
        self.expected_traceback_message = expected_traceback_message

    def RaiseExceptionUsingReraise(self):

        def RaiseException():
            ExecutePythonCode(self.string_statement)
            pytest.fail('Should not reach here')

        def ReraiseException():
            try:
                RaiseException()
            except self.exception_type as exception:
                Reraise(exception, "While doing 'bar'")

        try:
            try:
                ReraiseException()
            except self.exception_type as e1:
                Reraise(e1, "While doing x:")
        except self.exception_type as e2:
            Reraise(e2, "While doing y:")

    def GetExpectedExceptionMessage(self):
        return "\nWhile doing y:\nWhile doing x:\nWhile doing 'bar'\n" + self.expected_inner_exception_message

    def GetExpectedTracebackMessage(self, actual_exception, use_utf_8_encoding=True):
        # Getting the type of the "actual exception" because its type might be different than self.exception_type
        reraised_exception_name = type(actual_exception).__name__
        exception_message = self.GetExpectedExceptionMessage()

        if self.expected_traceback_message is not None:
            exception_message = self.expected_traceback_message
        else:
            exception_message = reraised_exception_name + ": " + exception_message + "\n"

        # HACK [muenz]: the 'traceback' module does this, so in order to be able to compare strings we need this workaround
        # notice that if the exception "leaks" the Python console handles the unicode symbols properly
        if use_utf_8_encoding:
            exception_message = exception_message.encode('utf-8')
        else:
            exception_message = traceback._some_str(exception_message)
        assert isinstance(exception_message, bytes)

        return exception_message


parametrized_exceptions = pytest.mark.parametrize('exception_configuration', [
    ExceptionTestConfiguration(ValueError, "raise ValueError('message')", 'message'),
    ExceptionTestConfiguration(KeyError, "raise KeyError('message')", "u'message'"),
    ExceptionTestConfiguration(OSError, "raise OSError(2, 'message')", '[Errno 2] message'),
    ExceptionTestConfiguration(IOError, "raise IOError('message')", 'message'),
    ExceptionTestConfiguration(
        SyntaxError,
        "in valid syntax",
        expected_inner_exception_message='invalid syntax (<string>, line 1)',
        expected_traceback_message=('  File "<string>", line 1\n'
                                    '    in valid syntax\n'
                                    '     ^\n'
                                    'ReraisedSyntaxError: invalid syntax\n'
                                    )
    ),
    ExceptionTestConfiguration(UnicodeDecodeError, "u'£'.encode('utf-8').decode('ascii')", "'ascii' codec can't decode byte 0xc2 in position 0: ordinal not in range(128)"),
    ExceptionTestConfiguration(UnicodeEncodeError, "u'£'.encode('ascii')", "'ascii' codec can't encode character u'\\xa3' in position 0: ordinal not in range(128)"),
    ExceptionTestConfiguration(AttributeError, "raise AttributeError('message')", 'message'),

    ExceptionTestConfiguration(OSError, "raise OSError()"),
    ExceptionTestConfiguration(OSError, "raise OSError(1)", '1'),
    ExceptionTestConfiguration(OSError, "raise OSError(2, '£ message')", '[Errno 2] £ message'),
    ExceptionTestConfiguration(IOError, "raise IOError('исключение')", "исключение", expected_traceback_message='IOError: <unprintable IOError object>\n'),
    ExceptionTestConfiguration(OSError, "import locale; raise OSError(2, '£ message'.encode(locale.getpreferredencoding()))", '[Errno 2] £ message'),
    ExceptionTestConfiguration(OSError, "raise OSError(2, b'£ message')", '[Errno 2] £ message'),
    ExceptionTestConfiguration(IOError, "raise IOError(b'£ message')", '£ message', expected_traceback_message='IOError: <unprintable IOError object>\n'),
    ExceptionTestConfiguration(Exception, "raise Exception(b'£ message')", '£ message'),
]
, ids=[
    'ValueError',
    'KeyError',
    'OSError',
    'IOError',
    'SyntaxError',
    'UnicodeDecodeError',
    'UnicodeEncodeError',
    'AttributeError',

    'OSError - empty',
    'OSError - ErrorNo, empty message',
    'OSError - ErrorNo, unicode message',
    'IOError - unicode message',

    'OSError - bytes message in UTF-8',
    'OSError - bytes message in locale.getpreferredencoding()',
    'IOError - bytes message',
    'Exception - bytes message',
])


@parametrized_exceptions
def testReraiseKeepsTraceback(exception_configuration):
    with pytest.raises(exception_configuration.exception_type) as e:
        exception_configuration.RaiseExceptionUsingReraise()

    # Reraise() should not appear in the traceback
    traceback_filenames = []
    for traceback_entry in e.traceback:
        try:
            traceback_filenames.append(traceback_entry.path.basename)
        except AttributeError:
            # traceback_entry.path will be a string when the code was run using "exec compile('code')".
            # However this does not hold true if 'code' contains a SyntaxError, which in that case 'traceback_entry.path'
            # will be a LocalPath
            traceback_filenames.append(traceback_entry.path)

    crash_entry = e.traceback.getcrashentry()
    if isinstance(crash_entry.path, six.string_types):
        assert traceback_filenames[0] == b'test_reraise.py'
        assert traceback_filenames[-1] == b'<string>'
    else:
        assert traceback_filenames[0] == b'test_reraise.py'
        assert traceback_filenames[-1] == b'test_reraise.py'


@parametrized_exceptions
def testReraiseAddsMessagesCorrectly(exception_configuration):
    with pytest.raises(exception_configuration.exception_type) as e:
        exception_configuration.RaiseExceptionUsingReraise()

    assert isinstance(e.value, exception_configuration.exception_type)
    assert ExceptionToUnicode(e.value) == exception_configuration.GetExpectedExceptionMessage()

    traceback_message = traceback.format_exception_only(type(e.value), e.value)
    traceback_message = b''.join(traceback_message)

    if traceback_message != exception_configuration.GetExpectedTracebackMessage(e.value, True):
        assert traceback_message == exception_configuration.GetExpectedTracebackMessage(e.value, False)


@parametrized_exceptions
def testPickle(exception_configuration):
    try:
        exception_configuration.RaiseExceptionUsingReraise()
    except exception_configuration.exception_type as reraised_exception:
        import cPickle
        dumped_exception = cPickle.dumps(reraised_exception)
        pickled_exception = cPickle.loads(dumped_exception)
        assert ExceptionToUnicode(pickled_exception) == ExceptionToUnicode(reraised_exception)
        assert ExceptionToUnicode(pickled_exception) != ''
        assert ExceptionToUnicode(reraised_exception) != ''
