# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from abc import ABCMeta, abstractmethod

class Rule:
    __metaclass__ = ABCMeta

    def __init__(self, args):
        self._args = args
        self._clients = {}

    def connect(self, client):
        client_id = len(self._clients)
        self._clients[client_id] = client
        client.on_connected(client_id)

    def disconnect(self, client_id):
        del self._client[client_id]

    @abstractclass
    def can_connect(self, client):
        pass

    @abstractclass
    def create_board(self):
        pass

    def run(self, game):
        if not self.__check_clients():
            raise Exception("clients not ready")

        self.__notify_client()
        self.__run_internal()

    def set_up():
        ''' should assign client id, notify clients and do other initializations '''
        pass

    @abstractclass
    def __run_internal():
        ''' game loop '''
        pass
