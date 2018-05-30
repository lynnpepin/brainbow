""" world.py

# Provides:
    board_from_pic(image):  Converts a 2D array of RGB-tuples to a 2D array of cells (ints)
    pic_from_board(board):  Converts a 2D array of cells (ints) to a 2D array of RGB-tuples

# TODO:
    save_pic(filename)
    load_pic(filename)
    
    World._get_neighbours()
    

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



class World():
    def __init__(self, board):
        self._gen = 0
        self._h, self._w = board.shape
        self._board = board
    
    def _get_neighbours(self, x, y):
        return ((self._board[y, (x+1)%self._w], self._board[y, (x+2)%self._w]),
                (self._board[y, (x-1)%self._w], self._board[y, (x-2)%self._w]),
                (self._board[(y-1)%self._h, x], self._board[(y-2)%self._h, x]),
                (self._board[(y+1)%self._h, x], self._board[(y+2)%self._h, x]))
    
    #def iterate():
