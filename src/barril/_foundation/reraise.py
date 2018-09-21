from __future__ import unicode_literals

import six
from six import raise_from

# Inspired by http://www.thescripts.com/forum/thread46361.html

if six.PY2:
    
    #===============================================================================================
    # Reraise
    #===============================================================================================
    def Reraise(exception, message, separator='\n'):
        '''
        Raised the same exception given, with an additional message.

        :param Exception exception:
            Original exception being raised with additional messages

        :param str message:
            Message to be added to the given exception

        :param str separator:
            String separating `message` from the `exception`'s original message.

        e.g.
            try:
                raise RuntimeError('original message')
            except Exception, e:
                Reraise(e, 'message')

            >>> RuntimeError:
            >>> message
            >>> original message

            try:
                raise RuntimeError('original message')
            except Exception, e:
                Reraise(e, '[message]', separator=' ')

            >>> RuntimeError:
            >>> [message] original message
        '''
        from barril._foundation.exceptions import ExceptionToUnicode

        # IMPORTANT: Do NOT use try/except mechanisms in this method or the sys.exc_info()[-1] will be invalid
        if hasattr(exception, 'reraised_message'):
            current_message = exception.reraised_message
        else:
            current_message = ExceptionToUnicode(exception)

        # Build the new message
        if not current_message.startswith(separator):
            current_message = separator + current_message
        message = '\n' + message + current_message

        if exception.__class__ in _SPECIAL_EXCEPTION_MAP:
            # Handling for special case, some exceptions have different behaviors.
            exception = _SPECIAL_EXCEPTION_MAP[exception.__class__](*exception.args)

        elif exception.__class__ not in _SPECIAL_EXCEPTION_MAP.values():
            # In Python 2.5 overriding the exception "__str__" has no effect in "unicode()". Instead, we
            # must change the "args" attribute which is used to build the string representation.
            # Even though the documentation says "args" will be deprecated, it uses its first argument
            # in unicode() implementation and not "message".
            exception.args = (message,)

        exception.message = message
        # keep the already decoded message in the object in case this exception is reraised again
        exception.reraised_message = message

        # taken from source code of future.utils.raise_with_traceback
        import sys
        exec('raise exception, None, sys.exc_info()[-1]')

    #===================================================================================================
    # SPECIAL_EXCEPTIONS
    #===================================================================================================
    class ReraisedKeyError(KeyError):

        def __init__(self, *args):
            KeyError.__init__(self, *args)
            self.message = None

        def __str__(self):
            return self.message

    class ReraisedOSError(OSError):

        def __init__(self, *args):
            OSError.__init__(self, *args)
            self.message = None

        def __str__(self):
            return self.message

    class ReraisedSyntaxError(SyntaxError):

        def __init__(self, *args):
            SyntaxError.__init__(self, *args)
            self.message = None

        def __str__(self):
            return self.message

    class ReraisedUnicodeDecodeError(UnicodeDecodeError):

        def __init__(self, *args):
            UnicodeDecodeError.__init__(self, *args)
            self.message = None

        def __str__(self):
            return self.message

    class ReraisedUnicodeEncodeError(UnicodeEncodeError):

        def __init__(self, *args):
            UnicodeEncodeError.__init__(self, *args)
            self.message = None

        def __str__(self):
            return self.message

    _SPECIAL_EXCEPTION_MAP = {
        KeyError : ReraisedKeyError,
        OSError : ReraisedOSError,
        SyntaxError : ReraisedSyntaxError,
        UnicodeDecodeError : ReraisedUnicodeDecodeError,
        UnicodeEncodeError : ReraisedUnicodeEncodeError,
    }
    # [[[end]]] (checksum: 87ea5d69d51083d7009b216f50cc2be5)
else:

    def Reraise(exception, message, separator='\n'):
        """
        Forwards to a `raise exc from cause` statement. Kept alive for backwards compatibility
        (`separator` argument only kept for this reason).
        """
        # Important: Don't create a local variable for the new exception otherwise we'll get a
        # cyclic reference between the exception and its traceback, meaning the traceback will
        # keep all frames (and their contents) alive.
        raise_from(type(exception)(message), exception)
