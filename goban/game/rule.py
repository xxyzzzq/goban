# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import Queue
from abc import ABCMeta, abstractmethod
from threading import Thread

class Rule:
    __metaclass__ = ABCMeta

    def __init__(self, game, args):
        self._game = game
        self._args = args
        self.__message_queue = Queue.Queue()
        self._clients = {}

    def connect(self, client):
        self._clients[client.client_id] = client
        self._send_client_message(client, {'type': 'connected',
                                           'rule': self})

    def _send_client_message(self, client, message):
        print "send_client_message", message
        client.enqueue_message(message)

    def _broadcast_client_message(self, message):
        for client in self._clients.values():
            self._send_client_message(client, message)

    def disconnect(self, client_id):
        self._send_client_message(self._clients[client_id], {'type': 'disconnect'})
        del self._clients[client_id]

    def enqueue_message(self, message):
        self.__message_queue.put(message)

    def get_board(self):
        return self._board

    @abstractmethod
    def can_connect(self, client):
        pass

    @abstractmethod
    def _can_start(self):
        pass

    def start_game(self):
        self._setup_game()
        self.__run_loop_thread = Thread(target=Rule.__message_loop,
                                        name=("Rule message loop thread"),
                                        args=(self,))
        self.__run_loop_thread.start()

    def __message_loop(self):
        while True:
            message = self.__message_queue.get()
            print "rule.message_loop:", message
            if message['type'] == 'quit':
                # Must come from Game.finalize
                break
            self._handle_message(message)

    @abstractmethod
    def _setup_game(self):
        pass

    @abstractmethod
    def _handle_message(self, message):
        pass
