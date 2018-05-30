""" world.py

# Provides:
    board_from_pic(image):  Converts a 2D array of RGB-tuples to a 2D array of cells (ints)
    pic_from_board(board):  Converts a 2D array of cells (ints) to a 2D array of RGB-tuples
    World(board):           

# TODO:
    Document
    save_pic(filename)
    load_pic(filename)

"""

from cell import cell_to_rgb, rgb_to_cell, iterate_cell
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

def _get_neighbours(board, x, y, w, h):
    return ((board[y, (x+1)%w], board[y, (x+2)%w]),
            (board[y, (x-1)%w], board[y, (x-2)%w]),
            (board[(y-1)%h, x], board[(y-2)%h, x]),
            (board[(y+1)%h, x], board[(y+2)%h, x]))

def iterate_board(board):
    board_copy = np.copy(board)
    h, w = board.shape
    for y, row in enumerate(board_copy):
        for x, cell in enumerate(row):
            neighbours = _get_neighbours(board_copy, x, y, w, h)
            board[y,x] = iterate_cell(cell, neighbours)
    return board
