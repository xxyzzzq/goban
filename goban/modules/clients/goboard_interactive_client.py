# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import sys
import json
from goban.game.client import Client

class GoBoardInteractiveClient(Client):
    def __init__(self, args):
        Client.__init__(self, args)
        self.__is_waiting_for_next_move = False

    def _handle_game_message(self, message):
        if message['type'] == 'game_start':
            self.__handle_game_start(message)
        elif message['type'] == 'get_next_move':
            self.__handle_get_next_move(message)
        elif message['type'] == 'new_stone':
            self.__handle_new_stone(message)
        elif message['type'] == 'remove_stone':
            self.__handle_remove_stone(message)
        elif message['type'] == 'ui_click':
            self.__handle_ui_click(message)
        elif message['type'] == 'game_over':
            self.__handle_game_over(message)
        elif message['type'] == 'disconnect':
            self.__handle_disconnect(message)

    def __handle_game_start(self, message):
        self.__color = message['color']
        self.__board = message['board']

    def __handle_get_next_move(self, message):
        print "Client.get_next_move" + str(self.__color)
        self.__is_waiting_for_next_move = True
        self.__sequence = message['sequence']

    def __handle_new_stone(self, message):
        print "Client.handle_new_stone"
        coord = message['coord']
        stone = message['stone']
        self.__board.place_stone(coord, stone)
        self.__is_waiting_for_next_move = False

    def __handle_remove_stone(self, message):
        print "Client.handle_remove_stone"
        coord = message['coord']
        self.__board.remove_stone(coord)
        self.__is_waiting_for_next_move = False

    def __handle_ui_click(self, message):
        if not self.__is_waiting_for_next_move:
            print "not my turn"
            return
        coord = message['coord']
        if self.__board.get_stone_at(coord) == None:
            self.send_message_to_game({'type': 'place_stone',
                                       'coord': coord,
                                       'color': self.__color,
                                       'sequence': self.__sequence})
            self.__is_waiting_for_next_move = False

    def __handle_game_over(self, message):
        self.__is_waiting_for_next_move = False

    def __handle_disconnect(self, message):
        self.enqueue_message({'type': 'quit'})
