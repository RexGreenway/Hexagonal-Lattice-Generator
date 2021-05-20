"""
**********
Class Factorys
**********

"""

## IMPORTS
from polylatlib.classes.regular import *
from polylatlib.classes.nonregular import *

__all__ = [
    "Build_Regular",
    "Build_NonRegular"
]

# REGULAR POLYGON FACTORY
class Build_Regular():
    """
    Returns a corresponding regular polygon class object.  

    Parameters
    ----------
    sides : int
        Number of sides for the polygon.
    edge_length : float > 0 , Default = 1, optional
        The desired edge length.
    centre : (x, y) - 2D Cartesian Coordinate, Default = (0, 0), optional
        Centre position for the polygon.
    rotation : angle, Default = 0, optional
        The angle, in degrees, to rotate the polygon arounds its centre anti-clockwise.

    Notes
    -----
    Default Squares are initialised with an additional 45 degrees of rotation as to orient
    their sides parallel with the x and y axes.
    """
    def __new__(cls, sides, edge_length: float = 1, centre = (0, 0), rotation: float = 0):
        """
        """
        if sides == 3:
            return EquilateralTriangle(edge_length, centre, rotation)
        elif sides == 4:
            return Square(edge_length, centre, rotation + 45)
        elif sides == 5:
            return Pentagon(edge_length, centre, rotation)
        elif sides == 6:
            return Hexagon(edge_length, centre, rotation)
        elif sides == 7:
            return Septagon(edge_length, centre, rotation)
        elif sides == 8:
            return Octagon(edge_length, centre, rotation)


# NON-REGULAR POLYGON FACTORY
class Build_NonRegular():
    """
    """
    def __new__(cls, sides, *angles):
        """
        """
        return