# Lattice Generator
By Rex Greenway

This small project uses python libraries networkx, numpy, and OpenCV to generate and draw lattices layer by layer, working out from the centre.

# V1) 2 simple and unoptimised files producing specific lattices. 
- Hexagon - Generates lattice of hexagons with desired edge length and number of layers input by the user.
- Parrallogram - Generates lattice of paralleograms, with changable internal angle, to fit within a given circle.

# V2) (In progress..) Designed as a class based extention to the NetworkX library to work with, view, and manipulate polygons.
Features so far:
- Basic class structure for Regular Polygons.
- Methods to generate and draw Regular Polygons.
- Methods to generate and draw lattices for squares and hexagons.

Completed:
- Re-work graph generation process to remove unoptimised creation and deletion of nodes and edges.

To be completed:
- Triangle Lattice Generation
- Move all libraries (except networkx) to supplimentry file.
- Add thourough documentation to all classes.
- Add additional useful methods to relevant classes. 
- Structure to build and work with non-regular polygons.
- Introduce factory to dynamically cast correct object instance when called.

Possibilty:
- Functionality to dynamically detect whether or not a user built shape is able to be tessalated?  

https://github.com/RexGreenway/Lattice-Generator.git
