from __future__ import unicode_literals

import locale

import six

#===================================================================================================
# ExceptionToUnicode
#===================================================================================================
if six.PY2:

    def ExceptionToUnicode(exception):
        '''
        Obtains unicode representation of an Exception.

        This wrapper is used to circumvent Python 2.7 problems with built-in exceptions with unicode
        messages.

        Steps used:
            * Try to obtain Exception.__unicode__
            * If the exception message is a unicode, returns it.
            * Try to obtain Exception.__str__ and decode with utf-8
            * Try to obtain Exception.__str__ and decode with locale.getpreferredencoding
            * If all fails, return Exception.__str__ and decode with (ascii, errors='replace')

        :param Exception exception:

        :return six.text_type:
            Unicode representation of an Exception.
        '''

        try:
            # First, try to obtain __unicode__ as defined by the Exception
            return six.text_type(exception)
        except UnicodeError:
            pass

        # When message is a unicode, just return it
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            # exception.message deprecated since Python 2.6
            exception_message = getattr(exception, 'message', None)
        if isinstance(exception_message, unicode):
            return exception_message

        bytes_msg = six.binary_type(exception)
        try:
            # If that fails, try decoding with utf-8 which is the strictest and will complain loudly.
            return bytes_msg.decode('utf-8')
        except UnicodeError:
            pass
        try:
            # If that fails, try decoding with locale
            return bytes_msg.decode(locale.getpreferredencoding())
        except UnicodeError:
            pass

        # If all failed, give up and decode with ascii replacing errors.
        return bytes_msg.decode(errors='replace')

else:

    def ExceptionToUnicode(exception):
        """
        Python 3 exception handling already deals with string and six.binary_type (and mixed) error messages. Here we
        will only append the original exception message to the returned message (this is automatically done in Python 2
        since the original exception message is added into the new exception while Python 3 keeps the original exception
        as a separated attribute
        """
        messages = []
        while exception:
            messages.append(str(exception))
            exception = exception.__cause__ or exception.__context__
        return '\n'.join(messages)
