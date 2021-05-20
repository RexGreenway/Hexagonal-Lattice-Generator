"""
**********
Non Regular Polygon Classes
**********
Non Regular Polygon classes for PolyLatLib.

This file contains the non-regular classes and non-regular polygon presets for PolyLatLib, establishing
the key attributes for all non-regular polygons.

"""

import abc
from polylatlib.classes.base_shapes import Polygon, Lattice, FourSided
from polylatlib.classes.regular import Square
from polylatlib.functions import add_vectors, change_to_cart_list

__all__ = [
    "NonRegularPolygon",
    "Rectangle",
    "Parallelogram"
]

class NonRegularPolygon(Polygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, centre, rotation):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__()
        self.centre = centre
        self.rotation = rotation
        self.polygon_vectors = self.generate_polygon_vectors()

        self.radius_vec = self.get_radius_vec()
        start_point = (centre[0] + self.radius_vec[0], centre[1] + self.radius_vec[1])

        self.generate_shape(start_point, 0, self.polygon_vectors)
        
    def get_radius_vec(self):
        """
        Returns vector from inital point or starting point to the centrooid of the shape.
        If we want the shape to be centred on (0, 0), for example, we need to do negative
        of this vector to get to starting point.
        """
        n = len(self.polygon_vectors)
        x, y = 0, 0
        start_point = [0, 0]
        for i in range(n - 1):
            start_point[0] += self.polygon_vectors[i][0]
            start_point[1] += self.polygon_vectors[i][1]
            x += start_point[0]
            y += start_point[1]
        return (-x/n, -y/n)

    @abc.abstractmethod
    def generate_polygon_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """


class Rectangle(NonRegularPolygon, FourSided):
    """
    PRESET SHAPE: Rectangle
    """
    def __new__(cls, width, height, centre = (0, 0), rotation = 0):
        """
        If Width == Height return Sqaure class object instead.
        """
        if width == height:
            return Square(width, centre, rotation)
        else:
            return super(Rectangle, cls).__new__(cls)

    def __init__(self, width, height, centre = (0, 0), rotation = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        self.height = height
        self.width = width
        super().__init__(centre, rotation)
    
    def generate_change_vectors(self): 
        """
        IMPLEMENT DOCUMENTATION
        """
        return self.polygon_vectors

    def generate_polygon_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        vectors = []
        for i in range(0, 4, 2):
            width_polar = (-self.width, i*90 + self.rotation)
            height_polar = (-self.height, (i + 1)*90 + self.rotation)
            vectors.append(width_polar)
            vectors.append(height_polar)
        return change_to_cart_list(vectors)
    
    def get_lattice_state(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return True
    

class Parallelogram(NonRegularPolygon, FourSided):
    """
    PRESET SHAPE: Parallelogram

    Parameters
    ----------
    angle : 0 < int < 180]
        Angle of parallelogram in bottom left corner....
    """
    def __new__(cls, width, height, angle, centre = (0, 0), rotation = 0):
        """
        If just angle == 90 then rectangle. this carries over to square in rectangle
        initialisation...
        """
        if angle == 90:
            return Rectangle(width, height, centre, rotation)
        else:
            return super(Parallelogram, cls).__new__(cls)
    
    def __init__(self, width, height, angle, centre = (0, 0), rotation = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        self.height = height
        self.width = width
        self.angle = angle
        super().__init__(centre, rotation)

    def generate_change_vectors(self): 
        """
        IMPLEMENT DOCUMENTATION
        """
        return self.polygon_vectors

    def generate_polygon_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        vectors = []
        for i in range(0, 4, 2):
            width_polar = (-self.width, i*90 + self.rotation)
            height_polar = (-self.height, (i + 1)*90 - 90 + self.angle + self.rotation)
            vectors.append(width_polar)
            vectors.append(height_polar)
        return change_to_cart_list(vectors)
    
    def get_lattice_state(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return True