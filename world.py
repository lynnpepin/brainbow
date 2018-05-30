""" world.py

# Provides:
    board_from_pic(image):  Converts a 2D array of RGB-tuples to a 2D array of cells (ints)
    pic_from_board(board):  Converts a 2D array of cells (ints) to a 2D array of RGB-tuples

"""

from cell import cell_to_rgb, rgb_to_cell
import numpy as np

def board_from_pic(image):
    return np.apply_along_axis(rgb_to_cell, 2, image)
    
def pic_from_board(board):
    h, w = board.shape
    outimage = np.zeros(shape=(5,4,3),dtype=np.uint8)
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            outimage[y,x] = cell_to_rgb(cell)
    return outimage
