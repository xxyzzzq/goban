# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import Queue

from abc import ABCMeta, abstractmethod
from threading import Thread

class Client:
    __metaclass__ = ABCMeta

    def __init__(self, args):
        self.client_id = args['client_id']
        self.name = args['name']
        self.__message_queue = Queue.Queue()
        self.__run_loop_thread = Thread(target=Client.__message_loop,
                                        name=("Client<" + self.name + "> message loop thread"),
                                        args=(self,))
        self.__run_loop_thread.start()

    def connect_to(self, game):
        game.connect(self)

    def enqueue_message(self, message):
        self.__message_queue.put(message)

    def send_message_to_game(self, message):
        message['client_id'] = self.client_id
        self.__rule.enqueue_message(message)

    def __message_loop(self):
        while True:
            message = self.__message_queue.get()
            print "client.message_loop", message
            if message['type'] == 'quit':
                break
            self.__handle_message(message)

    def __handle_message(self, message):
        ''' All subclasses should call this method from parent class
        and then handle the message themselves'''

        if message['type'] == 'connected':
            self.__on_connected(message)
        else:
            # Non-session message
            self._handle_game_message(message)

    def __on_connected(self, message):
        self.__rule = message['rule']

    @abstractmethod
    def _handle_game_message(self, message):
        pass
