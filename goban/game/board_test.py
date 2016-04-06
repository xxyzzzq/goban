# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import unittest

from goban.game.board import *

class BoardTest(unittest.TestCase):
    def test_init(self):
        board = Board(((0, 10), (0, 10)))
        self.assertEquals(board._dims, ((0, 10), (0, 10)))
        self.assertEquals(len(board._stones), 0)

    def test_place_stone(self):
        board = Board(((0, 10), (0, 10)))
        board.place_stone((0, 0), 0)
        self.assertEquals(board._stones[(0, 0)].get_color(), 0)

if __name__ == "__main__":
    unittest.main()
