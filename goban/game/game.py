# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

class Game :
    def __init__(self, board_creator, stone_piece_creator, rule):
        self.__board_creator = board_creator
        self.__stone_creator = stone_piece_creator
