import cv2 as cv
import numpy as np

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
def change_vector(a, b, sides):
        shape_pos = []
        for i in range(sides):
            pos_tup = tuple([sum(x) for x in zip(a[i], b)])  # creates initial pos tuples
            e0 = round(pos_tup[0], 3)
            e1 = round(pos_tup[1], 3)
            pos_tup_rounded = (e0, e1)
            shape_pos.append(pos_tup_rounded)  # adds tuples to hex pos
        return shape_pos


## DICTIONARY SEARCH ##
def dict_search(search, dictionary):
    for key, value in dictionary.items():
        if value == search:
            return key
