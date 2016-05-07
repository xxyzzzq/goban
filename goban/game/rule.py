# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from abc import ABCMeta, abstractmethod
from threading import Thread

class Rule:
    __metaclass__ = ABCMeta

    def __init__(self, game, args):
        self._game = game
        self._args = args
        self.__message_queue = Queue()
        self._clients = {}

    def connect(self, client):
        self._clients[client.client_id] = client
        client.on_connected(client_id)

    def _send_client_message(self, client, message):
        client.enqueue_messaeg(message)

    def _broadcast_client_message(self, message):
        for client in self._clients.values():
            self._send_client_message(client, message)

    def disconnect(self, client_id):
        del self._client[client_id]

    def enqueue_message(self, message):
        self.__message_queue.put(message)

    @abstractmethod
    def can_connect(self, client):
        pass

    @abstractmethod
    def create_board(self):
        pass

    @abstractmethod
    def _can_start(self):
        pass

    def start_game(self, game):
        self._game = game
        self._setup_game()
        self.__run_loop_thread = Thread(target=Rule.__message_loop,
                                        name=("Rule message loop thread"),
                                        args=(self,))

    def __message_loop(self):
        while True:
            message = self.__message_queue.get()
            if message['type'] == 'quit':
                # This should only be received from Game
                break
            self._handle_message(message)

    @abstractmethod
    def _init_game(self, game):
        pass

    @abstractmethod
    def _handle_message(self, message):
        pass

    @abstractmethod
    def on_ui_terminate(self):
        pass
