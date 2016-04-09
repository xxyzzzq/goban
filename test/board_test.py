# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import unittest

from goban.game.board import *
from goban.game.stone import *

class BoardTest(unittest.TestCase):
    def test_init(self):
        board = GoBoard(((0, 10), (0, 10)))
        self.assertEquals(board._dims, ((0, 10), (0, 10)))
        self.assertEquals(len(board._stones), 0)

    def test_place_stone(self):
        board = GoBoard(((0, 10), (0, 10)))
        board.place_stone((0, 0), ColoredStone(0))
        self.assertEquals(len(board._stones), 1)
        self.assertEquals(board._stones[(0, 0)].get_color(), 0)

    def test_remove_stone(self):
        board = GoBoard(((0, 10), (0, 10)))
        board.place_stone((0, 0), ColoredStone(0))
        board.remove_stone((0, 0))
        self.assertEquals(len(board._stones), 0)

    def test_change_stone(self):
        board = GoBoard(((0, 10), (0, 10)))
        board.place_stone((0, 0), ColoredStone(0))
        board.change_stone((0, 0), ColoredStone(1))
        self.assertEquals(board._stones[(0, 0)].get_color(), 1)

    def test_get_stone_at(self):
        board = GoBoard(((0, 10), (0, 10)))
        board.place_stone((0, 0), ColoredStone(0))
        self.assertEquals(board.get_stone_at((1, 1)), None)
        self.assertEquals(board.get_stone_at((0, 0)).get_color(), 0)

if __name__ == "__main__":
    unittest.main()
