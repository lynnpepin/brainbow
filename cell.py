""" cell.py

# Provides:
    cell_to_rgb(cell):  Convert, returns a cell to a 3-tuple RGB value
    rgb_to_cell(color): Convert, returns a 3-tuple RGB value to a cell
    rot(cell):          Returns the rotation of a cell (nonstandard)
    dot(cellA, cellB):  Performs the dot of two cells (nonstandard)
    iterate(cell, neighbours):
                        Iterates a cell based on it's 8-closest
                        orthogonal neighbours.
"""

import numpy as np

R = 1
G = 2
B = 3

def cell_to_rgb(cell):
    """ Convert, returns a cell to a 3-tuple RGB value.

    # Arguments:
        cell: Integer in {0, R, G, B}

    # Returns:
        A 3-tuple representing a color. (255,0,0) for R, etc.
    """

    if cell == 0:
        return (255, 255, 255)
    else:
        return (255*(cell == R), 255*(cell == G), 255*(cell == B))

def rgb_to_cell(color):
    """ Convert, returns a 3-tuple RGB value to a cell
    
    # Arguments:
        color: A 3-tuple representing
    
    # Returns:
        An integer {0, R, G, B} representing a cell
    """
    if np.array_equal(color, (255, 255, 255)):
        return 0
    elif np.array_equal(color, (255, 0, 0)):
        return R
    elif np.array_equal(color, (0, 255, 0)):
        return G
    elif np.array_equal(color, (0, 0, 255)):
        return B
    elif np.array_equal(color, (0, 0, 0)):
        return -1

def rot(cell):
    """ Returns the rotation of a cell.
    rot(R) = G, rot(G) = B, rot(B) = R, rot(0) = 0

    # Arguments:
        cell: Integer in {0, R, G, B}

    # Returns:
        An integer {0, R, G, B} representing a cell

    # Note:
        rot(S) is written S+,
        S- is defined such that rot(S-) = (S-)+ = S
    """
    if cell == 0:
        return 0
    else:
        return (cell%3)+1

def dot(cellA, cellB):
    """ Performs the dot of two cells (nonstandard)
    With R, G, B, defined as above, dot(A,B) = A xor B

    # Function specification:
        For a color S in {0, R, G, B},
        S+ and S- defined in the rot() docstring,
        we can define dot() using this pattern:

            dot(S, S) = 0
            dot(S, 0) = dot(0, S) = S
            dot(S, S+) = dot(S+, S) = S-
            dot(S, S-) = dot(S-, S) = S+

        dot(X, Y) also written X.Y

    # Arguments:
        cell: Integer in {0, R, G, B}

    # Returns:
        An integer {0, R, G, B} representing a cell
    """

    return cellA^cellB

def iterate(cell, neighbours):
    """
    # Arguments:
        cell: Integer in {0, R, G, B}
        neighbours: A 4-tuple; each element is a 2-tuple of cells

    # Returns:
        An integer {0, R, G, B} representing a cell

    # Neighbourhood around cell S:
       .  .  .A2.  .  .
       .  .  .A1.  .  .
       .B2.B1. S.C1.C2.
       .  .  .D1.  .  .
       .  .  .D2.  .  .
    """

    # Result R
    R = 0
    # Outgoing value E
    E = 0

    for A1, A2 in neighbours:
    # Look for incoming or outgoing cells
        if rot(A1) == A2:
            # A1 is incoming
            R = dot(R, A1)
        if rot(cell) == A1:
            #A1 is outgoing, head S
            E = A1
    if R != 0:
        # One or more are indeed incoming; modify result R by original cell
        E = cell

    return dot(R, E)
