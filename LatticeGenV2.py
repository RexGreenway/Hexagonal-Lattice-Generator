import networkx as nx
import abc
import cv2 as cv
import numpy as np
from math import sin, cos, radians, sqrt, pi
import matplotlib.pyplot as plt

from LatticeGen_Funcs import my_filled_circle, my_line, add_vectors, draw_graph, change_to_cart

### CHILD CLASS of NetworkX GRAPH Class, to handle and manipulate polygons ###
class Polygon(nx.Graph):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__()
    
    def view_info(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        print("Nodes: ", self.nodes.data())
        print("Edges: ", self.edges.data())

    # TEMP - need to clean up open cv file stuff and re-work postion finding (move open cv stuff to seperate file, like the draw_shape function).
    def draw_shape(self, diagram):
        """
        IMPLEMENT DOCUMENTATION
        """
        # Creates White Canvas
        W = 800
        size = W, W, 3
        image = np.ones(size) 
        # Get Graph Details
        dic = nx.get_node_attributes(diagram, "pos")
        graph = {0: dic, 1: diagram}
        # Draw Edges
        for edge in graph[1].edges:  
            start_pos = graph[0][edge[0]]
            start_pos_big = tuple([int(x * 20 + W/2) for x in start_pos])  # adapt position coords for pixel display
            end_pos = graph[0][edge[1]]
            end_pos_big = tuple([int(x * 20 + W/2) for x in end_pos])  # adapt position coords for pixel display
            my_line(image, start_pos_big, end_pos_big)
        # Draw Nodes
        for node in graph[0]:  # draw nodes
            node_pos = graph[0][node]
            node_pos_big = tuple([int(x * 20 + W/2)for x in node_pos])  # adapt position coords for pixel display
            my_filled_circle(image, node_pos_big)
        # Creates window
        cv.namedWindow("Diagram", cv.WINDOW_AUTOSIZE)  
        cv.imshow("Diagram", image)  # displays window with image
        cv.waitKey(0)
        cv.destroyAllWindows()

    ## ABSTRACT METHDOS (Implemented below) ##
    @abc.abstractmethod
    def generate_shape(self):
        """
        IMPLEMENT DOCUMENTATION test test
        """
        pass

    @abc.abstractmethod
    def get_lattice_state(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        pass

    @abc.abstractmethod
    def generate_lattice(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        pass


## REGULAR POLYGONS Subclass ##
class RegularPolygon(Polygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, sides: int, edgeLength: [int,float] = 1, rotation: (-360,360) = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        # Inherit initialisation of grpah from Shape parent
        super().__init__()
        self.sides = sides
        self.edgeLength = edgeLength
        self.rotation = rotation  # OPEN CV is rotating this in the wrong direction!!!!!!!

        # Error handling if a certain rules not met.
        if self.sides < 3:
            raise ValueError("Argument 'sides' = {self.sides}. A regular polygon have at least 3 sides.".format(self=self))
        elif self.edgeLength < 0:
            raise ValueError("Argument 'edgeLength' = {self.edgeLength}. Edges cannot be of negative length.".format(self=self))
        elif self.rotation < - 360 and self.rotation > 360:
            raise ValueError("Argument 'rotation' = {self.rotation}. Shape rotations should be within range (-360, 360).".format(self=self))
        
        self.intAngle = round(((self.sides - 2)*180)/self.sides, 2)
        self.theta = 180 - self.intAngle
        self.radius = round((self.edgeLength)/(2*sin(radians(self.theta/2))), 2)
        self.generate_shape()

        self.can_lattice = self.get_lattice_state()

    # Generate single shape for Regular Polygons
    def generate_shape(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        pos = []
        for i in range(self.sides):
            x = self.radius*cos(radians(i*self.theta + self.rotation))
            y = self.radius*sin(radians(i*self.theta + self.rotation))
            coord = [round(x, 2), round(y, 2)]
            pos.append(coord)
            self.add_node(i, pos = tuple(pos[i]))
        for i in range(self.sides - 1):
            self.add_edge(i, i + 1)
        self.add_edge(self.sides - 1, 0)

    # 'can_lattice' getter for Regular Polygons
    def get_lattice_state(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        lattice_test = 360/self.intAngle
        return lattice_test.is_integer()

    def generate_lattice(self, layers):
        """
        IMPLEMENT DOCUMENTATION
        """
        if self.can_lattice:
            chg_vectors = self._generate_change_vectors()
            self.lattice = self._generate_lattice_graph(layers, chg_vectors)
            return self.lattice
        else:
            print("LATTICE NOT POSSIBLE WITH THIS SHAPE")
    
    @abc.abstractmethod
    def _generate_change_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        pass

    @abc.abstractmethod
    def _generate_lattice_graph(self, layers, chg_vectors):
        """
        IMPLEMENT DOCUMENTATION
        """
        pass



## DEFAULT SHAPES (with space to expand into some shape specific manipulation/ generation)##
class Triangle(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edgeLength: [int,float] = 1, rotation: (-360,360) = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(3, edgeLength, rotation)
    
    def _get_shape_num(self, layers):
        """
        IMPLEMENT DOCUMENTATION
        """
        return int(3*((layers*(layers - 1)/2))+1)
    
    def _generate_change_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        base_vectors = {}
        for i in range(2*self.sides):
            base_vectors[i] = (self.edgeLength, 30 + (i + 1)*self.intAngle + self.rotation)
        change_vectors = change_to_cart(base_vectors)
        return change_vectors
    
    def _generate_lattice_graph(self, layers, chg_vectors):
        """
        IMPLEMENT DOCUMENTATION
        """
        # Generates the 2 (relected) triangles used.
        cart_one = {}
        for i in range(self.sides):
            cart_one[i] = chg_vectors[2*i + 1]
        cart_two = {}
        for i in range(self.sides):
            cart_two[i] = chg_vectors[len(chg_vectors) - (2*i + 1)]

        rad_x = round(self.radius*cos(radians(self.rotation)), 3)
        rad_y = round(self.radius*sin(radians(self.rotation)), 3)
        radius_vec = (rad_x, rad_y)

        lattice = nx.Graph()
        shape = 0
        origin_node_even = add_vectors((0, 0), radius_vec)
        for layer in range(layers):
            if layer == 0:
                draw_graph(origin_node_even, lattice, shape, 3, cart_one, 1)
            else:
                if layer % 2 == 0: # Odd Layers
                    origin_node_even = add_vectors(origin_node_even, chg_vectors[5])
                    origin_node_even = add_vectors(origin_node_even, chg_vectors[4])
                    node_pos = origin_node_even
                    for i in range(3):
                        for _ in range(int(layer/2)):
                            shape += 1
                            draw_graph(node_pos, lattice, shape, 3, cart_one, 1)
                            node_pos = add_vectors(node_pos, chg_vectors[2*i])
                        for _ in range(int(layer/2)):
                            shape += 1
                            draw_graph(node_pos, lattice, shape, 3, cart_one, 1)
                            node_pos = add_vectors(node_pos, chg_vectors[(2*i) + 1])    
                else: # Even Layers
                    origin_node_even = add_vectors(origin_node_even, chg_vectors[2])
                    node_pos = origin_node_even
                    for i in range(3):
                        for _ in range(int((layer + 1)/2)):
                            shape += 1
                            draw_graph(node_pos, lattice, shape, 3, cart_two, 1)
                            node_pos = add_vectors(node_pos, chg_vectors[2*i])
                        for _ in range(int((layer + 1)/2) - 1):
                            shape += 1
                            draw_graph(node_pos, lattice, shape, 3, cart_two, 1)
                            node_pos = add_vectors(node_pos, chg_vectors[(2*i) + 1])
        return lattice


class Square(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edgeLength: [int,float] = 1, rotation: (-360,360) = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(4, edgeLength, rotation)
    
    def _get_shape_num(self, layers):
        """
        IMPLEMENT DOCUMENTATION
        """
        return int((1 + (layers - 1)*2)**2)

    def _generate_change_vectors(self): 
        """
        IMPLEMENT DOCUMENTATION
        """
        polar_vectors = {}
        for i in range(self.sides):
            polar_vectors[i] = (self.edgeLength, i*self.theta + (180 - (self.intAngle/2)) + self.rotation)
        edge_vectors = change_to_cart(polar_vectors)
        return edge_vectors

    def _generate_lattice_graph(self, layers, chg_vectors):
        """
        IMPLEMENT 
        """
        lattice = nx.Graph()
        
        rad_x = round(self.radius*cos(radians(self.rotation)), 2)
        rad_y = round(self.radius*sin(radians(self.rotation)), 2)

        layer_list = list(range(layers))
        even_numbers = list(range(0, 2*layers, 2))
        shape = 0
        for layer in layer_list:
            radius_vec = (round((layer*2*rad_x) + rad_x, 2), round((layer*2*rad_y) + rad_y, 2))
            start_node_pos = add_vectors((0, 0), radius_vec)
            if layer == 0:
                draw_graph(start_node_pos, lattice, shape, self.sides, chg_vectors, self.edgeLength)
                shape += 1
            else:
                for i in range(self.sides):
                    for _ in range(even_numbers[layer]):
                        draw_graph(start_node_pos, lattice, shape, self.sides, chg_vectors, self.edgeLength)
                        start_node_pos = add_vectors(start_node_pos, chg_vectors[i])
                        shape += 1
        return lattice
    

class Pentagon(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edgeLength: [int,float] = 1, rotation: (-360,360) = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(5, edgeLength, rotation)

class Hexagon(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edgeLength: [int,float] = 1, rotation: (-360,360) = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(6, edgeLength, rotation)
    
    def _get_shape_num(self, layers):
        """
        IMPLEMENT DOCUMENTATION
        """
        return int(1 + 6 * ((layers * (layers - 1)) / 2))
    
    def _generate_change_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        edgeLengthPlus = 1.5*self.edgeLength
        halfHexHeight = round(sqrt(0.75*((self.edgeLength)**2)), 2)
        vector_length = round(sqrt(edgeLengthPlus**2 + halfHexHeight**2), 2)
        base_vector = {}
        for i in range(self.sides):
            base_vector[i] = (vector_length, i*(self.theta) + self.theta/2 + self.rotation)
        change_vectors = change_to_cart(base_vector)
        return change_vectors
    
    def _generate_lattice_graph(self, layers, chg_vectors):
        """
        IMPLEMENT 
        """
        lattice = nx.Graph()
        
        rad_x = round(self.radius*cos(radians(self.rotation)), 2)
        rad_y = round(self.radius*sin(radians(self.rotation)), 2)
        radius_vec = (rad_x, rad_y)

        vectors = {}
        for i in range(6):
            x = self.radius*cos(radians(i*self.theta + (180 - (self.intAngle/2)) + self.rotation))
            y = self.radius*sin(radians(i*self.theta + (180 - (self.intAngle/2)) + self.rotation))
            vectors[i] = (round(x, 2), round(y, 2))
        
        shape = 1
        for layer in range(layers):
            if layer == 0:
                start_node_pos = add_vectors((0, 0), radius_vec)
                draw_graph(start_node_pos, lattice, 0, self.sides, vectors, self.edgeLength)
            else:
                start_node_pos = add_vectors(start_node_pos, chg_vectors[4])
                draw_graph(start_node_pos, lattice, shape, self.sides, vectors, self.edgeLength)
                for i in range(self.sides):
                    for _ in range(layer):
                        shape += 1
                        start_node_pos = add_vectors(start_node_pos, chg_vectors[i])
                        draw_graph(start_node_pos, lattice, shape, self.sides, vectors, self.edgeLength)
        
        return lattice


class Septagon(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edgeLength: [int,float] = 1, rotation: (-360,360) = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(7, edgeLength, rotation)

class Octagon(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edgeLength: [int,float] = 1, rotation: (-360,360) = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(8, edgeLength, rotation)
