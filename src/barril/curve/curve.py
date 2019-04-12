from barril.curve.curve_interface import ICurve
from barril.units.interfaces import IArray
from oop_ext.interface._interface import ImplementsInterface, AssertImplements
from oop_ext.foundation.decorators import Implements, Deprecated

__all__ = ["Curve"]  # pylint: disable=invalid-all-object


@ImplementsInterface(ICurve)
class Curve:
    """
    The curve is an element that has a domain "x" and an image "f(x)".

    Domain: The domain of a given function is the set of 'input' values for which the function is
    defined -- from Wikipedia

    Image: it is defined as 'image set' the set of values which effectively f(x) takes -- from
    Wikipedia (pt)

    :ivar IArray _image:
        The array with the image for this curve

    :ivar IArray _domain:
        The array with the domain for this curve
    """

    def __init__(self, image, domain):
        """
        :param IArray image:
            This is the image of this curve

        :param IArray domain:
            This is the domain of this curve
        """
        AssertImplements(image, IArray)
        AssertImplements(domain, IArray)

        self._CheckImageAndDomainLength(image, domain)
        self._image = image
        self._domain = domain

    def _CheckImageAndDomainLength(self, image, domain):
        """
        Check if image and domain have different lengths, if is True raises ValueError.

        :param IArray image:
            This is the image of this curve

        :param IArray domain:
            This is the domain of this curve

        :raises ValueError:
            if image and domain have different lengths
        """
        image_length = len(image.GetValues())
        domain_length = len(domain.GetValues())
        if image_length != domain_length:
            msg = "The length of the image ({}) is different from the size of the domain ({})".format(
                image_length, domain_length
            )
            raise ValueError(msg)

    def GetDomain(self):
        return self._domain

    def SetDomain(self, domain):
        """
            Define the curve domain.

            :type domain: L{Array}
            :param domain:
                the domain of this curve
        """
        self._CheckImageAndDomainLength(self._image, domain)
        self._domain = domain

    domain = property(GetDomain, SetDomain)

    def GetLength(self):
        """
        :rtype: int
        :returns:
            The lenght of the curve
        """
        return len(self._image.GetValues())

    def GetImage(self):
        return self._image

    def SetImage(self, image):
        """
        Define the curve image.

        :param IArray image:
            The image of this curve
        """
        self._CheckImageAndDomainLength(image, self._domain)
        self._image = image

    image = property(GetImage, SetImage)

    @Deprecated("SetImage")
    def SetValues(self, values):
        return self.SetImage(values)

    @Deprecated("GetImage")
    def GetValues(self):
        """
        @see ICurve.GetImage.
        """
        return self.GetImage()

    def __eq__(self, other):
        if not isinstance(other, Curve):
            return False
        return (
            self.GetImage() == other.GetImage()
            and self.GetDomain() == other.GetDomain()
        )

    def __ne__(self, other):
        return not self == other

    @Implements(ICurve.__getitem__)
    def __getitem__(self, index):
        return self.GetDomain().values[index], self.GetImage().values[index]

    def __repr__(self, *args, **kwargs):
        image = self.GetImage()
        domain = self.GetDomain()

        xy = []
        for i, (x, y) in enumerate(zip(image, domain)):
            if i > 20:
                xy.append(" ... ")
                break
            xy.append(f"({x}, {y})")

        return "Curve({}, {})[{}]".format(image.unit, domain.unit, " ".join(xy))
