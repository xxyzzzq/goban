# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from abc import ABCMeta, abstractmethod

class Client:
    __metaclass__ = ABCMeta

    def __init__(self, args):
        self.client_id = args['client_id']
        self.name = args['name']

    def connect(self, game):
        game.connect(self)

    @abstractmethod
    def on_connected(self, args):
        pass

    @abstractmethod
    def prepare(self, args):
        pass

    @abstractmethod
    def on_board_updated(self, message):
        ''' message has the following format
        { ["new_stone": { "coord": <coord>, ...} |
           "changed_stone": { "coord": <coord>, ...} |
           "removed_stone": { "coord": <coord>}] ...}
        '''
        pass

    @abstractmethod
    def get_next_move(self):
        pass

    @abstractmethod
    def on_game_end(self, game_result):
        pass
