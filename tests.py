import numpy as np
import unittest as ut
import itertools as it
import cell
from cell import R, G, B, rot, dot, cell_to_rgb, rgb_to_cell, iterate_cell
import bbworld
from bbworld import board_from_pic, pic_from_board, _get_neighbours, iterate_board, save_pic, load_pic
from PIL import Image
import numpy as np

class CellsTest(ut.TestCase):
    def setUp(self):
        self.colors      = (0, R, G, B)
        self.blanks      = ((0,0), (0,R), (0,G), (0,B))
        self.red_in      = (R,G)
        self.blue_in     = (B,R)
        self.green_in    = (G,B)
        self.incoming    = (self.red_in, self.blue_in, self.green_in)
    
    def tearDown(self):
        pass

    def test_cell_to_rgb(self):
        self.assertEqual(cell_to_rgb(R), (255, 0 ,0))
        self.assertEqual(cell_to_rgb(G), (0, 255, 0))
        self.assertEqual(cell_to_rgb(B), (0, 0, 255))
        self.assertEqual(cell_to_rgb(0), (255, 255, 255))

    def test_rgb_to_cell(self):
        self.assertEqual(rgb_to_cell((255, 0, 0)), R)
        self.assertEqual(rgb_to_cell((0, 255, 0)), G)
        self.assertEqual(rgb_to_cell((0, 0, 255)), B)
        self.assertEqual(rgb_to_cell((255, 255, 255)), 0)

    def test_rot(self):
        self.assertEqual(rot(R), G)
        self.assertEqual(rot(G), B)
        self.assertEqual(rot(B), R)
        self.assertEqual(rot(0), 0)

    def test_dot(self):
        for S in self.colors:
            #S.S=0
            self.assertEqual(dot(S, S), 0)
            #S.0 = 0
            self.assertEqual(dot(S, 0), S)
            self.assertEqual(dot(0, S), S)
            #S.S+ = S-
            self.assertEqual(dot(S, rot(S)), rot(rot(S)))
            self.assertEqual(dot(rot(S), S), rot(rot(S)))
            #S.S- = S+
            self.assertEqual(dot(S, rot(rot(S))), rot(S))
            self.assertEqual(dot(rot(rot(S)), S), rot(S))

    def test_iterate_cell_on_blanks(self):
        for S in self.colors:
            for neighbours in it.combinations_with_replacement(self.blanks, 4):
                self.assertEqual(0, iterate_cell(cell=S, neighbours=neighbours))


    def test_iterate_incoming(self):
        for t in self.incoming:
            for S in self.colors:
                for blank_neighbours in it.combinations_with_replacement(self.blanks, 3):
                    neighbours = (t, ) + blank_neighbours
                    self.assertEqual(
                        dot(S,t[0]),
                        iterate_cell(cell=S, neighbours = neighbours)
                    )

    def test_iterate_outgoing(self):
        for S in {R, G, B}:
            for blank_neighbours in it.combinations_with_replacement(self.blanks, 3):
                neighbours = ((rot(S),0), ) + blank_neighbours
                #print(S, neighbours)
                self.assertEqual(
                    rot(S),
                    iterate_cell(cell=S, neighbours=neighbours)
                    )
    # More complicated tests may be in order sometime?


class WorldTest(ut.TestCase):
    def setUp(self):
        fname0_0    = "test_images/00_step00.png"
        fname0_1    = "test_images/00_step01.png"
        self.rgb0_0_open = np.asarray(Image.open(fname0_0))
        self.rgb0_1_open = np.asarray(Image.open(fname0_1))
        self.board0_0 =np.array(
                    [   [R,G,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,B,0,0]])
        self.board0_1 =np.array(
                    [   [G,B,0,R],
                        [0,G,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0]])

    def tearDown(self):
        pass
    
    def test_board_from_pic(self):
        self.assertTrue(
            np.array_equiv(
                board_from_pic(self.rgb0_0_open),
                self.board0_0
            )
        )
        self.assertTrue(
            np.array_equiv(
                board_from_pic(self.rgb0_1_open),
                self.board0_1
            )
        )

    def test_pic_from_board(self):
        self.assertTrue(
            np.array_equiv(
                self.rgb0_0_open,
                pic_from_board(self.board0_0)
            )
        )
        self.assertTrue(
            np.array_equiv(
                self.rgb0_1_open,
                pic_from_board(self.board0_1)
            )
        )
        
    def test_pic_io(self):
        save_pic(self.board0_0, "test_images/savetest.png")
        b0 = load_pic("test_images/savetest.png")
        self.assertTrue(
            np.array_equal(b0, self.board0_0)
        )

    def test_get_neighbours(self):
        neighbours = _get_neighbours(self.board0_0, x=1, y=2, w=4, h=5)
        self.assertEqual(neighbours.count((0,0)), 2)
        self.assertEqual(neighbours.count((0,G)), 1)
        self.assertEqual(neighbours.count((0,B)), 1)
        
        neighbours = _get_neighbours(self.board0_0, x=2, y=0, w=4, h=5)
        self.assertEqual(neighbours.count((G,R)), 1)
        self.assertEqual(neighbours.count((0,R)), 1)
        self.assertEqual(neighbours.count((0,0)), 2)

    def test_bbworld_iterate(self):
        self.assertTrue(
            np.array_equal( iterate_board(self.board0_0), self.board0_1 )
        )
        # Make sure that it didn't modify board0_0:
        self.assertFalse(
            np.array_equal(self.board0_0, self.board0_1)
            )


tests = [   CellsTest,
            WorldTest
            ]


if __name__ == '__main__':
    for test in tests:
        ut.TextTestRunner(verbosity=2).run(
            ut.TestLoader().loadTestsFromTestCase(test  )
        )
