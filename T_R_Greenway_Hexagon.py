import networkx as nx
import cv2 as cv
import numpy as np
from math import sin, cos, pi, sqrt, ceil

# this is a test

### HEX GEN ###
sideLength = float("%.3f" % float(input("Please input desired side legnth: ")))
halfHexHeight = float("%.3f" % sqrt(sideLength**2 - (sideLength/2)**2))
print(halfHexHeight)
#Centre
centre = [(sideLength, 0), (sideLength/2, halfHexHeight), (- sideLength/2, halfHexHeight), (- sideLength, 0), (- sideLength/2, - halfHexHeight), (sideLength/2, - halfHexHeight)]
#Vectors
sideLengthPlus = sideLength + (sideLength/2)
chg_vec_se = (sideLengthPlus, - halfHexHeight)
chg_vec_sw = (- sideLengthPlus, - halfHexHeight)
chg_vec_nw = (- sideLengthPlus, halfHexHeight)
chg_vec_n = (0.000, 2*halfHexHeight)
chg_vec_ne = (sideLengthPlus, halfHexHeight)
chg_vec_s = (0.000, - 2*halfHexHeight)

def change_vector(a, b):
    hex_pos = []
    for i in range(6):
        pos_tup = tuple([sum(x) for x in zip(a[i], b)])  # creates initial pos tuples
        e0 = float("%.3f" % pos_tup[0])
        e1 = float("%.3f" % pos_tup[1])
        pos_tup_rounded = (e0, e1)
        hex_pos.append(pos_tup_rounded)  # adds tuples to hex pos
    return hex_pos


def dict_search(search, dictionary):
    for key, value in dictionary.items():
        if value == search:
            return key


def create_lattice():
    # Establish constants
    m = int(input("Enter Number of Layers: "))

    hex_num = int(1 + 6 * ((m * (m - 1)) / 2))
    layer_list = list(range(m))

    # Generate Positions
    position = []
    for layer in layer_list:
        if layer == 0:
            position.append(centre)
        else:
            layer_chg_vec = tuple([layer * x for x in chg_vec_se])  # scales change vector
            hex_pos = change_vector(centre, layer_chg_vec)
            position.append(hex_pos)  # adds initial hex pos
            for i in range(layer):
                hex_pos = change_vector(hex_pos, chg_vec_sw)
                position.append(hex_pos)
            for i in range(layer):
                hex_pos = change_vector(hex_pos, chg_vec_nw)
                position.append(hex_pos)
            for i in range(layer):
                hex_pos = change_vector(hex_pos, chg_vec_n)
                position.append(hex_pos)
            for i in range(layer):
                hex_pos = change_vector(hex_pos, chg_vec_ne)
                position.append(hex_pos)
            for i in range(layer):
                hex_pos = change_vector(hex_pos, chg_vec_se)
                position.append(hex_pos)
            for i in range(layer - 1):
                hex_pos = change_vector(hex_pos, chg_vec_s)
                position.append(hex_pos)

    # Generate Hexagons
    G = nx.Graph()
    for hexagon in range(hex_num):
        H = nx.Graph()
        for i in range(6):
            H.add_node(hexagon + i / 10, pos=position[hexagon][i])  # add nodes to H
        node_list = list(H.nodes)
        for j in range(5):
            H.add_edge(node_list[j], node_list[j + 1])  # add edges to H
        H.add_edge(node_list[0], node_list[5])

        G_hex_dict = nx.get_node_attributes(G, "pos")
        H_hex_dict = nx.get_node_attributes(H, "pos")
        for v in H_hex_dict:
            v_neighbors = list(H.adj[v])
            search_pos = H_hex_dict.get(v)
            if search_pos in G_hex_dict.values():
                replacement = dict_search(search_pos, G_hex_dict)  # finds the preexisting node with same position
                H.remove_node(v)  # removes dupe node and all adjacent edges
                H.add_node(replacement, pos=search_pos)  # adds replacement with same position
                for e in v_neighbors:
                    H.add_edge(replacement, e)  # re establishes edges with v's original neighbors

        G = nx.compose(G, H)
        G_hex_dict = nx.get_node_attributes(G, "pos")

    return {0: G_hex_dict, 1: G}
    # nx.draw(G, G_hex_dict, with_labels=True)
    # plt.show()
    # print("\n", nx.info(G))


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


def draw_lattice():
    W = 1050
    size = W, W, 3
    image = np.ones(size)  # creates white canvas
    
    ## CREATE LATTICE
    graph = create_lattice()  # first generate graph of the lattice

    ## DRAW LATTICE
    for edge in graph[1].edges:  # draw edges
        start_pos = graph[0][edge[0]]
        start_pos_big = tuple([int(x * 20 + W/2) for x in start_pos])  # adapt position coords for pixel display
        end_pos = graph[0][edge[1]]
        end_pos_big = tuple([int(x * 20 + W/2) for x in end_pos])  # adapt position coords for pixel display
        my_line(image, start_pos_big, end_pos_big)

    for node in graph[0]:  # draw nodes
        node_pos = graph[0][node]
        node_pos_big = tuple([int(x * 20 + W/2)for x in node_pos])  # adapt position coords for pixel display
        my_filled_circle(image, node_pos_big)

    cv.namedWindow("Lattice", cv.WINDOW_AUTOSIZE)  # creates window
    cv.imshow("Lattice", image)  # displays window with lattice image
    cv.waitKey(0)
    cv.destroyAllWindows()


draw_lattice()
