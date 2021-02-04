import abc
import cv2 as cv
import numpy as np
from math import sqrt, sin, cos, radians
from LatticeGen_Funcs import add_vectors, change_to_cart_dict, change_to_cart_vector, check_if_coord, my_filled_circle, my_line

colours = ["black", "red", "green", "blue", "yellow", "orange", "purple"]

# Collection of vertices (position, size, colour) and edges (weight, colour)...
class Shape():
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        self.vertices = []
        self.vertices_info = []
        self.edges = []
        self.edges_info = []

    def add_vertex(self, vertex_for_adding, position = None, size = 1, colour = "black"):
        """
        IMPLEMENT DOCUMENTATION
        """
        if vertex_for_adding not in self.vertices:
            self.vertices.append(vertex_for_adding)
            info = {
                "position": position,
                "size": size,
                "colour": colour
            }
            self.vertices_info.append((vertex_for_adding, info)) 
        else:
            print("This vertex already exists.")

    def _update_vertex_attribute(self, vertex_for_update, attr, value):
        """
        IMPLEMENT DOCUMENTATION
        """
        try:
            index = self.vertices.index(vertex_for_update)
            self.vertices_info[index][1][attr] = value
        except:
            raise ValueError("The vertex entered does not exist.")
    
    def update_vertex_position(self, vertex_for_update, value):
        """
        IMPLEMENT DOCUMENTATION
        """
        if check_if_coord(value):
            self._update_vertex_attribute(vertex_for_update, "position", value)
        else:
            raise ValueError(value, " - position should be a cartesian coordinate.")
    
    def update_vertex_size(self, vertex_for_update, value):
        """
        IMPLEMENT DOCUMENTATION
        """
        if type(value) == int:
            self._update_vertex_attribute(vertex_for_update, "size", value)
        else:
            raise ValueError(value, " - size should be an integer.")

    def update_vertex_colour(self, vertex_for_update, value):
        """
        IMPLEMENT DOCUMENTATION
        """
        if value in colours:
            self._update_vertex_attribute(vertex_for_update, "colour", value)
        else:
            raise ValueError(value, " - not a supported colour.")

    def _get_vertex_info(self, desired_info):
        """
        IMPLEMENT DOCUMENTATION
        """
        vertex_info = {}
        for vertex in self.vertices_info:
            vertex_info[vertex[0]] = vertex[1][desired_info]
        return vertex_info

    def get_vertex_positions(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return self._get_vertex_info("position")

    def get_vertex_sizes(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return self._get_vertex_info("size")
    
    def get_vertex_colours(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return self._get_vertex_info("colour")

    def add_edge(self, vertex_one, vertex_two, weight = 1, colour = "black"):
        """
        IMPLEMENT DOCUMENTATION
        """
        if (vertex_one, vertex_two) not in self.edges and (vertex_two, vertex_one) not in self.edges:
            self.edges.append((vertex_one, vertex_two))
            info = {
                "weight": weight,
                "colour": colour
            }
            self.edges_info.append((vertex_one, vertex_two, info))
            for vertex in (vertex_one, vertex_two):
                if vertex not in self.vertices:
                    self.add_vertex(vertex)
        else:
            pass
    
    def _update_edge_attribute(self, edge_for_update, attr, value):
        """
        IMPLEMENT DOCUMENTATION
        """
        if edge_for_update in self.edges:
            index = self.edges.index(edge_for_update)
            self.edges_info[index][2][attr] = value
        else:
            try:
                index = self.edges.index((edge_for_update[1], edge_for_update[0]))
                self.edges_info[index][2][attr] = value
            except:
                raise ValueError("The edge entered does not exist.")

    def update_edge_weight(self, edge_for_update, value):
        """
        IMPLEMENT DOCUMENTATION
        """
        self._update_edge_attribute(edge_for_update, "weight", value)

    def update_edge_colour(self, edge_for_update, value):
        """
        IMPLEMENT DOCUMENTATION
        """
        self._update_edge_attribute(edge_for_update, "colour", value)
    
    def _get_edge_info(self, desired_info):
        """
        IMPLEMENT DOCUMENTATION
        """
        edge_info = {}
        for edge in self.edges_info:
            edge_info[(edge[0], edge[1])] = edge[2][desired_info]
        return edge_info

    def get_edge_weights(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return self._get_edge_info("weight")
    
    def get_edge_colours(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return self._get_edge_info("colour")
    
    ### TEMP ###
    def draw_shape(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        # Creates White Canvas
        W = 800
        size = W, W, 3
        image = np.ones(size) 
        # Get Graph Details
        dic = self.get_vertex_positions()
        graph = {0: dic, 1: self}
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


class Polygon(Shape):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__()
        self.can_lattice = self._get_lattice_state()
    
    def generate_polygon(self, vertex_pos, shape_name, vectors):
        """
        IMPLEMENT DOCUMENTATION
        """
        edge_list = []
        for k in range(len(vectors)):
            vertex_dict = self.get_vertex_positions()
            found = False
            for key in vertex_dict.keys():
                edge_length = round(sqrt(abs((vertex_dict[key][0])**2 + (vertex_dict[key][1])**2)), 3)
                if (vertex_pos[0] - vertex_dict[key][0])**2 + (vertex_pos[1] - vertex_dict[key][1])**2 <= (edge_length/100)**2: ## Change to edge_length!!
                    edge_list.append(key)
                    found = True
            if found == False:
                self.add_vertex(shape_name + k/10, vertex_pos)
                edge_list.append(shape_name + k/10)
            vertex_pos = add_vectors(vertex_pos, vectors[k])
        for e in range(len(vectors) - 1):
            self.add_edge(edge_list[e], edge_list[e + 1])
        self.add_edge(edge_list[len(vectors) - 1], edge_list[0])

    def generate_shapes_lattice(self, layers):
        """
        IMPLEMENT DOCUMENTATION
        """
        if self.can_lattice:
            chg_vectors = self._generate_change_vectors()
            return self._generate_lattice_graph(layers, chg_vectors)
            
        else:
            print("LATTICE NOT POSSIBLE WITH THIS SHAPE")

    @abc.abstractmethod
    def _generate_change_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return

    @abc.abstractmethod
    def _generate_lattice_graph(self, layer, chg_vectors):
        """
        IMPLEMENT DOCUMENTATION
        """
        return

    @abc.abstractmethod
    def _get_lattice_state(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return


class RegularPolygon(Polygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, sides, edge_length, centre, rotation):
        """
        IMPLEMENT DOCUMENTATION
        """
        self.sides = sides
        self.edge_length = edge_length
        self.centre = centre
        self.rotation = rotation

        # Error Handling for parameters.
        if self.sides < 3:
            raise ValueError("Argument 'sides' = {self.sides}. A regular polygon have at least 3 sides.".format(self=self))
        elif self.edge_length < 0:
            raise ValueError("Argument 'edge_length' = {self.edge_length}. Edges cannot be of negative length.".format(self=self))
        elif not check_if_coord(self.centre):
            raise ValueError("Argument 'centre' = {self.centre}. Centre must be a cartesian coordinate.".format(self=self))
        elif self.rotation < - 360 and self.rotation > 360:
            raise ValueError("Argument 'rotation' = {self.rotation}. Shape rotations should be within range (-360, 360).".format(self=self))

        # Generates Regular Polygon with input data...
        self._set_radius_info()
        super().__init__()

        self.polygon_vectors = self._generate_polygon_vectors(self.sides)
        start_pos = add_vectors(self.centre, self.radius_vec)
        self.generate_polygon(start_pos, 0, self.polygon_vectors)

    def _set_radius_info(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        self.intAngle = round(((self.sides - 2)*180)/self.sides, 3)
        self.theta = 180 - self.intAngle
        self.radius = round((self.edge_length)/(2*sin(radians(self.theta/2))), 3)
        self.radius_vec = change_to_cart_vector((self.radius, self.rotation))
    
    def _generate_polygon_vectors(self, sides):
        """
        IMPLEMENT DOCUMENTATION
        """
        vectors = {}
        for i in range(self.sides):
            angle = i*self.theta + (180 - (self.intAngle/2)) + self.rotation
            vectors[i] = change_to_cart_vector((self.edge_length, angle))
        return vectors
    
    def _get_lattice_state(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        lattice_test = 360/self.intAngle
        return lattice_test.is_integer()
    
    

################## DEFAULT REGULAR POLYGON ######################


class Triangle(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edge_length = 1, centre = (0, 0), rotation = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(3, edge_length, centre, rotation)

    def _generate_change_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        base_vectors = {}
        for i in range(2*self.sides):
            base_vectors[i] = (self.edge_length, 30 + (i + 1)*self.intAngle + self.rotation)
        change_vectors = change_to_cart_dict(base_vectors)
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

        lattice = Lattice(3, layers)
        shape = 0
        origin_vertex = add_vectors(self.centre, self.radius_vec)
        for layer in range(layers):
            if layer == 0:
                lattice.generate_polygon(origin_vertex, shape, cart_one)
            else:
                if layer % 2 == 0: # Odd Layers
                    origin_vertex = add_vectors(origin_vertex, chg_vectors[5])
                    origin_vertex = add_vectors(origin_vertex, chg_vectors[4])
                    vertex_pos = origin_vertex
                    for i in range(3):
                        for _ in range(int(layer/2)):
                            shape += 1
                            lattice.generate_polygon(vertex_pos, shape, cart_one)
                            vertex_pos = add_vectors(vertex_pos, chg_vectors[2*i])
                        for _ in range(int(layer/2)):
                            shape += 1
                            lattice.generate_polygon(vertex_pos, shape, cart_one)
                            vertex_pos = add_vectors(vertex_pos, chg_vectors[(2*i) + 1])    
                else: # Even Layers
                    origin_vertex = add_vectors(origin_vertex, chg_vectors[2])
                    vertex_pos = origin_vertex
                    for i in range(3):
                        for _ in range(int((layer + 1)/2)):
                            shape += 1
                            lattice.generate_polygon(vertex_pos, shape, cart_two)
                            vertex_pos = add_vectors(vertex_pos, chg_vectors[2*i])
                        for _ in range(int((layer + 1)/2) - 1):
                            shape += 1
                            lattice.generate_polygon(vertex_pos, shape, cart_two)
                            vertex_pos = add_vectors(vertex_pos, chg_vectors[(2*i) + 1])
        return lattice


class Square(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edge_length = 1, centre = (0, 0), rotation = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(4, edge_length, centre, rotation)

    def _generate_change_vectors(self): 
        """
        IMPLEMENT DOCUMENTATION
        """
        return self.polygon_vectors

    def _generate_lattice_graph(self, layers, chg_vectors):
        """
        IMPLEMENT 
        """
        lattice = Lattice(4, layers)

        even_numbers = list(range(0, 2*layers, 2))
        shape = 0
        for layer in range(layers):
            radius_vec = (round((layer*2*self.radius_vec[0]) + self.radius_vec[0], 3), round((layer*2*self.radius_vec[1]) + self.radius_vec[1], 3))
            start_vertex_pos = add_vectors(self.centre, radius_vec)
            if layer == 0:
                lattice.generate_polygon(start_vertex_pos, shape, chg_vectors)
                shape += 1
            else:
                for i in range(self.sides):
                    for _ in range(even_numbers[layer]):
                        lattice.generate_polygon(start_vertex_pos, shape, chg_vectors)
                        start_vertex_pos = add_vectors(start_vertex_pos, chg_vectors[i])
                        shape += 1
        return lattice

class Pentagon(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edge_length = 1, centre = (0, 0), rotation = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(5, edge_length, centre, rotation)


class Hexagon(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edge_length = 1, centre = (0, 0), rotation = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(6, edge_length, centre, rotation)

    def _generate_change_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        edgeLengthPlus = 1.5*self.edge_length
        halfHexHeight = round(sqrt(0.75*((self.edge_length)**2)), 2)
        vector_length = round(sqrt(edgeLengthPlus**2 + halfHexHeight**2), 2)
        base_vector = {}
        for i in range(self.sides):
            base_vector[i] = (vector_length, i*(self.theta) + self.theta/2 + self.rotation)
        change_vectors = change_to_cart_dict(base_vector)
        return change_vectors
    
    def _generate_lattice_graph(self, layers, chg_vectors):
        """
        IMPLEMENT 
        """
        lattice = Lattice(6, layers)
        
        shape = 1
        for layer in range(layers):
            if layer == 0:
                start_vertex_pos = add_vectors(self.centre, self.radius_vec)
                lattice.generate_polygon(start_vertex_pos, 0, self.polygon_vectors)
            else:
                start_vertex_pos = add_vectors(start_vertex_pos, chg_vectors[4])
                lattice.generate_polygon(start_vertex_pos, shape, self.polygon_vectors)
                for i in range(self.sides):
                    for _ in range(layer):
                        shape += 1
                        start_vertex_pos = add_vectors(start_vertex_pos, chg_vectors[i])
                        lattice.generate_polygon(start_vertex_pos, shape, self.polygon_vectors)
        return lattice

class Septagon(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edge_length = 1, centre = (0, 0), rotation = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(7, edge_length, centre, rotation)


class Octagon(RegularPolygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, edge_length = 1, centre = (0, 0), rotation = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__(8, edge_length, centre, rotation)


############################################################################################


class NonRegularPolygon(Polygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, start_point, rotation):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__()
        self.start_point = start_point
        self.rotation = rotation
        self.polygon_vectors = self._generate_polygon_vectors()

        self.generate_polygon(start_point, 0, self.polygon_vectors)
    
    # Future Method For Non-Regs
    def get_centroid(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return
    
    @abc.abstractmethod
    def _generate_polygon_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return

class _FourSided(Polygon):
    """
    IMPLEMENT DOCUMENTATION
    """    
    def _generate_lattice_graph(self, layers, chg_vectors): 
        """
        IMPLEMENT DOCUMENTATION
        """
        lattice = Lattice(4, layers)
        
        radius_vec = add_vectors(chg_vectors[2], chg_vectors[3])

        even_numbers = list(range(0, 2*layers, 2))
        shape = 0
        for layer in range(layers):
            if layer == 0:
                lattice.generate_polygon(self.start_point, shape, chg_vectors)
                shape += 1
            else:
                radius_vec = (round((layer*radius_vec[0]), 3), round((layer*radius_vec[1]), 3))
                start_vertex_pos = add_vectors(self.start_point, radius_vec)
                for i in range(4):
                    for _ in range(even_numbers[layer]):
                        lattice.generate_polygon(start_vertex_pos, shape, chg_vectors)
                        start_vertex_pos = add_vectors(start_vertex_pos, chg_vectors[i])
                        shape += 1
        return lattice

class Rectangle(NonRegularPolygon, _FourSided):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, width, height, start_point = (0, 0), rotation = 0):
        """
        IMPLEMENT DOCUMENTATION
        """
        self.height = height
        self.width = width
        super().__init__(start_point, rotation)
    
    def _generate_change_vectors(self): 
        """
        IMPLEMENT DOCUMENTATION
        """
        return self.polygon_vectors

    def _generate_polygon_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        vectors = {}
        for i in range(0, 4, 2):
            height_polar = (self.height, (i + 1)*90 + self.rotation)
            width_polar = (self.width, (i + 2)*90 + self.rotation)
            vectors[i] = height_polar
            vectors[i + 1] = width_polar
        return change_to_cart_dict(vectors)
    
    def _get_lattice_state(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return True
    

class Parallelogram(NonRegularPolygon, _FourSided):
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

    def _generate_change_vectors(self): 
        """
        IMPLEMENT DOCUMENTATION
        """
        return self.polygon_vectors

    def _generate_polygon_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        vectors = {}
        for i in range(0, 4, 2):
            height_polar = (self.height, (i + 1)*90 + self.angle + self.rotation)
            width_polar = (self.width, (i + 2)*90 + self.rotation)
            vectors[i] = height_polar
            vectors[i + 1] = width_polar
        return change_to_cart_dict(vectors)
    
    def _get_lattice_state(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        return True

        
class Lattice(Polygon):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, sides, layers):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__()
        self.sides = sides
        self.layers = layers
    
    def get_shape_num(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        if self.sides % 3 == 0:
            return int(1 + self.sides*(self.layers*(self.layers - 1)/2))
        elif self.sides % 4 == 0:
            return int((1 + 2*(self.layers - 1))**2)

