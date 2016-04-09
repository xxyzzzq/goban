# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from goban.game.client import Client

class DummyClient(Client):
    def __init__(self):
        super().__init__()
        self.__next_x = 0
        self.__next_y = 0
        pass

    def prepare(self, args):
        pass

    def on_board_updated(self, message):
        pass

    def get_next_move(self):
        result = {"coord": (self.__next_x, self.__next_y), "color": 0}
        self.__next_x = self.__next_x + 1
        self.__next_y = self.__next_y + 1
        return result
