from math import sqrt, sin, cos, radians
from polylatlib.classes.base_shapes import Shape, Polygon, Lattice
from polylatlib.functions import *
from polylatlib.exception import *

__all__ = [
    "RegularPolygon",
    "EquilateralTriangle",
    "Square",
    "Pentagon",
    "Hexagon",
    "Septagon",
    "Octagon"
]


class RegularPolygon(Polygon):
    """
    Regular polygons are defined to be polygons with all edges having equal length and all
    internal angles the same.

    Attributes
    ----------
    .int_angle : The angle between edges within the shape.
    .theta : The angle from one radii, from the centre to each vertex, to the next.
    .radius : The length from the centre to any vertex in a regular polygon.
    .radius_vector : The vector from the centre to the initial vertex, with regard to rotation.

    Example
    -------
    >>> ADD EXAMPLE

    Notes
    -----    
    Regular Polygons are defined by their number of sides and edge length. When
    initialised, RegularPolygon implements both these parameters along with a user
    defined centre for the shape and an angle of rotation. When called regular polygons
    are automatically generated with help from some variables detailed below;

    The polygons of this type can thus be defined simply by their number of sides and edge
    length. Along with a given centre and a rotation all further features of these shapes can
    be found through private class methods.
    """
    def __init__(self, sides: int, edge_length, centre, rotation):
        """
        Initialises a Reular Polygon object.

        Parameters
        ----------
        sides : int > 3
            The number of sides for the regular polygon (Attribute).
        edge_length : float > 0,
            Edge length for all edges of the shape (Attribute).
        centre : (x, y) - 2D Cartesian Coordinate
            Centre point for the shape. For regular polygons this is possible as the uniform nature
            of the shape results in an equal radius to each vertex in the polygon (Attribute).
        rotation : angle
            The angle, in degrees, to rotate the shape around the centre anti-clockwise. This value
            is cyclic with period 360 degrees (Attribute).
        
        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        self.sides = sides
        self.edge_length = edge_length
        self.centre = centre
        self.rotation = rotation

        # Error Handling for input attributes.
        if self.sides < 3:
            raise ValueError(f"Argument 'sides' = {self.sides}. A regular polygon have at least 3 sides.")
        elif self.edge_length < 0:
            raise ValueError("Argument 'edge_length' = {self.edge_length}. Edges cannot be of negative length.".format(self=self))
        elif not check_if_coord(self.centre):
            raise PolyLatNotCart(self.centre)

        super().__init__()

        # Set Radius related attributes
        self.int_angle = round(((sides - 2)*180)/sides, 3)
        self.theta = 180 - self.int_angle
        self.radius = round((edge_length)/(2*sin(radians(self.theta/2))), 3)
        self.radius_vec = change_to_cart_vector((self.radius, rotation))

        # Generate polygon
        polygon_vectors = self.generate_polygon_vectors()
        start_pos = add_vectors(centre, self.radius_vec)
        self.generate_shape(start_pos, 0, polygon_vectors)

    
    def generate_polygon_vectors(self):
        """
        Generates and returns the edge vectors for a regular polygon.
            
        Returns
        -------
        edge_vectors : list
            List with edge vectors as values.

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        edge_vectors = []
        for i in range(self.sides):
            angle = i*self.theta + (180 - (self.int_angle/2)) + self.rotation
            edge_vectors.append(change_to_cart_vector((self.edge_length, angle)))
        return edge_vectors
    
    def get_lattice_state(self):
        """
        Returns True if lattice can be generated from current regular polygon. False otherwise.

        Returns
        -------
        boolean
            Returns True if lattice can be generated from current regular polygon. False if not. 

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        lattice_test = 360/self.int_angle
        return lattice_test.is_integer()
    
    

################## PRESETs for REGULAR POLYGONs ######################


class EquilateralTriangle(RegularPolygon):
    """
    PRESET SHAPE: EquilateralTriangle

    Equilateral triangles are 3 sided polygons with equal edge length and internal angle of 60
    degrees. The default Equilateral Triangle is generated "pointing" along the x-axis in the
    positive direction centred at the origin (0, 0). 
    """
    def __init__(self, edge_length: float = 1, centre = (0, 0), rotation: float = 0):
        """
        Equilateral Triangles are initialised as Regular Polygons with 3 sides.

        Parameters
        ----------
        edge_length : float > 0, Default = 1, optional
            The deired edge length for the triangles.
        centre : (x, y) - 2D Cartesian Coordinate, Default = (0, 0), optional
            Centre position for the triangle.
        rotation : angle, Default = 0, optional
            The angle, in degrees, to rotate the triangle arounds its centre anti-clockwise.
        
        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        super().__init__(3, edge_length, centre, rotation)

    def generate_lattice_circular(self, layers: int):
        """
        Generates and returns the circular lattice for Equilateral Triangles.

        Parameters
        ----------
        layers : int > 0
            The number of desired layers in the lattice.

        Returns
        -------
        lattice : Lattice
            Lattice object from 

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        polar_vectors = []
        for i in range(2*self.sides):
            polar_vectors.append((self.edge_length, 30 + (i + 1)*self.int_angle + self.rotation))
        chg_vectors = change_to_cart_list(polar_vectors)

        triangle_one = []
        for i in range(self.sides):
            triangle_one.append(chg_vectors[2*i + 1])
        triangle_two = []
        for i in range(self.sides):
            triangle_two.append(chg_vectors[len(chg_vectors) - (2*i + 1)])
        
        lattice = Lattice(layers)
        shape = 0
        origin_vertex = add_vectors(self.centre, self.radius_vec)
        for layer in range(layers):
            if layer == 0:
                lattice.generate_shape(origin_vertex, shape, triangle_one)
            else:
                if layer % 2 == 0: # Odd Layers
                    origin_vertex = add_vectors(origin_vertex, chg_vectors[5])
                    origin_vertex = add_vectors(origin_vertex, chg_vectors[4])
                    vertex_pos = origin_vertex
                    for i in range(3):
                        for _ in range(int(layer/2)):
                            shape += 1
                            lattice.generate_shape(vertex_pos, shape, triangle_one)
                            vertex_pos = add_vectors(vertex_pos, chg_vectors[2*i])
                        for _ in range(int(layer/2)):
                            shape += 1
                            lattice.generate_shape(vertex_pos, shape, triangle_one)
                            vertex_pos = add_vectors(vertex_pos, chg_vectors[(2*i) + 1])    
                else: # Even Layers
                    origin_vertex = add_vectors(origin_vertex, chg_vectors[2])
                    vertex_pos = origin_vertex
                    for i in range(3):
                        for _ in range(int((layer + 1)/2)):
                            shape += 1
                            lattice.generate_shape(vertex_pos, shape, triangle_two)
                            vertex_pos = add_vectors(vertex_pos, chg_vectors[2*i])
                        for _ in range(int((layer + 1)/2) - 1):
                            shape += 1
                            lattice.generate_shape(vertex_pos, shape, triangle_two)
                            vertex_pos = add_vectors(vertex_pos, chg_vectors[(2*i) + 1])
        return lattice


class Square(RegularPolygon):
    """
    PRESET SHAPE: Square

    Squares are 4 sided polygons with internal angles of 90 degrees. The default square is positioned with
    its edges at 45 degree angles to the x-axis, centred at the origin.
    """
    def __init__(self, edge_length: float = 1, centre = (0, 0), rotation: float = 0):
        """
        Squares are initialised as Regular Polygons with 4 sides.

        Parameters
        ----------
        edge_length : float > 0, Default = 1, optional
            The deired edge length for the triangles.
        centre : (x, y) - 2D Cartesian Coordinate, Default = (0, 0), optional
            Centre position for the triangle.
        rotation : angle, Default = 0, optional
            The angle, in degrees, to rotate the triangle arounds its centre anti-clockwise.
        
        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        super().__init__(4, edge_length, centre, rotation)

    def generate_lattice_circular(self, layers: int):
        """
        Generates and returns the circular lattice for Squares.

        Parameters
        ----------
        layers : int > 0
            The number of desired layers in the lattice.

        Returns
        -------
        lattice : Lattice
            Lattice object from 

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        chg_vectors = list(self.get_edge_vectors().values())

        lattice = Lattice(layers)

        even_numbers = list(range(0, 2*layers, 2))
        shape = 0
        for layer in range(layers):
            radius_vec = (round((layer*2*self.radius_vec[0]) + self.radius_vec[0], 3), round((layer*2*self.radius_vec[1]) + self.radius_vec[1], 3))
            start_vertex_pos = add_vectors(self.centre, radius_vec)
            if layer == 0:
                lattice.generate_shape(start_vertex_pos, shape, chg_vectors)
                shape += 1
            else:
                for i in range(self.sides):
                    for _ in range(even_numbers[layer]):
                        lattice.generate_shape(start_vertex_pos, shape, chg_vectors)
                        start_vertex_pos = add_vectors(start_vertex_pos, chg_vectors[i])
                        shape += 1
        return lattice


class Pentagon(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edge_length: float = 1, centre = (0, 0), rotation: float = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(5, edge_length, centre, rotation)


class Hexagon(RegularPolygon):
    """
    PRESET SHAPE: Hexagon

    Regular hexagons are 6 sided polygons with internal angles of 120 degrees. The default Hexagon is positioned with
    its "top" and "bottom" edges parallel to the x-axis, centred at the origin.
    """
    def __init__(self, edge_length: float = 1, centre = (0, 0), rotation: float = 0):
        """
        Hexagons are initialised as Regular Polygons with 6 sides.

        Parameters
        ----------
        edge_length : float > 0, Default = 1, optional
            The deired edge length for the triangles.
        centre : (x, y) - 2D Cartesian Coordinate, Default = (0, 0), optional
            Centre position for the triangle.
        rotation : angle, Default = 0, optional
            The angle, in degrees, to rotate the triangle arounds its centre anti-clockwise.
        
        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        super().__init__(6, edge_length, centre, rotation)
    
    def generate_lattice_circular(self, layers: int):
        """
        Generates and returns the circular lattice for Hexagons.

        Parameters
        ----------
        layers : int > 0
            The number of desired layers in the lattice.

        Returns
        -------
        lattice : Lattice
            Lattice object from 

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        edgeLengthPlus = 1.5*self.edge_length
        halfHexHeight = round(sqrt(0.75*((self.edge_length)**2)), 2)
        vector_length = round(sqrt(edgeLengthPlus**2 + halfHexHeight**2), 2)
        polar_vectors = []
        for i in range(self.sides):
            polar_vectors.append((vector_length, i*(self.theta) + self.theta/2 + self.rotation))
        chg_vectors = change_to_cart_list(polar_vectors)

        lattice = Lattice(layers)
        polygon_vectors = list(self.get_edge_vectors().values())

        shape = 1
        for layer in range(layers):
            if layer == 0:
                start_vertex_pos = add_vectors(self.centre, self.radius_vec)
                lattice.generate_shape(start_vertex_pos, 0, polygon_vectors)
            else:
                start_vertex_pos = add_vectors(start_vertex_pos, chg_vectors[4])
                lattice.generate_shape(start_vertex_pos, shape, polygon_vectors)
                for i in range(self.sides):
                    for _ in range(layer):
                        shape += 1
                        start_vertex_pos = add_vectors(start_vertex_pos, chg_vectors[i])
                        lattice.generate_shape(start_vertex_pos, shape, polygon_vectors)
        return lattice


class Septagon(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edge_length: float = 1, centre = (0, 0), rotation: float = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(7, edge_length, centre, rotation)


class Octagon(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edge_length: float = 1, centre = (0, 0), rotation: float = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(8, edge_length, centre, rotation)
