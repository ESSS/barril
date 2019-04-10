class QuantityValidationError(ValueError):
    def __init__(self, message, caption, value, operator, limit_value):
        """
            QuantityValidationError inherits from ValueError
            with helpers attributes (message, caption, value, operator, limit_value)
        :param str message:
            the full formatted message
        :param str caption:
            caption of the category info
        :param float value:
            value validated
        :param str operator:
            operator (literal or not)
        :param float limit_value:
            limit value
        """
        super().__init__(message)
        self.message = message
        self.caption = caption
        self.value = value
        self.operator = operator
        self.limit_value = limit_value
