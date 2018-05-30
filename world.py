""" world.py

# Provides:
    board_from_pic(image):  Converts a 2D array of RGB-tuples to a 2D array of cells (ints)
    pic_from_board(board):  Converts a 2D array of cells (ints) to a 2D array of RGB-tuples

# TODO:
    Rename cell.iterate() as iterate_cell()
    Rename ._gen to generation
    Document
    save_pic(filename)
    load_pic(filename)

"""

from cell import cell_to_rgb, rgb_to_cell, iterate as cell_iterate
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



class World():
    def __init__(self, board):
        self._gen = 0
        self._h, self._w = board.shape
        self._board = board
    
    def _get_neighbours(self, board, x, y):
        return ((board[y, (x+1)%self._w], board[y, (x+2)%self._w]),
                (board[y, (x-1)%self._w], board[y, (x-2)%self._w]),
                (board[(y-1)%self._h, x], board[(y-2)%self._h, x]),
                (board[(y+1)%self._h, x], board[(y+2)%self._h, x]))
    
    def iterate(self):
        board_copy = np.copy(self._board)
        for y, row in enumerate(board_copy):
            for x, cell in enumerate(row):
                neighbours = self._get_neighbours(board_copy, x, y)
                self._board[y,x] = cell_iterate(cell, neighbours)
        self._gen += 1
                
