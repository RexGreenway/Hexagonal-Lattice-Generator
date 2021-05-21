"""
**********
Class Factorys
**********
Factory classes for PolyLatLib.

This file contains the Builder or Factory Classes for the various Preset Shapes
within the code:

- Build_Shape : The base builder class provides the funcionality to create any
    PolyLatLib shape object given a defining path of vectors and centre point. 
    Dynamically detects Polygon connectedness condition and passes to sub-builder
    if necessary.
- Build_Polygon : Similar to shape builder - will check connectedness first and will
    return either generic polygon or Preset Polygon if applicable.
- Build_Regular : Given a number of sides, as well as optional edge length, centre
    point, and rotation, returns the applicable Preset if it exists (2 < sides < 9).
"""

## IMPORTS
from matplotlib.pyplot import connect
from polylatlib.classes.base_shapes import Shape, Polygon
from polylatlib.classes.regular import *
from polylatlib.classes.nonregular import Parallelogram
from polylatlib.exception import *
from math import atan, sqrt, acos, degrees

__all__ = [
    "Build_Regular",
    "Build_Polygon",
    "Build_Shape"
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
        else:
            return RegularPolygon(sides, edge_length, centre, rotation)


# POLYGON FACTORY
class Build_Polygon():
    """
    Returns a corresponding Polygon class object given defining vectors and centre point

    Parameters
    ----------
    defining_vectors : list(Vectors (x, y))
        List of ordered vectors describing the path of the shapes edges.
    centre : Coord. (x, y)
        Centre point the shape is built around.
    """
    def __new__(cls, defining_vectors, centre):
        # Lengths and angles of the input shape vectors.
        end_point = [0, 0]
        lengths = []
        angles = []
        for i in range(len(defining_vectors)):
            end_point[0] += defining_vectors[i][0]
            end_point[1] += defining_vectors[i][1]
            a, b = defining_vectors[i - 1], defining_vectors[i]
            a_mag, b_mag = sqrt(a[0]**2 + a[1]**2), sqrt(b[0]**2 + b[1]**2)
            ab_dot = -a[0]*b[0] + -a[1]*b[1]
            lengths.append(b_mag)
            angles.append(degrees(acos(ab_dot / (a_mag * b_mag))))

        # Connectedness Check
        if end_point != [0, 0]:
            raise PolyLatError("Provided defining_vectors must define a closed shape.")

        # Rotation
        ang = degrees(atan(defining_vectors[0][1] / defining_vectors[0][0]))
        
        # 4 Sided Presets
        if len(lengths) == 4 and angles[0] == angles[2]:
            return Parallelogram(lengths[0], lengths[1], angles[0], centre, ang)

        # Regular Polygons
        elif all(x == angles[0] for x in angles):
            if all(x == lengths[0] for x in lengths):
                return Build_Regular(len(lengths), lengths[0], centre, ang)
        
        # Non Preset Polygon
        n = len(defining_vectors)
        x, y = 0, 0
        start_point = [0, 0]
        for i in range(n - 1):
            start_point[0] += defining_vectors[i][0]
            start_point[1] += defining_vectors[i][1]
            x += start_point[0] / n
            y += start_point[1] / n

        poly = Polygon()
        poly.generate_shape((centre[0] - x, centre[1] - y), "Polygon", defining_vectors)
        return poly


# ALL SHAPE FACTORY
class Build_Shape():
    """
    Returns a corresponding Shape class object given defining vectors and centre point

    Parameters
    ----------
    defining_vectors : list(Vectors (x, y))
        List of ordered vectors describing the path of the shapes edges.
    centre : Coord. (x, y)
        Centre point the shape is built around.
    """
    def __new__(cls, defining_vectors, centre):
        # Calc centroid vector and vector path to endpoint.
        x, y = 0, 0
        start_point = [0, 0]
        for i in range(len(defining_vectors)):
            start_point[0] += defining_vectors[i][0]
            start_point[1] += defining_vectors[i][1]
            if i != len(defining_vectors) - 1:
                x += start_point[0] / len(defining_vectors)
                y += start_point[1] / len(defining_vectors)

        # Polygon if startpoint = endpoint
        if start_point == [0, 0]:            
            return Build_Polygon(defining_vectors, centre)

        else:
            # Return Shape Object (grpah of vertexes and edges)
            shape = Shape()
            shape.generate_shape((centre[0] - x, centre[1] - y), "Shape", defining_vectors)
            return shape
