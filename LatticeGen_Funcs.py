import cv2 as cv
import networkx as nx
from math import sqrt, sin, cos, radians

## OPENCV Drawing Tools ##
# Draws red dot with radius 2 on img at specified center.
def my_filled_circle(img, center):
    cv.circle(
        img,
        center,
        2,
        (0, 0, 255),
        -1,
        8)


# Draws blue line with thickness 1 on img with specified endpoints.
def my_line(img, start, end):
    cv.line(
        img,
        start,
        end,
        (255, 0, 0),
        1)


## VALUE CHECKING ##
def check_if_coord(value):
    if type(value) == tuple and len(value) == 2:
        ans = True
        for i in range(2):
            if type(value[i]) != int and type(value[i]) != float:
                ans *= False
        return bool(ans)
    else:
        return False


## VECTOR MANIPULATION ##
def add_vectors(a, b):
    new_val = (a[0] + b[0], a[1] + b[1])
    new_val = (round(new_val[0], 6), round(new_val[1], 6))
    return new_val

def change_to_cart_vector(polar_vector):
    x = polar_vector[0]*cos(radians(polar_vector[1]))
    y = polar_vector[0]*sin(radians(polar_vector[1]))
    temp = (round(x, 3), round(y, 3))
    return temp

def change_to_cart_dict(dictionary):
    temp = {}
    for i in range(len(dictionary)):
        vector = change_to_cart_vector(dictionary[i])
        temp[i] = vector
    return temp


## DRAWS SHAPES ##
def draw_graph(node_pos, graph, shape_name, vectors):
    edge_list = []
    # Add Nodes
    for k in range(len(vectors)):
        node_dict = nx.get_node_attributes(graph, "pos")
        found = False
        for key in node_dict.keys():
            edge_length = round(sqrt(abs((node_dict[key][0])**2 + (node_dict[key][1])**2)), 3)
            if (node_pos[0] - node_dict[key][0])**2 + (node_pos[1] - node_dict[key][1])**2 < (edge_length/10)**2:
                edge_list.append(key)
                found = True
        if found == False:
            graph.add_node(shape_name + k/10, pos = node_pos)
            edge_list.append(shape_name + k/10)
        node_pos = add_vectors(node_pos, vectors[k])
    # Add Edges
    for e in range(len(vectors) - 1):
        graph.add_edge(edge_list[e], edge_list[e + 1])
    graph.add_edge(edge_list[len(vectors) - 1], edge_list[0])
