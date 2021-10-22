from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from barril.units import Quantity

# constants for unknown quantities
UNKNOWN_QUANTITY_TYPE = "Unknown"
UNKNOWN_UNIT = "<unknown>"

LENGTH_QUANTITY_TYPE = "length"


def CreateUnknwonwReadOnlyQuantity() -> "Quantity":
    """
    :returns:
        Returns a read only quantity for an unknown quantity.
    """
    from ._quantity import ObtainQuantity

    return ObtainQuantity(UNKNOWN_UNIT, UNKNOWN_QUANTITY_TYPE)
