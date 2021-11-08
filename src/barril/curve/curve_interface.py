from typing import Any
from typing import overload
from typing import Tuple
from typing import Union

from oop_ext.interface import Interface
from oop_ext.interface import TypeCheckingSupport

from barril.units import Array
from barril.units._array import ValuesType

__all__ = ["ICurve"]


class ICurve(Interface, TypeCheckingSupport):
    """
    The curve is an element that has values and domain for those values.
    """

    def GetImage(self) -> Array:
        """
        :returns:
            An IArray -- which is an IObjectWithQuantity with the image for this curve
        """

    def GetDomain(self) -> Array:
        """
        :returns:
            An {IArray} -- which is an IObjectWithQuantity with the domain for this curve
        """

    @overload
    def __getitem__(self, index: int) -> Tuple[float, float]:
        ...

    @overload
    def __getitem__(self, index: slice) -> Tuple[ValuesType, ValuesType]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Any:
        """
        [] operator, supporting slices.

        :param index:
            The index of the curve to return

        :returns:
            Returns the pair (domain, image) for the passed slice.
        """
