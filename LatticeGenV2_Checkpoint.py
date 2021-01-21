import networkx as nx
import abc
import cv2 as cv
import numpy as np
from math import sin, cos, radians, sqrt

from LatticeGen_Funcs import my_filled_circle, my_line, change_vector, dict_search

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

    # TEMP - need to clean up open cv file stuff and re-work postion finding.
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
        self.rotation = radians(rotation)

        # Error handling if a certain rules not met.
        if self.sides < 3:
            raise ValueError("Argument 'sides' = {self.sides}. A regular polygon have at least 3 sides.".format(self=self))
        elif self.edgeLength < 0:
            raise ValueError("Argument 'edgeLength' = {self.edgeLength}. Edges cannot be of negative length.".format(self=self))
        elif self.rotation < - 360 and self.rotation > 360:
            raise ValueError("Argument 'rotation' = {self.rotation}. Shape rotations should be within range (-360, 360).".format(self=self))
        
        self.intAngle = round(((self.sides - 2)*180)/self.sides, 3)
        self.theta = radians(180 - self.intAngle)
        self.radius = round((self.edgeLength/2)/sin(self.theta/2 ), 3)
        self.generate_shape()

        self.can_lattice = self.get_lattice_state()

    # Generate shape for Regular Polygons
    def generate_shape(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        pos = []
        for i in range(self.sides):
            x = self.radius*cos(i*self.theta + self.rotation)
            y = self.radius*sin(i*self.theta + self.rotation)
            coord = [round(x, 3), round(y, 3)]
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
    
    def _generate_lattice_graph(self, posList, shapeNum):
        """
        IMPLEMENT DOCUMENTATION
        """
        position = posList
        shape_num = shapeNum
        lattice = nx.Graph()
        for shape in range(shape_num):
            H = nx.Graph()
            for i in range(self.sides):
                H.add_node(shape + i / 10, pos = position[shape][i])  # add nodes to H
            node_list = list(H.nodes)
            for j in range(self.sides - 1):
                H.add_edge(node_list[j], node_list[j + 1])  # add edges to H
            H.add_edge(node_list[0], node_list[self.sides - 1])
            lattice_shape_dict = nx.get_node_attributes(lattice, "pos")
            H_shape_dict = nx.get_node_attributes(H, "pos")
            for v in H_shape_dict:
                v_neighbors = list(H.adj[v])
                search_pos = H_shape_dict.get(v)
                if search_pos in lattice_shape_dict.values():
                    replacement = dict_search(search_pos, lattice_shape_dict)  # finds the preexisting node with same position
                    H.remove_node(v)  # removes dupe node and all adjacent edges
                    H.add_node(replacement, pos = search_pos)  # adds replacement with same position
                    for e in v_neighbors:
                        H.add_edge(replacement, e)  # re establishes edges with v's original neighbors
            lattice = nx.compose(lattice, H)
            lattice_shape_dict = nx.get_node_attributes(lattice, "pos")

        return lattice


    def generate_lattice(self, layers):
        """
        IMPLEMENT DOCUMENTATION
        """
        if self.can_lattice:
            chg_vectors = self._generate_change_vectors()
            position = self._generate_lattice_positions(layers, chg_vectors)
            shape_num = self._get_shape_num(layers)
            self.lattice = self._generate_lattice_graph(position, shape_num)
            return self.lattice
        else:
            print("LATTICE NOT POSSIBLE WITH THIS SHAPE")
    
    @abc.abstractmethod
    def _generate_lattice_positions(self, layers, chg_vectors):
        pass

    @abc.abstractmethod
    def _get_shape_num(self, layers):
        pass
    
    @abc.abstractmethod
    def _generate_change_vectors(self):
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
        return (1 + (layers - 1)*2)**2
    
    def _generate_change_vectors(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        change_vectors = {}
        for side in range(self.sides - 1):
            x_vec = self.nodes.data()[side + 1]["pos"][0] - self.nodes.data()[side]["pos"][0]
            y_vec = self.nodes.data()[side + 1]["pos"][1] - self.nodes.data()[side]["pos"][1]
            change_vectors[side] = (x_vec, y_vec)
        x_vec = self.nodes.data()[0]["pos"][0] - self.nodes.data()[self.sides - 1]["pos"][0]
        y_vec = self.nodes.data()[0]["pos"][1] - self.nodes.data()[self.sides - 1]["pos"][1]
        change_vectors[self.sides - 1] = (x_vec, y_vec)
        return change_vectors
    
    def _generate_lattice_positions(self, layers, chg_vectors):
        """
        IMPLEMENT DOCUMENTATION
        """
        centre = []
        for node in self.nodes.data():
            centre.append(node[1]["pos"])
        layer_list = list(range(layers))
        even_numbers = list(range(0, (layers*2), 2))
        self.vector = (2*round(self.radius*cos(self.rotation), 3), 2*round(self.radius*sin(self.rotation), 3))
        position = []
        for layer in layer_list:
            if layer == 0:
                position.append(centre)
            else:
                layer_chg_vec = tuple([layer * x for x in self.vector])
                shape_pos = change_vector(centre, layer_chg_vec, self.sides)
                position.append(shape_pos)
                for i in range(self.sides - 1):
                    for _ in range(even_numbers[layer]):
                        shape_pos = change_vector(shape_pos, chg_vectors[i], self.sides)
                        position.append(shape_pos)
                for _ in range(even_numbers[layer] - 1):
                    shape_pos = change_vector(shape_pos, chg_vectors[self.sides - 1], self.sides)
                    position.append(shape_pos)
        return position

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
        halfHexHeight = sqrt(self.edgeLength**2 - (self.edgeLength/2)**2)
        change_vectors = {
            0: (- edgeLengthPlus, halfHexHeight),
            1: (- edgeLengthPlus, - halfHexHeight),
            2: (0, - 2*halfHexHeight),
            3: (edgeLengthPlus, - halfHexHeight),
            4: (edgeLengthPlus, halfHexHeight),
            5: (0, 2*halfHexHeight),
        }
        return change_vectors
    
    def _generate_lattice_positions(self, layers, chg_vectors):
        """
        IMPLEMENT DOCUMENTATION
        """
        centre = []
        for node in self.nodes.data():
            centre.append(node[1]["pos"])

        layer_list = list(range(layers))
        position = []
        for layer in layer_list:
            if layer == 0:
                position.append(centre)
            else:
                layer_chg_vec = tuple([layer * x for x in chg_vectors[4]])
                shape_pos = change_vector(centre, layer_chg_vec, self.sides)
                position.append(shape_pos)
                for i in range(self.sides - 1):
                    for _ in range(layer):
                        shape_pos = change_vector(shape_pos, chg_vectors[i], self.sides)
                        position.append(shape_pos)
                for _ in range(layer - 1):
                    shape_pos = change_vector(shape_pos, chg_vectors[self.sides - 1], self.sides)
                    position.append(shape_pos)
        return position
    


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
        super().__init__(7, edgeLength, rotation)



test = Hexagon(1)
testLat = test.generate_lattice(10)
test.draw_shape(testLat)