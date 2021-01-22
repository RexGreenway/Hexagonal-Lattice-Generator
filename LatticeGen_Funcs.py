import cv2 as cv
import numpy as np
import networkx as nx

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


## VECTOR MANIPULATION ##
def add_vectors(a, b):
    new_val = np.array(a) + np.array(b)
    new_val = (round(new_val[0], 3), round(new_val[1], 3))
    return new_val

## DRAWS SHAPES
def draw_graph(node_pos, graph, shapeName, sides, vectors):
    counter = 0
    edge_dict = {}
    # Add Nodes
    for k in range(sides):
        node_dict = nx.get_node_attributes(graph, "pos")
        if node_pos in node_dict.values():
            node_pos_index = list(node_dict.values()).index(node_pos)
            node = list(node_dict.keys())[(node_pos_index)]
            counter += 1
            edge_dict[counter] = node
        else:
            graph.add_node(shapeName + k/10, pos = node_pos)
            counter += 1
            edge_dict[counter] = shapeName + k/10
        node_pos = add_vectors(node_pos, vectors[k])
    # Add Edges
    for e in range(sides - 1):
        graph.add_edge(edge_dict[e + 1], edge_dict[e + 2])
    graph.add_edge(edge_dict[sides], edge_dict[1])
