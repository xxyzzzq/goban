# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

class Game:
    def __init__(self, rule_class, renderer_class):
        self.__rule_class = rule_class
        self.__renderer = renderer_class

    def prepare(self, args):
        self.__rule = self.__rule_class(args)
        self.__render = self.__renderer_class(args)

    def connect(self, client):
        self.__rule.connect(client)

    def update_render(self):
        self.__renderer.update()

    def start_game(self):
        self.__board = self.__rule.create_board()
        self.__rule.set_up()
        self.__render.start()

    def run(self):
        self.__rule.run(self)

    def get_board(self):
        return self.__board
