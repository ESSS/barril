class QuantityValidationError(ValueError):
    def __init__(
        self, message: str, caption: str, value: float, operator: str, limit_value: float
    ) -> None:
        """
        Value error subclass with helpers attributes.

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
        super().__init__(message)
        self.message = message
        self.caption = caption
        self.value = value
        self.operator = operator
        self.limit_value = limit_value
