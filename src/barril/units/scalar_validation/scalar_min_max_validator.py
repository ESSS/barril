from typing import Optional

from barril.units import ObtainQuantity
from barril.units import Scalar


class ScalarMinMaxValidator:
    """
    Simple helper class to create default checkers.

    It implements methods to create simple messages of scalar value limits checking
    """

    @classmethod
    def CreateScalarCheckWarningMsg(cls, scalar: Scalar, name: str) -> Optional[str]:
        """
        :param Scalar scalar:
            The scalar to be checked against its limits
        :param str name:
            The scalar property name

        :returns str:
            The built warning message saying if the scalar is less or greater than its limits
        """
        predicate = cls._ScalarCheckMsgPredicate(scalar)

        if predicate is not None:
            return f"Warning in {name}. {predicate}"

        return None

    @classmethod
    def CreateScalarCheckErrorMsg(cls, scalar: Scalar, name: str) -> Optional[str]:
        """
         :param scalar:
            The scalar to be checked against its limits

        :param name:
            The scalar property name

        :returns str:
            The built error message saying if the scalar is less or greater than its limits
        """
        predicate = cls._ScalarCheckMsgPredicate(scalar)

        if predicate is not None:
            return f"Error in {name}. {predicate}"

        return None

    @classmethod
    def _ScalarCheckMsgPredicate(cls, scalar: Scalar) -> Optional[str]:
        """
        :param Scalar scalar:
            The scalar to be checked against its limits

        :returns str:
            The built message saying if the scalar is less or greater than its limits
        """
        try:
            quantity = ObtainQuantity(scalar.GetUnit(), scalar.GetCategory())
            quantity.CheckValue(scalar.GetValue(), use_literals=True)

        except ValueError as error:
            return str(error)

        return None
