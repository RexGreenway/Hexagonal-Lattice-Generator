import abc
import cv2 as cv
import numpy as np
from math import sqrt, sin, cos, radians
from functions import add_vectors, change_to_cart_dict, change_to_cart_vector, check_if_coord, my_filled_circle, my_line

## Potential Library Name: 'polylat', or 'polylatlib'

# Temp Colour List
colours = ["black", "red", "green", "blue", "yellow", "orange", "purple"]

### SHAPE (Parent Base Class) ###
class Shape():
    """
    Shape is the base parent class for all shape objects. This class implements the basic features
    and methods of vertices and edges for all shapes. 
    
    Example
    -------
    >>> PUT EXAMPLE HERE!!!!!!

    Notes
    -----
    The shape class includes all the methods related specifically to vertices and edges. Through
    these methods the shape can be built piece-meal with the addition of vertices and edges to the
    shape object, as well as be used to update vertex information (using the '.update_' methods),
    or retrieve a vertex's, or edge's, specific property dictionary (using the '.get_' methods).

    The final method of the shape object (currently) utilises the OpenCV library to create and
    canvas and draw the created shape.
    """
    def __init__(self):
        """
        Initialise a Shape object to be populated with vertices and edges.

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
        Returns a logical summary of the shape.

        Returns
        -------
        info : string
            Basic information opf the shape object. Indicates the shape type, number of verticies,
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
        """
        return type(self).__name__ + f":\n- Num. of Vertices: {len(self.vertices)},\n- Num. of Edges: {len(self.edges)}.".format(self=self)

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

        Example
        -------
        >>> A = EquilateralTriangle()
        >>> ("0-0", "0-1") in A
        True
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
            if check_if_coord(position) or position == None:
                self.vertices.append(vertex_for_adding)
                info = {
                    "position": position,
                    "size": size,
                    "colour": colour
                }
                self.vertices_info.append((vertex_for_adding, info))
            else:
                raise ValueError("Input 'position' must be in the form of a cartesian coordinate")
        else:
            raise ValueError("This vertex already exists.")

    def _update_vertex_property(self, vertex_for_update, prop, value):
        """
        Private method for updating any of the vertex properties.

        Parameters
        ----------
        vertex_for_update : vertex
            A prexisting vertex in the shape to be updated.
        property : "position", "size", or "colour"
            The desired vertex property for update.
        value : property dependent value
            New value to be inserted into vertex information dictionary for desired attribute.
        """
        # Checks vertex existence
        try:
            index = self.vertices.index(vertex_for_update)
            self.vertices_info[index][1][prop] = value
        except:
            raise ValueError("The vertex entered does not exist.")
    
    def update_vertex_position(self, vertex_for_update, value):
        """
        Updates the vertex position.

        Parameters
        ----------
        vertex_for_update : vertex
            A prexisting vertex in the shape to be updated.
        value : (x, y) - 2D Cartesian Coordinate
            New position to be inserted into vertex's information dictionary.
        
        Example
        -------
        >>> A = Shape()
        >>> A.add_vertex("xmpl", (2, 3))
        >>> print(A.vertices_info)
        [("xmpl", {position: (2, 3), size: 1, colour: "black"})]
        >>> A.update_vertex_position("xmpl", (0, 0))    # move "xmpl" to the origin.
        >>> print(A.vertices_info)
        [("xmpl", {position: (0, 0), size: 1, colour: "black"})]

        Notes
        -----
        This method takes a prexisting vertex within the shape and proceeds to update its position
        property in the vertex's infomation dictionary.
        """
        # Checks if value input is a cartesian coordinate
        if check_if_coord(value):
            self._update_vertex_property(vertex_for_update, "position", value)
        else:
            raise ValueError(value, " - position should be a cartesian coordinate.")
    
    def update_vertex_size(self, vertex_for_update, value):
        """
        Updates the vertex size.

        Parameters
        ----------
        vertex_for_update : vertex
            A prexisting vertex in the shape to be updated.
        value : int > 0
            New size to be inserted into vertex's information dictionary.

        Example
        -------
        >>> A = Shape()
        >>> A.add_vertex("xmpl", (2, 3))
        >>> print(A.vertices_info)
        [("xmpl", {position: (2, 3), size: 1, colour: "black"})]
        >>> A.update_vertex_size("xmpl", 100)    # scale "xmpl" to size 100.
        >>> print(A.vertices_info)
        [("xmpl", {position: (2, 3), size: 100, colour: "black"})]
        
        Notes
        -----
        This method takes a prexisting vertex within the shape and proceeds to update its size
        property in the vertex's infomation dictionary.
        """
        # Checks if size value is a positive integer
        if type(value) == int and value > 0:
            self._update_vertex_property(vertex_for_update, "size", value)
        else:
            raise ValueError(value, " - size should be an integer.")

    def update_vertex_colour(self, vertex_for_update, value):
        """
        Updates the vertex colour.

        Parameters
        ----------
        vertex_for_update : vertex
            A prexisting vertex in the shape to be updated.
        value : colour
            New colour to be inserted into vertex's information dictionary.

        Example
        -------
        >>> A = Shape()
        >>> A.add_vertex("xmpl", (2, 3))
        >>> print(A.vertices_info)
        [("xmpl", {position: (2, 3), size: 1, colour: "black"})]
        >>> A.update_vertex_colour("xmpl", "green")    # change "xmpl" from black to green.
        >>> print(A.vertices_info)
        [("xmpl", {position: (2, 3), size: 1, colour: "green"})]
        
        Notes
        -----
        This method takes a prexisting vertex within the shape and proceeds to update its colour
        property in the vertex's infomation dictionary.
        """
        # Checks if value is a supported colour
        if value in colours:
            self._update_vertex_property(vertex_for_update, "colour", value)
        else:
            raise ValueError(value, " - not a supported colour.")

    def _get_vertex_info(self, desired_info):
        """
        Private method to get a specific property dictionary for all vertices.

        Parameters
        ----------
        desired_info : "position", "size", or "colour"
            Desired property to return property dictionary for all vertices.
        
        Returns
        -------
        vertex_info : dictionary
            Property dictionary with vertices as keys, and the desired property ('deired_info')
            as values.
        """
        vertex_info = {}
        for vertex in self.vertices_info:
            vertex_info[vertex[0]] = vertex[1][desired_info]
        return vertex_info

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
        return self._get_vertex_info("position")

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
        return self._get_vertex_info("size")
    
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
        return self._get_vertex_info("colour")

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
        >>> A.add_edge("Hello", "xmpl", colour = "red") # Establishing edge between exsiting
                                                        vertex "Hello" and new vertex "xmpl".
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
        if (vertex_one, vertex_two) not in self.edges and (vertex_two, vertex_one) not in self.edges:
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
        # Currently passed as usage in "generate_polygon" causes error raised to be thrown.
        # POTENTIAL FIX: make it not throw error in 'add' methods if pre-exist...?
        else:
            pass
    
    def _update_edge_property(self, edge_for_update, prop, value):
        """
        Private method for updating any of the edge properties.

        Parameters
        ----------
        edge_for_update : 2-tuple, vertex pair
            A prexisting edge in the shape to be updated.
        property: "weight" or "colour"
            The desired edge property for update.
        value: propery dependent value
            New value to be inserted into edge information dictionary for desired attribute.
        """
        # Checks existence of edge as input by user
        if edge_for_update in self.edges:
            index = self.edges.index(edge_for_update)
            self.edges_info[index][2][prop] = value
        else:
            # Checks existence of oppossite direcvtion edge.
            try:
                index = self.edges.index((edge_for_update[1], edge_for_update[0]))
                self.edges_info[index][2][prop] = value
            except:
                raise ValueError("The edge entered does not exist.")

    def update_edge_weight(self, edge_for_update, value):
        """
        Updates the edge weight.

        Parameters
        ----------
        edge_for_update : 2-tuple, vertex pair
            A prexisting edge in the shape to be updated.
        value : int > 0
            New weight to be inserted into edges's information dictionary.
        
        Example
        -------
        >>> A = Shape()
        >>> A.add_edge("xmpl", 2)
        >>> print(A.edges_info)
        [(("xmpl", 2), {weight: 1, colour: "black"})]
        >>> A.update_edge_weight(("xmpl", 2), 20)    # change edge's weight to 20.
        >>> print(A.edges_info)
        [(("xmpl", 2), {weight: 20, colour: "black"})]
        
        Notes
        -----
        This method takes a prexisting edge within the shape and proceeds to update its weight
        property in the edge's infomation dictionary.

        """
        self._update_edge_property(edge_for_update, "weight", value)

    def update_edge_colour(self, edge_for_update, value):
        """
        Updates the edge colour.

        Parameters
        ----------
        edge_for_update : 2-tuple, vertex pair
            A prexisting edge in the shape to be updated.
        value : colour
            New colour to be inserted into edges's information dictionary.
        
        Example
        -------
        >>> A = Shape()
        >>> A.add_edge("xmpl", 2)
        >>> print(A.edges_info)
        [(("xmpl", 2), {weight: 1, colour: "black"})]
        >>> A.update_edge_colour(("xmpl", 2), "yellow")    # change edge's colour to yellow.
        >>> print(A.edges_info)
        [(("xmpl", 2), {weight: 2, colour: "yellow"})]
        
        Notes
        -----
        This method takes a prexisting edge within the shape and proceeds to update its colour
        property in the edge's infomation dictionary.
        """
        self._update_edge_property(edge_for_update, "colour", value)
    
    def _get_edge_info(self, desired_info):
        """
        Private method to get a specific property dictionary for all edges in the shape.

        Parameters
        ----------
        desired_info : "weight" or "colour"
            Desired property to return information about.
        
        Returns
        -------
        edge_info : dictionary
            Property dictionary with edges as keys, and the desired property ('desired_info') as
            values.
        """
        edge_info = {}
        for edge in self.edges_info:
            edge_info[(edge[0], edge[1])] = edge[2][desired_info]
        return edge_info

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
        return self._get_edge_info("weight")
    
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
        return self._get_edge_info("colour")

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

        """
        # Checks both directions for vertex pair
        for e in [edge, (edge[1], edge[0])]:
            if e in self.edges:
                return self.get_edge_vectors()[e]
        raise ValueError("This edge does not exist")

    def generate_shape(self, vertex_pos, shape_name, vectors):
        """
        Less restrictive version of generate polygon. not closed 
        Cannot!!
        """
        edge_list = []
        for k in range(len(vectors) + 1):
            vertex_dict = self.get_vertex_positions()
            found = False
            # Check if a vertex in close prox to vector start and replace
            edge_length = round(sqrt((vectors[k][0])**2 + (vectors[k][1])**2), 3)
            for key in vertex_dict.keys():
                if (vertex_pos[0] - vertex_dict[key][0])**2 + (vertex_pos[1] - vertex_dict[key][1])**2 <= (edge_length/100)**2: ## Change to edge_length!!
                    edge_list.append(key)
                    found = True
                    break
            # Else create new vertex in that spot
            if found == False:
                self.add_vertex(str(shape_name) + "-" + str(k), vertex_pos)
                edge_list.append(str(shape_name) + "-" + str(k))
            if k == len(vectors) - 1:
                break
            vertex_pos = add_vectors(vertex_pos, vectors[k])
        # This does not account for the fact that the final vertex may exist already!!!!!!!
        self.add_vertex(str(shape_name) + "-" + str(len(vectors)), vertex_pos)
        for e in range(len(vectors) - 1):
            self.add_edge(edge_list[e], edge_list[e + 1])
        self.add_edge(edge_list[-1], str(shape_name) + "-" + str(len(vectors)))
        
    
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
    >>>

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
        Initialises a Polygon object with vertices and edges as well as its lattice ability status.
                
        Attributes
        ----------
        .can_lattice : is a boolean value regarding the ability to generate a lattice from the polygon object.
            This attribute runs the the private method '._can_lattice_state'. This check is an abstract method
            that defers to child classes for specific definition.

        Notes
        -----
        The .can_lattice attribute is established here to be inherited by all future child classes
        however the check method itself is to be implemented in these. This is for potential
        future check method on all polygons on their ability to be tesselated.
        """
        super().__init__()
        self.can_lattice = self._get_lattice_state()
    
    def generate_polygon(self, vertex_pos, shape_name, vectors):
        """
        Generates a named polygon from a series of edge vectors staring at a given point.
        
        Parameters
        ----------
        vertex_pos : (x, y) - 2D Cartesian Coordinate
            Start position for the initial vertex in the polygon.
        shape_name : string, int, or float
            This is the overiding shape name dictating all the vertex names within the shape.
            Vertex names are of the form; 'shape_name-k', where k is number of the vertex.
        vectors : list
            This should be an ordered list of edge vectors. This method runs through the list in
            order to generate the polygon. It should be noted that if the last edge vector in the
            list does not "close" the shape itself this last vector will be replaced with an edge
            connecting the last vertex to the starting vertex.

        Notes
        -----
        TO DO... overwriting edges and no two vertices in the same position.
        - WILL NOT DRAW A VERTEX IF THERE EXISTS A VERTEX IN A CLOSE ENOUGH PROXIMITY TO THE 
            DESTINATION!
        - Draws the in
        """
        edge_list = []
        for k in range(len(vectors) + 1):
            vertex_dict = self.get_vertex_positions()
            found = False
            # Check if a vertex in close prox to vector start and replace
            edge_length = round(sqrt((vectors[k][0])**2 + (vectors[k][1])**2), 3)
            for key in vertex_dict.keys():
                if (vertex_pos[0] - vertex_dict[key][0])**2 + (vertex_pos[1] - vertex_dict[key][1])**2 <= (edge_length/100)**2: ## Change to edge_length!!
                    edge_list.append(key)
                    found = True
                    break
            # Else create new vertex in that spot
            if found == False:
                self.add_vertex(str(shape_name) + "-" + str(k), vertex_pos)
                edge_list.append(str(shape_name) + "-" + str(k))
            # Move along next vector
            if k == len(vectors) - 1:
                break
            vertex_pos = add_vectors(vertex_pos, vectors[k])
        # Connect up the vertexes (this closes the loop no matter what)
        for e in range(len(vectors) - 1):
            self.add_edge(edge_list[e], edge_list[e + 1])
        self.add_edge(edge_list[len(vectors) - 1], edge_list[0])

    def generate_lattice_circular(self, layers):
        """
        Generates the polygon's lattice in a given number of layers centred on the staring polygon. Uses the
        abstract methods; '_generate_change_vectors' and '_generate_lattice_circular'.

        Error Handling: Checks '.can_lattice' is True.

        Parameters:
            - layers:
                type: int > 0,
                description: The number of layers to be generated around the original polygon. If 1 is input
                    the original shape is just generated.
        
        Returns:
            - Lattice: specific to shape being generated from.
        """
        if self.can_lattice:
            chg_vectors = self._generate_change_vectors()
            return self._generate_lattice_circular(layers, chg_vectors)
            
        else:
            print("Lattice not possible with this shape.")

    @abc.abstractmethod
    def _generate_change_vectors(self):
        """
        Abstract method that generates the change vectors that define the movement between shapes within the
        lattice. To be defined in child classes.
        """
        return

    @abc.abstractmethod
    def _generate_lattice_circular(self, layer, chg_vectors):
        """
        Abstract method that generates the specific circular lattice for polygons. To be defined in child
        classes.
        """
        return

    @abc.abstractmethod
    def _get_lattice_state(self):
        """
        Abstract method that returns whether or not a polygon can have a lattioce generated from it. To be
        defined in child classes.
        """
        return "To be implemented in child class."


class RegularPolygon(Polygon):
    """
    Regular polygons are defined to be polygons with all edges having equal length and all internal angles
    the same.

    The polygons of this type can thus be defined simply by their number of sides and edge length. Along with
    a given centre and a rotation all further features of these shapes can be found through private class 
    methods.
    """
    def __init__(self, sides: int, edge_length, centre, rotation):
        """
        Regular Polygons are defined by their number of sides and edge length. When initialised, Regular
        Polygon implements both these parameters along with a user defined centre for the shape and an angle of
        rotation. When called regular polygons are automatically generated with help from some variables
        detailed below;

        '_set_radius_info()' calculates the radius vector for the shape. To calculate this, other shape
            variables are calculated (shape angles and radius length). This method is called before
            initialisation of parent class attributes for use in '._get_lattice_state' method.
        '.polygon_vectors' sets the edge_vectors, using the private method '._generate_polygon_vectors', for
            the polygon to then be used in parent class method 'generate_polygon'.

        Error Handling: Series of checks for each parameter to ensure correct type. 

        Parameters:
            - sides:
                type: int > 3,
                description: The number of sides for the regular polygon.
            - edge_length:
                type: (int or float) > 0,
                description: Edge length for all edges of the shape.
            - centre:
                type: (x, y) - Cartesian Coordinate (2-tuple with x, y values: int or float),
                description: Centre point for the shape. For regular polygons this is possible as the uniform
                    nature of the shape results in an equal radius to each vertex in the polygon.
            - rotation:
                type: Angle in the cyclic range (-360, 360),
                description: The angle, in degrees, to rotate the shape arounds its centre anti-clockwise.
                    (Though the type specifies range up to |360| degrees, 'rotation' is cyclic and values
                    outside this reccomendation will still work).
        
        Returns:
            Nothing
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
        Private method for regular polygons to establish shape specific atrributes related to radius
        calculation.

        '.int_angle' is the angle between edges within the shape.
        '.theta' is the angle from one radii to the next about the centre.
        '.radius' is the length of the radius vector.
        '.radius_vector' is the vector from the centre to the initial vertex, with regard to rotation.

        Parameters:
            Nothing
        
        Returns:
            Nothing
        """
        self.int_angle = round(((self.sides - 2)*180)/self.sides, 3)
        self.theta = 180 - self.int_angle
        self.radius = round((self.edge_length)/(2*sin(radians(self.theta/2))), 3)
        self.radius_vec = change_to_cart_vector((self.radius, self.rotation))
    
    def _generate_polygon_vectors(self, sides):
        """
        Private method to generate the edge vectors for a regular polygon.
        
        Parameters:
            Nothing
        
        Returns:
            - vectors: indexed dictionary with edge vectors as values.
        """
        vectors = []
        for i in range(self.sides):
            angle = i*self.theta + (180 - (self.int_angle/2)) + self.rotation
            vectors.append(change_to_cart_vector((self.edge_length, angle)))
        return vectors
    
    def _get_lattice_state(self):
        """
        Private method to check the ability for lattices to be created. For regular polygons this can be
        acheived by seeing if the shape's internal angle divides 360 completly.

        Parameters:
            Nothing

        Returns:
            Nothing
        """
        lattice_test = 360/self.int_angle
        return lattice_test.is_integer()
    
    

################## PRESETs for REGULAR POLYGONs ######################


class EquilateralTriangle(RegularPolygon):
    """
    PRESET SHAPE: EquilateralTriangle

    Equilateral triangles are 3 sided polygons with equal edge length and internal angle of 60 degrees.
    The default Equilateral Triangle is generated "pointing" along the x-axis in the positive direction
    centred at the origin (0, 0). 
    """
    def __init__(self, edge_length = 1, centre = (0, 0), rotation = 0):
        """
        Equilateral Triangles are initialised as Regular Polygons with 3 sides.

        Parameters:
            - edge_length:
                default: 1,
                type: (int or float) > 0,
                description: The deired edge length for the triangles.
            - centre:
                default: Origin (0, 0),
                type: (x, y) - Cartesian Coordinate (2-tuple with x, y values: int or float),
                description: Centre position for the triangle.
            - rotation:
                default: 0,
                type: Angle in the cyclic range (-360, 360),
                description: The angle, in degrees, to rotate the triangle arounds its centre anti-clockwise.
        
        Returns:
            Nothing
        """
        super().__init__(3, edge_length, centre, rotation)

    def _generate_change_vectors(self):
        """
        Private method to generate the lattice change vectors. For triangles these are 6 vectors correspoding 
        to the edge_vectors; 2 for each edge, 1 vector for each direction along the edge.

        Parameters:
            Nothing
        
        Returns:
            - change_vectors: the vectors that move between shapes when generating the lattice. 
        """
        base_vectors = {}
        for i in range(2*self.sides):
            base_vectors[i] = (self.edge_length, 30 + (i + 1)*self.int_angle + self.rotation)
        change_vectors = change_to_cart_dict(base_vectors)
        return change_vectors
    
    def _generate_lattice_circular(self, layers, chg_vectors):
        """
        Private method to create the lattice object corresponding to the current regular polygon. With given
        layers and lattice change vectors this method generates and returns a lattice layer by layer around
        the current regular polygon in a circular fashion.

        Parameters:
            - layers:
                type: int > 0,
                description: Number of layers around the central polygon with layer = 1 being the just the
                    original shape.
            - chg_vectors:
                type: dictionary,
                description: dictionary of vectors describing motion between shapes in the lattice.

        Return:
            - Lattice: Lattice of Equilateral Triangles.
        """
        # Generates the 2 (relected) EquilateralTriangles used.
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
    PRESET SHAPE: Square

    Squares are 4 sided polygons with internal angles of 90 degrees. The default square is positioned with
    its edges at 45 degree angles to the x-axis, centred at the origin.
    """
    def __init__(self, edge_length: float = 1, centre = (0, 0), rotation: float = 0):
        """
        Squares are initialised as Regular Polygons with 4 sides.

        Parameters:
            - edge_length:
                default: 1,
                type: float > 0,
                description: The deired edge length for the triangles.
            - centre:
                default: Origin (0, 0),
                type: (x, y) - Cartesian Coordinate (2-tuple with x, y values: float),
                description: Centre position for the triangle.
            - rotation:
                default: 0,
                type: float, 
                description: Angle in the cyclic range (-360, 360). The angle, in degrees, to rotate the triangle
                    arounds its centre anti-clockwise.
        
        Returns:
            Nothing
        """
        super().__init__(4, edge_length, centre, rotation)

    def _generate_change_vectors(self): 
        """
        Private method to generate the lattice change vectors. For four-sided polygons the change vectors are
        the same as the shapes edge vectors. 

        Parameters:
            Nothing
        
        Returns:
            - .polygon_vectors: the vectors that move between shapes when generating the lattice. 
        """
        return self.polygon_vectors

    def _generate_lattice_circular(self, layers, chg_vectors):
        """
        Private method to create the lattice object corresponding to the current regular polygon. With given
        layers and lattice change vectors this method generates and returns a lattice layer by layer around
        the current regular polygon in a circular fashion.

        Parameters:
            - layers:
                type: int > 0,
                description: Number of layers around the central polygon with layer = 1 being the just the
                    original shape.
            - chg_vectors:
                type: dictionary,
                description: dictionary of vectors describing motion between shapes in the lattice.

        Return:
            - Lattice: Lattice of squares.
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
    PRESET SHAPE: Hexagon

    Regular hexagons are 6 sided polygons with internal angles of 120 degrees. The default Hexagon is positioned with
    its "top" and "bottom" edges parallel to the x-axis, centred at the origin.
    """
    def __init__(self, edge_length = 1, centre = (0, 0), rotation = 0):
        """
        Hexagons are initialised as Regular Polygons with 6 sides.

        Parameters:
            - edge_length:
                default: 1,
                type: (int or float) > 0,
                description: The deired edge length for the triangles.
            - centre:
                default: Origin (0, 0),
                type: (x, y) - Cartesian Coordinate (2-tuple with x, y values: int or float),
                description: Centre position for the triangle.
            - rotation:
                default: 0,
                type: Angle in the cyclic range (-360, 360),
                description: The angle, in degrees, to rotate the triangle arounds its centre anti-clockwise.
        
        Returns:
            Nothing
        """
        super().__init__(6, edge_length, centre, rotation)

    def _generate_change_vectors(self):
        """
        Private method to generate the lattice change vectors. For regular hexagons the change vectors are
        the equivalent to the addition of the first 2 radius vectors rotated about the centre by '.theta'.

        Parameters:
            Nothing
        
        Returns:
            - change_vectors: the vectors that move between shapes when generating the lattice. 
        """
        edgeLengthPlus = 1.5*self.edge_length
        halfHexHeight = round(sqrt(0.75*((self.edge_length)**2)), 2)
        vector_length = round(sqrt(edgeLengthPlus**2 + halfHexHeight**2), 2)
        base_vector = {}
        for i in range(self.sides):
            base_vector[i] = (vector_length, i*(self.theta) + self.theta/2 + self.rotation)
        change_vectors = change_to_cart_dict(base_vector)
        return change_vectors
    
    def _generate_lattice_circular(self, layers, chg_vectors):
        """
        Private method to create the lattice object corresponding to the current regular polygon. With given
        layers and lattice change vectors this method generates and returns a lattice layer by layer around
        the current regular polygon in a circular fashion.

        Parameters:
            - layers:
                type: int > 0,
                description: Number of layers around the central polygon with layer = 1 being the just the
                    original shape.
            - chg_vectors:
                type: dictionary,
                description: dictionary of vectors describing motion between shapes in the lattice.

        Return:
            - Lattice: Lattice of hexagons. 
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
    def _generate_lattice_circular(self, layers, chg_vectors): 
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
