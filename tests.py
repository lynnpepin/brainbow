import numpy as np
import unittest as ut
import itertools as it
import cell
from cell import R, G, B, rot, dot, cell_to_rgb, rgb_to_cell


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
                self.assertEqual(0, cell.iterate(cell=S, neighbours=neighbours))


    def test_iterate_incoming(self):
        for t in self.incoming:
            for S in self.colors:
                for blank_neighbours in it.combinations_with_replacement(self.blanks, 3):
                    neighbours = (t, ) + blank_neighbours
                    self.assertEqual(
                        dot(S,t[0]),
                        cell.iterate(cell=S, neighbours = neighbours)
                    )

    def test_iterate_outgoing(self):
        for S in {R, G, B}:
            for blank_neighbours in it.combinations_with_replacement(self.blanks, 3):
                neighbours = ((rot(S),0), ) + blank_neighbours
                #print(S, neighbours)
                self.assertEqual(
                    rot(S),
                    cell.iterate(cell=S, neighbours=neighbours)
                    )

    # More complicated tests may be in order sometime?

class WorldHelpersTest(ut.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_fromPic(self):
        pass

    def test_toPic(self):
        pass

    def test_rgb_to_board(self):
        pass

    def test_board_to_rgb(self):
        pass

class WorldTest(ut.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_initialize(self):
        pass

    def test_iterate(self):
        pass

tests = [CellsTest]

if __name__ == '__main__':
    for test in tests:
        ut.TextTestRunner(verbosity=2).run(
            ut.TestLoader().loadTestsFromTestCase(test  )
        )
