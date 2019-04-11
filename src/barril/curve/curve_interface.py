
from oop_ext.interface import Interface


class ICurve(Interface):
    """
        The curve is an element that has values and domain for those values.
    """

    def GetImage(self):
        """
        :rtype: IArray
        :returns:
            An IArray -- which is an IObjectWithQuantity with the image for this curve
        """

    def GetDomain(self):
        """
        :rtype: IArray
        :returns:
            An {IArray} -- which is an IObjectWithQuantity with the domain for this curve
        """

    def __getitem__(self, index):
        """
        [] operator, supporting slices.

        :type index: int or slice
        :param index:
            The index of the curve to return

        :rtype: Curve
        :returns:
            Returns a new curve with the pair (domain, image) for the passed slice.
        """
