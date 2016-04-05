# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

class StonePiece:
    def __init__(self, board, coord, color):
        self._board = board
        self._coord = coord
        self._color = color

    def __check_coord(board, coord):
        if (board.get_dims().len != coord.len):
            return False
        for ((lb, ub), pos) in zip(board, coord):
            if pos < lb:
                return False
            if pos > ub:
                return False
        return True

class Board:
    def __init__(self, dim):
        self._dim = dim
        self._stones = set()

    def place_stone(self, coord, color):
        piece = StonePiece(this, coord)
        self._stones.
