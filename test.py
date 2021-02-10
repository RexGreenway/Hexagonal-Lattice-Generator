import polylatlib as pl

# Drawing the shapes the wrong way????
A = pl.Rectangle(2, 2, rotation=10)
A.add_vertex("Origin", (0, 0), 10, "r")
latA = A.generate_lattice_from_vectors(2, A.polygon_vectors)
latA.add_vertex("Centre", (1, 1), 10, "r")

latA.draw_shape()