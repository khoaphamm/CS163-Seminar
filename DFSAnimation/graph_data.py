import numpy as np

example_edges = [
    (1,3),
    (1,5),
    (1,9),
    (1,6),
    (2,6),
    (2,8),
    (2,4),
    (3,5),
    (3,7),
    (3,6),
    (3,8),
    (4,10),
    (5,7),
    (9,11),
    (9,12),
    (11,12)
]
example_vertices = np.unique(
    np.array([item for sublist in example_edges for item in sublist])
)