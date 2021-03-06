# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import hashlib
from abc import ABCMeta, abstractmethod

class Board:
    __metaclass__ = ABCMeta

    @abstractmethod
    def place_stone(self, coord, stone):
        pass

    @abstractmethod
    def remove_stone(self, coord):
        pass

    @abstractmethod
    def change_stone(self, coord, stone):
        pass

    @abstractmethod
    def get_stone_at(self, coord):
        pass

class GoBoard:
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
        self._num_stones = 0
        self._max_num_stones = 1
        for dim in dims:
            self._max_num_stones = self._max_num_stones * (dim[1] - dim[0] + 1)

    def place_stone(self, coord, stone):
        print "place_stone", coord, stone
        if not self.check_coord(coord):
            raise Exception("stone out of board")
        if coord in self._stones:
            raise Exception("there's already a stone in the coordinate")
        self._stones[coord] = stone
        self._num_stones = self._num_stones + 1

    def remove_stone(self, coord):
        if coord not in self._stones:
            raise Exception("no stone at the coordinate")
        del self._stones[coord]
        self._num_stones = self._num_stones - 1

    def change_stone(self, coord, stone):
        if coord not in self._stones:
            raise Exception("no stone at the coordinate")
        self._stones[coord] = stone

    def get_stone_at(self, coord):
        if coord not in self._stones:
            return None
        return self._stones[coord]

    def get_dims(self):
        return self._dims

    def check_coord(self, coord):
        if len(self._dims) !=  len(coord):
            return False
        for ((lb, ub), pos) in zip(self._dims, coord):
            if pos < lb:
                return False
            if pos > ub:
                return False
        return True

    def is_full(self):
        print self._num_stones, self._max_num_stones
        if (self._num_stones > self._max_num_stones):
            raise Exception("number of stones reached out of limit")
        return self._num_stones == self._max_num_stones
