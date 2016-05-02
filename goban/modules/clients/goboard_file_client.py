# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import sys
import json
from goban.game.client import Client

class GoBoardFileClient(Client):
    def __init__(self, args):
        Client.__init__(self, args)
        with open(args['file']) as input_file:
            self.__moves = json.load(input_file)
        self.__iter_moves = iter(self.__moves)

    def on_connected(self, args):
        pass

    def prepare(self, args):
        pass

    def on_board_updated(self, message):
        pass

    def get_next_move(self):
        next_item = self.__iter_moves.next()
        next_item['coord'] = tuple(next_item['coord'])
        print next_item
        return next_item

    def on_game_end(self, game_result):
        pass
