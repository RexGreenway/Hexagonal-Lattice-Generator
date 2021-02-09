import abc
import cv2 as cv
import numpy as np
from math import sqrt, sin, cos, radians
from exception import *
from functions import add_vectors, change_to_cart_vector, check_if_coord, my_filled_circle, my_line, is_positive_int, is_supported_colour, change_to_cart_list

## Potential Library Name: 'polylat', or 'polylatlib'

# Temp Colour List
colours = ["black", "red", "green", "blue", "yellow", "orange", "purple"]

### SHAPE (Parent Base Class) ###
class Shape():
    """
    Shape is the base parent class for all shape objects. This class implements the basic features
    and methods of vertices and edges for all shapes.

    Attributes
    ----------
    .vertices :  The list of all vertex names.
    .vertices_info : The list of vertex tuples of vertices along with their associated property
        dictionary. This dictionary contains the vertex properties position, size, and colour.
    .edges :  The list of edges. Edges are stored as 2-tuples of the vertices at either end of
        the edge.
    .edge_info : The list of tuples of edges along with their associated information dictionary.
        This dictionary contains the edge weight and colour.
    
    Example
    -------
    >>> ADD EXAMPLE

    Notes
    -----
    The shape class includes all the methods related specifically to vertices and edges. Through
    these methods the shape can be built piece-meal with the addition of vertices and edges to the
    shape object, as well as be used to update vertex information (using the '.update' methods),
    or retrieve a vertex's, or edge's, specific property dictionary (using the '.get' methods).

    The final method of the shape object (currently) utilises the OpenCV library to create and
    canvas and draw the created shape.
    """
    def __init__(self):
        """
        Initialise a Shape object to be populated with vertices and edges.

        Example
        -------
        >>> A = Shape()
        >>> for i in range(5):
        >>>     A.add_vertex(i) # adding veritces 0 through 4 to A.
        >>> A.add_edge(0, 1)
        >>> A.add_edge(1, 8, 4)
        >>> print(A.vertices)
        [0, 1, 2, 3, 4, 8]
        >>> print(A.edges_info)
        [((0, 1), {weight: 1, colour: "black"}), ((1, 8), {weight: 4, colour: "black"})]

        Notes
        -----
        When initialised a Shape is an empty object with the capacity for the addition of vertices
        and edges.
        """
        self.vertices = []
        self.vertices_info = []
        self.edges = []
        self.edges_info = []
    
    def __str__(self):
        """
        Returns the type and a summary of the shape.

        Returns
        -------
        info : string
            Basic information of the shape object. Indicates the shape type, number of verticies,
            and number of sides.

        Example
        -------
        >>> A = Shape()
        >>> for in in range(5):
        >>>     A.add_edge(i, i + 1)
        >>> print(A)
        Shape:
        - Num. of Vertices: 6,
        - Num. of Edges: 5

        Notes
        -----
        ADD NOTES
        """
        return (
            f"""
            Type : {type(self).__name__}
            Number of Vertices : {len(self.vertices)}
            Number of Edges : {len(self.edges)}
            """
        )

    def __len__(self):
        """
        Returns the number of edges (i.e number of sides) in the shape. Use: 'len(A)'.

        Returns
        -------
        sides : int
            Number of edges in the shape.

        Example
        -------
        >>> A = Shape()
        >>> for in in range(5):
        >>>     A.add_edge(i, i + 1)
        >>> print(len(A))
        5
        """
        return len(self.edges)
    
    def __contains__(self, a):
        """
        Returns True if a vertex or edge exists in the shape, False otherwise.

        Parameters
        ----------
        a : vertex or edge,
            A vertex or edge element that may be contained in the shape.

        Returns
        -------
        boolean
            True if 'a' is in the shape, False if not.

        Example
        -------
        >>> A = EquilateralTriangle()
        >>> ("0-0", "0-1") in A
        True

        Notes
        -----
        ADD NOTES
        """
        # First Checks if input could be an edge
        if type(a) == tuple and len(a) == 2:
            # checks both edge directions
            for edge in [a, (a[1], a[0])]:
                if edge in self.edges:
                    return True
        # Otherwise checks against vertices
        else:
            try:
                return a in self.vertices
            except TypeError:
                return False

    def add_vertex(self, vertex_for_adding, position = None, size: int = 1, colour = "black"):
        """
        Adds a desired vertex to the shape, with associated properties; positon, size, and colour. 

        Parameters
        ----------
        vertex_for_adding : vertex,
            The desired name for a vertex in the shape. These can be strings, numbers, or
            collections.
        position : (x, y) - 2D Cartesian Coordinate, Default = None, optional
            The desired position for the vertex in the form of a coordinate 2-tuple. New vertices
            have no postion by deafult allowing for the creation of a graph-like object.
        size : int, Default = 1, optional
            Size property to be ustilised upon drawing of the shape.
        colour : colour, Default = "black", optional
            Colour property to be utilisied upon drawing of the shape. Colour can be chosen from
            list of options; black, red, green, blue, yellow, orange, purple, ...

        Example
        -------
        >>> A = Shape()
        >>> A.add_vertex(1) # 'Abstract' vertex called '1' with no position.
        >>> A.add_vertex("Hello", (2, 3))   # A vertex called 'Hello' at position (2, 3).
        >>> A.add_vertex("example", colour = "red")
        >>> print(A.vertices)
        [1, "Hello", "example"]

        Notes
        -----
        A vertex is a point in space that can exist independently, or as the end of an 
        edge/ multiple edges. You cannot have multiple vertices of the same name, though you can
        have multiple vertices occupying the same position. Vertex properties are its position,
        size, and colour.
        
        If initialised with no position the vertex can be considered an 'abstract' vertex with
        position = None. This vertex is more akin to a node in a graph-like object and can still be
        utilisied in the creation of edges resulting in a shape with no set strucutre except for
        defined edges and vertices.

        When initialised with a position the vertex becomes a recognisable shape in the R x R 
        Cartesian space with an x and y position. This position can also be imagined as the vector
        from the origin to the point of the vertex.

        Size and colour are utilisied in the drawing of the shape with size indicating the radius
        of the circle drawn at the vertex point. Colour is self-explanatory.
        """
        # Checks vertex does not already exist
        if vertex_for_adding not in self.vertices:
            # Checks position of vertex is Cartesian coord. or None
            if not check_if_coord(position) and position != None:
                raise PolyLatNotCart(position)
            elif not is_positive_int(size):
                raise PolyLatNotPosInt(size)
            elif not is_supported_colour(colour):
                raise PolyLatNotColour(colour)
            
            info = {
                "position": position,
                "size": size,
                "colour": colour
            }
            self.vertices.append(vertex_for_adding)
            self.vertices_info.append((vertex_for_adding, info))
        else:
            ### change this to update system????
            raise PolyLatError(f"Vertex '{vertex_for_adding}' already exists.")

    def update(self, item_for_update, prop, value):
        """
        Updates the desired property for a given item, either a vertex or an edge.

        See Also
        --------
        update_vertex, update_vertex_position, update_vertex_size, update_vertex_colour,
        update_edge, update_edge_weight, update_edge_colour

        Parameters
        ----------
        item_for_update : vertex or edge
            A vertex or edge to have the desired property updated.
        prop : vertex or edge property
            Vertex property's are "position", "size", or "colour". Edge property's are "weight", or
            "colour".
        value : property dependent
            The new value to be inserted into the desired property for the given vertex.
        
        Examples
        --------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        if item_for_update in self:
            # Check if item is edge
            if type(item_for_update) == tuple:
                self.update_edge(item_for_update, prop, value)
            # Else the item is a vertex
            else:
                self.update_vertex(item_for_update, prop, value)
        else:
            raise PolyLatNotExist(item_for_update)


    def update_vertex(self, vertex_for_update, prop, value):
        """
        Updates the desired property for a given vertex.

        Parameters
        ----------
        vertex_for_update : vertex
            A prexisting vertex in the shape to be updated.
        property : "position", "size", or "colour"
            The desired vertex property for update.
        value : property dependent value
            New value to be inserted into vertex information dictionary for desired attribute.

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        # Checks vertex existence
        if vertex_for_update in self.vertices:
            # Method selector
            try:
                method_name = "update_vertex_" + prop
                method = getattr(self, method_name)
                method(vertex_for_update, value)
            except AttributeError:
                raise PolyLatNotProp(prop)
        else:
            raise PolyLatNotExist(vertex_for_update)
    
    def update_vertex_position(self, vertex_for_update, value):
        """
        Updates the position for a given vertex.

        Parameters
        ----------
        vertex_for_update : vertex
            A prexisting vertex in the shape to be updated.
        value : (x, y) - 2D Cartesian Coordinate
            New value to be inserted into vertex information dictionary for position.

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        if vertex_for_update in self.vertices:
            if check_if_coord(value):
                index = self.vertices.index(vertex_for_update)
                self.vertices_info[index][1]["position"] = value
            else:
                raise PolyLatNotCart(value)
        else:
            raise PolyLatNotExist(vertex_for_update)
    
    def update_vertex_size(self, vertex_for_update, value):
        """
        Updates the size for a given vertex.

        Parameters
        ----------
        vertex_for_update : vertex
            A prexisting vertex in the shape to be updated.
        value : int > 0
            New value to be inserted into vertex information dictionary for size.

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        if vertex_for_update in self.vertices:
            if is_positive_int(value):
                index = self.vertices.index(vertex_for_update)
                self.vertices_info[index][1]["size"] = value
            else:
                raise PolyLatNotPosInt(value)
        else:
            raise PolyLatNotExist(vertex_for_update)
    
    def update_vertex_colour(self, vertex_for_update, value):
        """
        Updates the colour for a given vertex.

        Parameters
        ----------
        vertex_for_update : vertex
            A prexisting vertex in the shape to be updated.
        value : colour
            New value to be inserted into vertex information dictionary for colour.

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        if vertex_for_update in self.vertices:
            if is_supported_colour(value):
                index = self.vertices.index(vertex_for_update)
                self.vertices_info[index][1]["colour"] = value
            else:
                raise PolyLatNotColour(value)
        else:
            raise PolyLatNotExist(vertex_for_update)
    
    def get_vertex_info(self, desired_info):
        """
        Returns a specific property dictionary for all vertices.

        Parameters
        ----------
        desired_info : "position", "size", or "colour"
            Desired property to return property dictionary for all vertices.
        
        Returns
        -------
        vertex_info : dictionary
            Property dictionary with vertices as keys, and the desired property ('deired_info')
            as values.
        
        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        try:
            vertex_info = {}
            for vertex in self.vertices_info:
                vertex_info[vertex[0]] = vertex[1][desired_info]
            return vertex_info
        except:
            raise PolyLatNotExist(desired_info)

    def get_vertex_positions(self):
        """
        Returns the property dictionary of vertex positions.

        Returns
        -------
        vertex_info : dictionary
            Position dictionary for all vertices in the shape. The vertices as keys and their
            positions as the values.
        
        Example
        -------
        >>> A = Shape()
        >>> for i in range(5):
        >>>     A.add_vertex(i, (i + 1, i + 2))
        >>> A.get_vertex_positions()
        {0: (1, 2), 1: (2, 3), 2: (3, 4), 3: (4, 5), 4: (5, 6)}

        Notes
        -----
        This method returns a very usable collection of all vertices in the shape with their
        associated position.
        """
        return self.get_vertex_info("position")

    def get_vertex_sizes(self):
        """
        Returns the property dictionary of vertex sizes.

        Returns
        -------
        vertex_info : dictionary
            Size dictionary for all vertices in the shape. The vertices as keys and their
            sizes as the values.
        
        Example
        -------
        >>> A = Shape()
        >>> for i in range(5):
        >>>     A.add_vertex(i, size = (i + 1)*10)
        >>> A.get_vertex_sizes()
        {0: 10, 1: 20, 2: 30, 3: 40, 4: 50}

        Notes
        -----
        This method returns a very usable collection of all vertices in the shape with their
        associated size.
        """
        return self.get_vertex_info("size")
    
    def get_vertex_colours(self):
        """
        Gets the property dictionary of vertex colours.

        Returns
        -------
        vertex_info : dictionary
            Colour dictionary for all vertices in the shape. The vertices as keys and their
            colours as the values.
        
        Example
        -------
        >>> A = Shape()
        >>> for i in range(5):
        >>>     A.add_vertex(i, colour = colours[i])
        >>> A.get_vertex_colours()
        {0: "black", 1: "red", 2: "green", 3: "blue", 4: "yellow"}

        Notes
        -----
        This method returns a very usable collection of all vertices in the shape with their
        associated colour.
        """
        return self.get_vertex_info("colour")

    def add_edge(self, vertex_one, vertex_two, weight = 1, colour = "black"):
        """
        Adds a desired edge to the shape between 2 vertices, with associated properties; weight and
        colour.

        Parameters
        ----------
        vertex_one : vertex
            The vertex for the one end of the edge.
        vertex_two : vertex
            The vertex name for the other end of the edge. 
        weight : int > 0, Default = 1, optional
            Weight property to be utilisied upon drawing of the shape.
        colour : colour, Default = "black", optional
            Colour property to be utilisied upon drawing of the shape. Colour can be chosen from
            list of options; black, red, green, blue, yellow, orange, purple, ...
        
        Example
        -------
        >>> A = Shape()
        >>> A.add_edge(1, 2) # Adding edge between to new vetrices, 1, and 2.
        >>> A.add_edge("Hello", "World", 3) # An edge between 'Hello' and 'World' with weight 3.
        >>> A.add_edge("Hello", "xmpl", colour = "red") # Establishing edge between exsiting vertex "Hello" and new vertex "xmpl".
        >>> print(A.edges)
        [(1, 2), ("Hello", "World"), ("Hello", "xmpl")]

        Notes
        -----
        Edges are a connecting line between two vertices and are stored as a tuple of these two
        defining vertex ends. You cannot have multiple edges between the same two vertices and thus
        edges are uniquely defined by their vertex pair, this also means that (a, b) = (b, a). Edge
        properies are weight and size. Weight references the 'thickness' of the edge line and colour
        is self-explanatory. These properties utilised in the drawing of shapes. 

        Vertices not pre-exsiting within the shape are automatically generated and added with no 
        position and default size and colour.
        """
        # Checks if edge (in either direction) pre-exists
        if (vertex_one, vertex_two) not in self:
            self.edges.append((vertex_one, vertex_two))
            info = {
                "weight": weight,
                "colour": colour
            }
            self.edges_info.append((vertex_one, vertex_two, info))
            # Adds new vertices if needed
            for vertex in (vertex_one, vertex_two):
                if vertex not in self.vertices:
                    self.add_vertex(vertex)
        else:
            raise PolyLatError(f"Edge '{(vertex_one, vertex_two)}' already exists in the shape.")
    
    def update_edge(self, edge_for_update, prop, value):
        """
        Updates a desired property for a specific edge.

        Parameters
        ----------
        edge_for_update : 2-tuple, vertex pair
            A prexisting edge in the shape to be updated.
        property: "weight" or "colour"
            The desired edge property for update.
        value: propery dependent value
            New value to be inserted into edge information dictionary for desired attribute.

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        # Checks existence of edge in shape
        if edge_for_update in self:
            # Method selector
            try:
                method_name = "update_edge_" + prop
                method = getattr(self, method_name)
                method(edge_for_update, value)
            except AttributeError:
                raise PolyLatNotProp(prop)
        else:
            raise PolyLatError(f"'{edge_for_update}' does not exist.")

    def update_edge_weight(self, edge_for_update, value):
        """
        Updates the weight for a specific edge.

        Parameters
        ----------
        edge_for_update : 2-tuple, vertex pair
            A prexisting edge in the shape to be updated.
        value: int > 0
            New value to be inserted into edge information dictionary for weight.

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        if is_positive_int(value):
            if edge_for_update in self.edges:
                index = self.edges.index(edge_for_update)
            elif (edge_for_update[1], edge_for_update[0]) in self.edges:
                index = self.edges.index((edge_for_update[1], edge_for_update[0]))
            else:
                raise PolyLatNotExist(edge_for_update)
            self.edges_info[index][2]["weight"] = value
        else:
            raise PolyLatNotPosInt(value)
    
    def update_edge_colour(self, edge_for_update, value):
        """
        Updates the colour for a specific edge.

        Parameters
        ----------
        edge_for_update : 2-tuple, vertex pair
            A prexisting edge in the shape to be updated.
        value: colour
            New value to be inserted into edge information dictionary for colour.

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        if is_supported_colour(value):
            if edge_for_update in self.edges:
                index = self.edges.index(edge_for_update)
            elif (edge_for_update[1], edge_for_update[0]) in self.edges:
                index = self.edges.index((edge_for_update[1], edge_for_update[0]))
            else:
                raise PolyLatNotExist(edge_for_update)
            self.edges_info[index][2]["colour"] = value
        else:
            raise PolyLatNotColour(value)

    def get_edge_info(self, desired_info):
        """
        Returns a specific property dictionary for all edges in the shape.

        Parameters
        ----------
        desired_info : "weight" or "colour"
            Desired property to return information about.
        
        Returns
        -------
        edge_info : dictionary
            Property dictionary with edges as keys, and the desired property ('desired_info') as
            values.

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES

        """
        try:
            edge_info = {}
            for edge in self.edges_info:
                edge_info[(edge[0], edge[1])] = edge[2][desired_info]
            return edge_info
        except:
            raise PolyLatError(f"'{desired_info}' is not an edge property.")

    def get_edge_weights(self):
        """
        Returns the property dictionary of edge weights.

        Returns
        -------
        edge_info : dictionary
            Weight dictionary for all edges in the shape. The edges as keys and their weights as
            the values
        
        Example
        -------
        >>> A = Shape()
        >>> for i in range(5):
        >>>     A.add_edge(i, i + 1, (i + 1)*10)
        >>> A.get_edge_weights()
        {(0, 1): 10, (1, 2): 20, (2, 3): 30, (3, 4): 40, (4, 5): 50}

        Notes
        -----
        This method returns a very usable collection of all edges in the shape with their
        associated weight.
        """
        return self.get_edge_info("weight")
    
    def get_edge_colours(self):
        """
        Returns the property dictionary of edge colours.

        Returns
        -------
        edge_info : dictionary
            Colour dictionary for all edges in the shape. The edges as keys and their colours as
            the values.
        
        Example
        -------
        >>> A = Shape()
        >>> for i in range(5):
        >>>     A.add_edge(i, i + 1, colour = colours[i])
        >>> A.get_vertex_colours()
        {(0, 1): "black", (1, 2): "red", (2, 3): "green", (3, 4): "blue", (4, 5): "yellow"}

        Notes
        -----
        This method returns a very usable collection of all edges in the shape with their
        associated colour.
        """
        return self.get_edge_info("colour")

    def get_edge_vectors(self):
        """
        Returns the vectors of the edges in the shape in the form of a dictionary.
        
        Returns
        -------
        edge_vectors : dictionary
            Dictionary with edges as keys and their vectors as values.

        Example
        -------
        >>> A = Shape()
        >>> for i in range(3):
        >>>     A.add_vertex(i, (i, i + (-1)**i)
        >>> A.add_edge(0, 1)
        >>> A.add_edge(1, 2)
        >>> A.add_edge(0, 2)
        >>> print(A.get_edge_vectors())
        {(0, 1): (1, -1), (1, 2): (1, 3), (0, 2): (2, 2)}
        
        Notes
        -----
        Edge vectors are the vectors from the first vertex in the edge to the second as the
        vertex pairs are stored. If needed, the vector in the opposite direction is simply the
        same vector with neagtive x, and y, values.
       
        This method calculates and returns the true edge vectors for all edge present within the
        shape. Calculation of these vectors from the property dictionaries is the prefered
        method to retrieve this information as vectors used for generation in child classes can
        be overwritten in some circumstances (i.e generate polygon automatically closes the shape
        if input vectors do not do so).
        """
        edge_vectors = {}
        for edge in self.edges:
            pos_one = self.get_vertex_positions()[edge[0]]
            pos_two = self.get_vertex_positions()[edge[1]]
            # Raises error upon any vertex with no position
            if pos_one == None or pos_two == None:
                raise TypeError("Edge vectors cannot be generated as one or more vertices in an edge do not have a position.")
            vector = (pos_two[0] - pos_one[0], pos_two[1] - pos_one[1])
            edge_vectors[edge] = vector
        return edge_vectors
    
    def get_edge_vector(self, edge):
        """
        Returns specific edge vector for a desired edge.

        Returns
        -------
        vector : 2-tuple
            Vector from the first vertex in the edge to the second.

        See Also
        --------
        get_edge_vectors
        
        Example
        -------
        >>> A = lg.Shape()
        >>> for i in range(3):
        >>>     A.add_vertex(i, (i, i + (-1)**i))
        >>> A.add_edge(0, 1)
        >>> A.add_edge(1, 2)
        >>> A.add_edge(0, 2)
        >>> print(A.get_edge_vector((2, 1)))    # Note reversed vertices still works.
        (1, 3)

        Notes
        -----
        ADD NOTES
        """
        for e in [edge, (edge[1], edge[0])]:
            if e in self.edges:
                return self.get_edge_vectors()[e]
        raise PolyLatNotExist(edge)


    def generate_shape(self, vertex_pos, shape_name, vectors):
        """
        Generates a named shape from a series of edge vectors staring at a given point.
        
        Parameters
        ----------
        vertex_pos : (x, y) - 2D Cartesian Coordinate
            Start position for the initial vertex in the polygon.
        shape_name : string, int, or float
            This is the overiding shape name dictating all the vertex names within the shape.
            Vertex names are of the form; 'shape_name-k', where k is number of the vertex.
        vectors : list
            This should be an ordered list of edge vectors. This method runs through the list in
            order to generate the polygon.

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        This method checks for pre-existence of vertices before adding new ones, i.e we cannot
        have multiple vetrices occupying the same position...
        """
        edge_list = []
        for k in range(len(vectors) + 1):
            vertex_dict = self.get_vertex_positions()
            found = False
            # Check if a vertex in within a small radius (1/100) to vector start,
            # If found choose existing vertex instead - this accounts for floating point error
            for key in vertex_dict.keys():
                if (vertex_pos[0] - vertex_dict[key][0])**2 + (vertex_pos[1] - vertex_dict[key][1])**2 <= (1/100)**2: ## Change to edge_length!!
                    edge_list.append(key)
                    found = True
                    break
            # Else create new vertex in that spot
            if found == False:
                self.add_vertex(str(shape_name) + "-" + str(k), vertex_pos)
                edge_list.append(str(shape_name) + "-" + str(k))
            # Move along next vector if not at end of vector list
            if k != len(vectors):
                vertex_pos = add_vectors(vertex_pos, vectors[k])
        for e in range(len(vectors)):
            if (edge_list[e], edge_list[e + 1]) not in self:
                self.add_edge(edge_list[e], edge_list[e + 1])
        
    ## TEMP ##
    def draw_shape(self):
        """
        Temporary draw_shape using OpenCV to view the results [Currently used for testing].
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


### POLYGON CLASS ###
class Polygon(Shape):
    """
    Polygon class to encapsulate the closed definition of polygons.

    Example
    -------
    >>> ADD EXAMPLE

    Notes
    -----
    A polygon is defined as a 2-dimensional closed shape with straight sides. The polygon class
    therefore implements methods that adhere to this definition as well as establishes the potential
    ability for a lattice to be generated from the polygon.

    Similar to its superclass, a polygon object can be built piece-meal through addition of vertices
    and edges however this does not ensure the required closed nature of a polygon. Instead, by 
    using 'generate polygon', the shape can be generated from a dictionary of vectors that describe
    the edges of the shape.
    
    Polygons can also potentially be organised into a regular repeated arrangement called a lattice.
    If this is possible for the polygon a series of change vectors (the vectors between iterations
    of the shapes in the lattice) can then be defined and the lattice can be generated. 

    """
    def __init__(self):
        """
        Initialises a Polygon object, inherits from Shape..
        
        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        super().__init__()

    def generate_lattice(self, layers, lat_type):
        """
        Generates the polygon's lattice in a given number of layers centred on the staring
        polygon. Uses the methods; 'generate_change_vectors' a 'generate_lattice_from_vectors'.

        Parameters
        ----------
        layers : int > 0
            The number of layers to be generated around the original polygon. If 1 is input
            the original shape is just generated.
        
        Returns
        -------
        lattice : Lattice class object specific to current generating shape.

        Example
        -------
        >>> ADD EXAMPLE

        Notes
        -----
        ADD NOTES
        """
        if self.get_lattice_state():
            if lat_type == "circular":
                return self.generate_lattice_circular(layers)
            elif lat_type == "stacked":
                return self.generate_lattice_stacked(layers)
            else:
                raise PolyLatNotProp(lat_type)  
        else:
            print("Lattice not possible with this shape.")


    @abc.abstractmethod
    def generate_lattice_stacked(self, layers):
        """
        Abstract method that generates and returns the stacked lattice for polygons. To be defined
        in child classes.
        """

    @abc.abstractmethod
    def generate_lattice_circular(self, layers):
        """
        Abstract method that generates and returns the circular lattice for polygons. To be defined
        in child classes.
        """

    @abc.abstractmethod
    def get_lattice_state(self):
        """
        Abstract method that returns whether or not a polygon can have a lattice generated from it.
        To be defined in child classes.
        """


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


############################################################################################

        
class Lattice(Shape):
    """
    IMPLEMENT DOCUMENTATION
    """
    def __init__(self, layers):
        """
        IMPLEMENT DOCUMENTATION
        """
        super().__init__()
        self.layers = layers
    
    def get_shape_num(self):
        """
        IMPLEMENT DOCUMENTATION
        """
        sides = len(self.edges)
        if sides % 3 == 0:
            return int(1 + sides*(self.layers*(self.layers - 1)/2))
        elif sides % 4 == 0:
            return int((1 + 2*(self.layers - 1))**2)