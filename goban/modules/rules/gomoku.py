# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from goban.game.rule import Rule
from goban.game.board import GoBoard
from goban.game.stone import ColoredStone

BLACK_COLOR = 0
WHITE_COLOR = 1

class GomokuRule(Rule):

    def __init__(self, game, args):
        Rule.__init__(self, game, args)

    def create_board(self):
        return GoBoard(self.__list_to_tuple_recursive(self._args['dims']))

    def can_connect(self, client):
        return len(self._clients) < 2

    def _setup_game(self):
        self.__next_color = BLACK_COLOR
        if not self._can_start():
            raise Exception("need exactly 2 clients")

        self._client_id_to_color = {}
        self._color_to_client_id = {}
        black_client_id = self._args['black_client_id']
        if black_client_id not in self._clients:
            raise Exception("black_client_id invalid")

        for (client_id, client) in self._clients.items():
            if client.client_id == black_client_id:
                self._client_id_to_color[client_id] = BLACK_COLOR
                self._color_to_client_id[BLACK_COLOR] = client_id
                client.prepare({'color': BLACK_COLOR})
            else:
                self._client_id_to_color[client_id] = WHITE_COLOR
                self._color_to_client_id[WHITE_COLOR] = client_id
                client.prepare({'color': WHITE_COLOR})

        # Broadcast game start
        for (client_id, client) in self._clients.items():
            self._send_client_message(client,
                                      {'type': 'game_start',
                                       'board': self._game.get_board(),
                                       'color': self._client_id_to_color[client_id]})
        self.__notify_client_to_move(self.__next_color)

    def _handle_message(self, message):
        if message['type'] == 'renderer_exit':
            self.__handle_renderer_exit(message)
        if message['type'] == 'place_stone':
            self.__handle_place_stone(message)

    def __other_color(self, color):
        if color == BLACK_COLOR:
            return WHITE_COLOR
        else:
            return BLACK_COLOR

    def __handle_place_stone(self, message):
        coord = message['coord']
        color = next_move['color']
        client_id = next_move['client_id']
        # Placing a stone of the opponent's color
        if color != self._client_id_to_color[color]:
            self.__on_game_over(color, "placing opponent's stone")
        # Not your turn
        if color != self.__next_color:
            self.__on_game_over(self.__other_color(color), "not your turn")
        try:
            self._game.get_board().place_stone(coord, ColoredStone(color))
        except Exception as e:
            # Illegal move
            self.__on_game_over(self.__other_color(color))
        self._game.update_renderer({'type': 'new_stone',
                                    'coord': coord,
                                    'stone': ColoredStone(color)})

        (win_side, reason) = self._check_result(coord, color)
        if win_side != None:
            self.__on_game_over(win_side, reason)
            return
        self.__next_color = self.__other_color(self.__next_color)
        self.__notify_client_to_move(self.__next_color)

    def __notify_client_to_move(self, color):
        client_id = self._color_to_client_id[color]
        self._send_client_message(self._clients[client_id], {'type': 'get_next_move'})

    def __on_game_over(self, win_side, reason):
        pass

    def _can_start(self):
        return len(self._clients) == 2

    def __handle_renderer_exit(self):
        self.__on_game_over(self, None, "renderer_exit")
        self._game.finalize()

    def __list_to_tuple_recursive(self, l):
        result = []
        for item in l:
            if isinstance(item, list):
                result.append(self.__list_to_tuple_recursive(item))
            else:
                result.append(item)
        return tuple(result)

    def _check_result(self, coord, color):
        return None
