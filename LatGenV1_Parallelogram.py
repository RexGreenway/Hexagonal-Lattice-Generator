import networkx as nx
import cv2 as cv
import numpy as np
from math import sin, cos, pi, sqrt, ceil


def change_vector(a, b):
    para_pos = []
    for i in range(4):
        pos_tup = tuple([sum(x) for x in zip(a[i], b)])  # creates initial pos tuples
        e0 = float("%.3f" % pos_tup[0])
        e1 = float("%.3f" % pos_tup[1])
        pos_tup_rounded = (e0, e1)
        para_pos.append(pos_tup_rounded)  # adds tuples to hex pos
    return para_pos


def dict_search(search, dictionary):
    for key, value in dictionary.items():
        if value == search:
            return key


def dist_from_centre(a):
    return sqrt(a[0] ** 2 + a[1] ** 2)


def create_parallelogram(alpha, radius):
    height = round(sin(alpha), 10)
    width = round(cos(alpha), 10)
    if alpha == 0:  # reverts to squares if angle set to 0
        height = 1
        width = 0

    one = (0, 0)
    two = (1, 0)
    three = (1 + width, height)
    four = (width, height)
    initial_para_pos = [one, two, three, four]

    left = (-1, 0)
    right = (1, 0)
    down = (-width, -height)
    up = (width, height)
    diag = (1 + width, height)

    rows = ceil(radius / height) # how many layers to fit inside half of given circle
    layer_list = list(range(rows))  # up to number of rows
    odd_numbers = list(np.arange(1, len(layer_list) * 2, 2))  # list of odd nums with same index as layer list

    # Generate Positions
    position = []
    for layer in layer_list:

        layer_chg_vec = tuple([layer * x for x in diag])
        para_pos = change_vector(initial_para_pos, layer_chg_vec)
        position.append(para_pos)  # adds initial pos

        for i in range(odd_numbers[layer]):
            para_pos = change_vector(para_pos, down)
            position.append(para_pos)
        for i in range(odd_numbers[layer]):
            para_pos = change_vector(para_pos, left)
            position.append(para_pos)
        for i in range(odd_numbers[layer]):
            para_pos = change_vector(para_pos, up)
            position.append(para_pos)
        for i in range(odd_numbers[layer] - 1):
            para_pos = change_vector(para_pos, right)
            position.append(para_pos)

    # Generate Parallelograms
    G = nx.Graph()
    para_num = (2 * rows)**2
    for para in range(para_num):
        H = nx.Graph()
        for i in range(4):
            H.add_node(para + i / 10, pos=position[para][i])  # add nodes to H
        node_list = list(H.nodes)
        for j in range(3):
            H.add_edge(node_list[j], node_list[j + 1])  # add edges to H
        H.add_edge(node_list[0], node_list[3])

        G_para_dict = nx.get_node_attributes(G, "pos")
        H_para_dict = nx.get_node_attributes(H, "pos")

        H_outside = True
        for v in H_para_dict:
            v_pos = H_para_dict.get(v)
            if dist_from_centre(v_pos) <= radius:
                H_outside = False

        if H_outside:
            H.clear()
        else:
            for v in H_para_dict:
                v_neighbors = list(H.adj[v])
                search_pos = H_para_dict.get(v)
                if search_pos in G_para_dict.values():
                    replacement = dict_search(search_pos, G_para_dict)  # finds the preexisting node with same position
                    H.remove_node(v)  # removes dupe node and all adjacent edges
                    H.add_node(replacement, pos=search_pos)  # adds replacement with same position
                    for e in v_neighbors:
                        H.add_edge(replacement, e)  # re establishes edges with v's original neighbors

        G = nx.compose(G, H)
        G_para_dict = nx.get_node_attributes(G, "pos")

    return {0: G_para_dict, 1: G}


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


def draw_lattice(alpha, radius):
    W = 1050
    size = W, W, 3
    image = np.ones(size)  # creates white canvas

    graph = create_parallelogram(alpha, radius)  # first generate graph of the lattice
    for edge in graph[1].edges:  # draw edges
        start_pos = graph[0][edge[0]]
        start_pos_big = tuple([int(x * 40 + W/2) for x in start_pos])  # adapt position coords for pixel display
        end_pos = graph[0][edge[1]]
        end_pos_big = tuple([int(x * 40 + W/2) for x in end_pos])  # adapt position coords for pixel display
        my_line(image, start_pos_big, end_pos_big)

    for node in graph[0]:  # draw nodes
        node_pos = graph[0][node]
        node_pos_big = tuple([int(x * 40 + W/2)for x in node_pos])  # adapt position coords for pixel display
        my_filled_circle(image, node_pos_big)

    cv.circle(image, tuple([int(x * 40 + W/2)for x in (0, 0)]), int(radius * 40), (0, 255, 0), 1, 8)

    cv.namedWindow("Lattice", cv.WINDOW_AUTOSIZE)  # creates window
    cv.imshow("Lattice", image)  # displays window with lattice image
    cv.waitKey(0)
    cv.destroyAllWindows()


draw_lattice(pi/4, 3.5)
