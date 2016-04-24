# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from abc import ABCMeta, abstractmethod

class Rule:
    __metaclass__ = ABCMeta

    def __init__(self, game):
        self._game = game
        self._clients = {}
        self._next_client_id = 0

    def connect(self, client):
        client_id = self._next_client_id
        self._next_client_id = self._next_client_id + 1
        self._clients[client_id] = client
        client.on_connected(client_id)

    def disconnect(self, client_id):
        del self._client[client_id]

    @abstractmethod
    def can_connect(self, client):
        pass

    @abstractmethod
    def create_board(self):
        pass

    @abstractmethod
    def _can_start(self):
        pass

    def run(self, game):
        self._run_internal(game)

    @abstractmethod
    def set_up(self, args):
        ''' should assign client id, notify clients and do other initializations '''
        pass

    @abstractmethod
    def _run_internal(self, game):
        ''' game loop '''
        pass

    @abstractmethod
    def on_ui_terminate(self):
        pass
