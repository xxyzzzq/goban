# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import hashlib

class StonePiece:
    def __init__(self, color):
        if color < 0:
            raise Exception("invalid stone color")
        self.__color = color

    def get_color(self):
        return self.__color

    def set_color(self, color):
        if color < 0:
            raise Exception("invalid stone color")
        self.__color = color

class Board:
    def __init__(self, dims):
        if not isinstance(dims, tuple) or len(dims) == 0:
            raise Exception("bad dims")
        for dim in dims:
            if not isinstance(dim, tuple) or len(dim) != 2:
                raise Exception("bad dims")
            if dim[0] > dim[1]:
                raise Exception("bad dims")

        self._dims = dims
        self._stones = {}

    def place_stone(self, coord, color):
        if not self.__check_coord(coord):
            raise Exception("stone out of board")
        if coord in self._stones:
            raise Exception("there's already a stone in the coordinate")
        self._stones[coord] = StonePiece(color)

    def remove_stone(self, coord, color):
        if not self.__check_coord(coord):
            raise Exception("stone out of bound")
        if coord not in self._stones:
            raise Exception("no stone at the coordinate")
        del self._stones[coord]

    def __check_coord(self, coord):
        if len(self._dims) !=  len(coord):
            return False
        for ((lb, ub), pos) in zip(self._dims, coord):
            if pos < lb:
                return False
            if pos > ub:
                return False
        return True
