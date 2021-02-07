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

def is_positive_int(value):
    if value > 0 and type(value) == int:
        return True
    else:
        return False

def is_supported_colour(colour):
    colours = ["black", "red", "green", "blue", "yellow", "orange", "purple"]
    if colour in colours:
        return True
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
