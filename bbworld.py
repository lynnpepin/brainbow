""" bbworld.py

# Provides:
    board_from_pic(image):      Converts a 2D array of RGB-tuples to a 2D array of cells (ints)
    pic_from_board(board):      Converts a 2D array of cells (ints) to a 2D array of RGB-tuples
    save_pic(filename, board):  Save a board to the filename as an image.
    load_pic(filename):         Load the image at the filename as a board. 
    iterate_board(board):       Returns an iterated copy of 'board'
                                (See: iterate_cell)
"""

from cell import cell_to_rgb, rgb_to_cell, iterate_cell
import numpy as np
from PIL import Image

def board_from_pic(image):
    """ Given an h*w*3 numpy array 'image',
    return the h*w numpy array 'board'.
    """
    return np.apply_along_axis(rgb_to_cell, 2, image)
    
def pic_from_board(board):
    """ Given an h*w numpy array 'board',
    return the h*w*3 numpy array 'image'.
    """
    h, w = board.shape
    outimage = np.zeros(shape=(h,w,3),dtype=np.uint8)
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            outimage[y,x] = cell_to_rgb(cell)
    return outimage

def save_pic(board, filename):
    """ Save a board array as an image at the filename """
    h, w = board.shape
    rgbdata = tuple(map(tuple, pic_from_board(board).reshape(-1,3).tolist()))
    image = Image.new("RGB",(w,h))
    image.putdata(rgbdata)
    image.save(filename, "PNG")

def load_pic(filename):
    """ Load an image as a board array from the filename """
    return board_from_pic(np.asarray(Image.open(filename)))

def _get_neighbours(board, x, y, w, h):
    """ Get the 8 orthogonal neighbours of cell x, y from the board.
    w and h are passed as parameters (rather than taken from board.shape)
    because I assumed it'd be faster. I still need to check that.
    
    Operates on the array as a torus (i.e. wraps on edges)
    
    ... What? It's a _ function! Let me optimize prematurely if I want to!
    """
    return ((board[y, (x+1)%w], board[y, (x+2)%w]),
            (board[y, (x-1)%w], board[y, (x-2)%w]),
            (board[(y-1)%h, x], board[(y-2)%h, x]),
            (board[(y+1)%h, x], board[(y+2)%h, x]))

def iterate_board(board):
    """ Given the h*w numpy 'board' array, return the once-iterated
    board, iterated according to the brainbow rules.
    (See: cell.iterate_cell),
    """
    # This can be modified to work in-place on board, if that makes it faster.
    # ... But if we wanted speed, we'd write this in C or Rust or something ;)
    board_copy = np.copy(board)
    h, w = board.shape
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            neighbours = _get_neighbours(board, x, y, w, h)
            board_copy[y,x] = iterate_cell(cell, neighbours)
    return board_copy
