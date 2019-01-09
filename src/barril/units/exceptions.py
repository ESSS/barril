

class QuantityValidationError(ValueError):
    def __init__(self, message, caption, value, operator, limit_value):
        """
            QuantityValidationError inherits from ValueError
            with helpers attributes (message, caption, value, operator, limit_value)
        :param message:
            the full formatted message
        :param caption:
            caption of the category info
        :param value:
            value validated
        :param operator:
            operator (literal or not)
        :param limit_value:
            limit value
        """
        super(QuantityValidationError, self).__init__(message)
        self.message = message
        self.caption = caption
        self.value = value
        self.operator = operator
        self.limit_value = limit_value
