# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

class Game:
    def __init__(self, rule_class, renderer_class):
        self.__rule_class = rule_class
        self.__renderer_class = renderer_class

    def prepare(self, args):
        self.__rule = self.__rule_class(self, args)
        self.__renderer = self.__renderer_class()

    def connect(self, client):
        self.__rule.connect(client)

    def update_renderer(self, args):
        self.__renderer.update(args)

    def start_game(self):
        self.__rule.start_game()
        self.__renderer.start(self, None)

    def get_board(self):
        return self.__rule.get_board()

    def enqueue_message(self, message):
        self.__rule.enqueue_message(message)

    def finalize(self):
        self.__renderer.finalize()
        self.enqueue_message({'type': 'quit'})
