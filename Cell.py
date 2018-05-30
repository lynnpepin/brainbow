import numpy as np

R = 1
G = 2
B = 3

# TODO: Documentation

def cell_to_rgb(cell):
    # Convert a cell to an RGB tuple
    if cell == 0:
        return (255,255,255)
    else:
        return (255*(cell==R), 255*(cell==G), 255*(cell==B))

def rgb_to_cell(color):
    # Convert an RGB tuple to a cell
    if color == (255, 255, 255):
        return 0
    elif color == (255, 0, 0):
        return R
    elif color == (0, 255, 0):
        return G
    elif color == (0, 0, 255):
        return B
    elif color == (0, 0, 0):
        return -1

def rot(cell):
    # Rotate a cell
    # Written S+
    # R -> G, G -> B, B -> R; 0 -> 0
    if cell == 0:
        return 0
    else:
        return (cell%3)+1

def dot(cellA, cellB):
    # Dot on cells
    # S.S = 0, S.0 = S, S.S+ = S-, S.S- = S+
    return cellA^cellB

def iterate(cell, neighbours):
    # iterate a cell according to it's neighbours, where
    # neighbours is a 4-set of ordered tuples.
    # E.g. neighbours = {(A1,A2), (B1,B2), (C1,C2), (D1,D2)},
    #      cell = S
    #  .  .A2.  .  
    #  .  .A1.  .
    #B2.B1. S.C1.C2
    #  .  .D1.  .
    #  .  .D2.  .

    R = 0       # Result
    E = 0       # Outgoing value

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

    return dot(R,E)


















