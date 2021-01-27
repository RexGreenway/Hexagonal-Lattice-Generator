# Lattice Generator
By Rex Greenway

This project aims to allow for the investigation of shapes in the R x R Cartesian Plane and their lattices. This Python library provides the functionality to generate, work with, view, and manipulate polygons in the 2D space and, for applciable shapes, generate the corresponding lattice in circular layers. (Currently also utilises OpenCV and Numpy)
https://github.com/RexGreenway/Lattice-Generator.git

# Version 2) (In progress..)
Features so far:
- Basic class structure for Polygons.
- Methods to generate and draw Regular Polygons, and some regular polygon defaults.
- Lattice generation for squares and hexagons.

Completed:
- Re-worked graph generation process to remove unoptimised creation and deletion of vertices and edges.
- Triangle lattice generation.
- Lattice Class and method get_shape_num which retrieves the number of shapes in the lattice.

To be completed:
- Add thorough documentation to all classes.
- Add additional useful methods to relevant classes (translate_shape, rotate_shape, resize_shape, ...).
- Generate Non-Circular Lattices ("stacked").
- Structure to build and work with non-regular polygons, including defaults such as Rectangale, Parallelogram, and Triangle variations.
- Introduce factory to dynamically cast correct object instance when called.

Possibilty:
- Functionality to dynamically detect whether or not a user built shape is able to be tessalated/ lattice?

# Version 1) (Legacy)
Two simple and unoptimised files, using networkx, numpy, opencv, and the maths module to produce specific lattices. 
- Hexagon - Generates lattice of hexagons with desired edge length and number of layers input by the user.
- Parrallogram - Generates lattice of paralleograms, with changable internal angle, to fit within a given circle.

