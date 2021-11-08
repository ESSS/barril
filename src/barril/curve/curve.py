from typing import Any
from typing import overload
from typing import Tuple
from typing import Union

from oop_ext.foundation.decorators import Deprecated
from oop_ext.interface import AssertImplements
from oop_ext.interface import ImplementsInterface

from barril.curve.curve_interface import ICurve
from barril.units.interfaces import IArray
from barril.units.interfaces import ValuesType

__all__ = ["Curve"]


@ImplementsInterface(ICurve)
class Curve:
    """
    The curve is an element that has a domain "x" and an image "f(x)".

    Domain: The domain of a given function is the set of 'input' values for which the function is
    defined -- from Wikipedia

    Image: it is defined as 'image set' the set of values which effectively f(x) takes -- from
    Wikipedia (pt)

    :ivar _image:
        The array with the image for this curve

    :ivar _domain:
        The array with the domain for this curve
    """

    def __init__(self, image: IArray, domain: IArray) -> None:
        """
        :param image:
            This is the image of this curve

        :param domain:
            This is the domain of this curve
        """
        AssertImplements(image, IArray)
        AssertImplements(domain, IArray)

        self._CheckImageAndDomainLength(image, domain)
        self._image = image
        self._domain = domain

    def _CheckImageAndDomainLength(self, image: IArray, domain: IArray) -> None:
        """
        Check if image and domain have different lengths, if is True raises ValueError.

        :param image:
            This is the image of this curve

        :param domain:
            This is the domain of this curve

        :raises ValueError:
            if image and domain have different lengths
        """
        image_length = len(image.GetValues())
        domain_length = len(domain.GetValues())
        if image_length != domain_length:
            msg = (
                "The length of the image ({}) is different from the size of the domain ({})".format(
                    image_length, domain_length
                )
            )
            raise ValueError(msg)

    def GetDomain(self) -> IArray:
        return self._domain

    def SetDomain(self, domain: IArray) -> None:
        """
        Define the curve domain.

        :param domain:
            the domain of this curve
        """
        self._CheckImageAndDomainLength(self._image, domain)
        self._domain = domain

    domain = property(GetDomain, SetDomain)

    def GetLength(self) -> int:
        """
        :returns:
            The length of the curve
        """
        return len(self._image.GetValues())

    def GetImage(self) -> IArray:
        return self._image

    def SetImage(self, image: IArray) -> None:
        """
        Define the curve image.

        :param IArray image:
            The image of this curve
        """
        self._CheckImageAndDomainLength(image, self._domain)
        self._image = image

    image = property(GetImage, SetImage)

    @Deprecated("SetImage")
    def SetValues(self, values: IArray) -> None:
        return self.SetImage(values)

    @Deprecated("GetImage")
    def GetValues(self) -> IArray:
        """
        @see ICurve.GetImage.
        """
        return self.GetImage()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Curve):
            return False
        return self.GetImage() == other.GetImage() and self.GetDomain() == other.GetDomain()

    @overload
    def __getitem__(self, index: int) -> Tuple[float, float]:
        ...

    @overload
    def __getitem__(self, index: slice) -> Tuple[ValuesType, ValuesType]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Tuple[Any, Any]:
        d = self.GetDomain().GetValues()[index]  # type:ignore[index]
        i = self.GetImage().GetValues()[index]  # type:ignore[index]
        return d, i

    def __repr__(self) -> str:
        image = self.GetImage()
        domain = self.GetDomain()

        xy = []
        for i, (x, y) in enumerate(zip(image, domain)):  # type:ignore[call-overload]
            if i > 20:
                xy.append(" ... ")
                break
            xy.append(f"({x}, {y})")

        return "Curve({}, {})[{}]".format(
            image.unit, domain.unit, " ".join(xy)  # type:ignore[attr-defined]
        )
