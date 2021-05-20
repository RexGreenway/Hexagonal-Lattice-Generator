"""
**********
Non Regular Polygon Classes
**********
Non Regular Polygon classes for PolyLatLib.

This file contains the non-regular classes and non-regular polygon presets for PolyLatLib, establishing
the key attributes for all non-regular polygons.

"""

import abc
from polylatlib.classes.base_shapes import Polygon, Lattice
from polylatlib.classes.regular import Square
from polylatlib.functions import add_vectors, change_to_cart_list

__all__ = [
    "NonRegularPolygon",
    "FourSided",
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

class FourSided(Polygon):
    """
    Put this into the base classes file???? For use with SQUARE ASWELL
    
    If can be made into a lattice then this 
    """
    def generate_lattice_circular(self, layers: int):
        """
        IMPLEMENT DOCUMENTATION
        """
        chg_vectors = list(self.get_edge_vectors().values())

        lattice = Lattice()

        even_numbers = list(range(0, 2*layers, 2))
        shape = 0
        for layer in range(layers):
            radius_vec = (round((layer*2*self.radius_vec[0]) + self.radius_vec[0], 3), round((layer*2*self.radius_vec[1]) + self.radius_vec[1], 3))
            start_vertex_pos = add_vectors(self.centre, radius_vec)
            if layer == 0:
                lattice.generate_shape(start_vertex_pos, shape, chg_vectors)
                shape += 1
            else:
                for i in range(4):
                    for _ in range(even_numbers[layer]):
                        lattice.generate_shape(start_vertex_pos, shape, chg_vectors)
                        start_vertex_pos = add_vectors(start_vertex_pos, chg_vectors[i])
                        shape += 1
        return lattice
    
    def generate_lattice_stacked(self, rows, columns):
        """
        """
        edge_vec = list(self.get_edge_vectors().values())
        move_row = edge_vec[3]
        move_col = edge_vec[2]
        lattice  = Lattice()
        start_pos = add_vectors(self.centre, self.radius_vec)
        for i in range(rows):
            vertex_pos = start_pos
            for j in range(columns):
                lattice.generate_shape(vertex_pos, str(i) + "." + str(j), edge_vec)
                vertex_pos = add_vectors(vertex_pos, move_col)
            start_pos = add_vectors(start_pos, move_row)
        return lattice



class Rectangle(NonRegularPolygon, FourSided):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __new__(cls, width, height, centre = (0, 0), rotation = 0):
        """
        If Width == Height return Sqaure class object instead.
        """
        if width == height:
            return Square(width, centre, rotation + 45)
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
        ## CHANGE TO LIST OF VECTORS
        vectors = []
        for i in range(0, 4, 2):
            height_polar = (-self.width, i*90 + self.rotation)
            width_polar = (-self.height, (i + 1)*90 + self.rotation)
            vectors.append(height_polar)
            vectors.append(width_polar)
        return change_to_cart_list(vectors)
    
    def get_lattice_state(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return True
    

class Parallelogram(NonRegularPolygon, FourSided):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, width, height, angle, start_point = (0, 0), rotation = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        self.height = height
        self.width = width
        self.angle = angle
        super().__init__(start_point, rotation)

    def generate_change_vectors(self): 
        """
        IMPLEMENT DOCUMENTATION
        """
        return self.polygon_vectors

    def generate_polygon_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        ## CHANGE TO LIST OF VECTORS
        vectors = []
        for i in range(0, 4, 2):
            height_polar = (self.height, (i + 1)*90 + self.angle + self.rotation)
            width_polar = (self.width, (i + 2)*90 + self.rotation)
            vectors.append(height_polar)
            vectors.append(width_polar)
        return change_to_cart_list(vectors)
    
    def get_lattice_state(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return True