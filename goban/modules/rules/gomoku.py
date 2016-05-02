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

    def set_up(self):
        if not self._can_start():
            raise Exception("need exactly 2 clients")
        clients = {}
        self._next_client_id = 0
        for (client_id, client) in self._clients.items():
            clients[self._next_client_id] = client
            self._next_client_id = self._next_client_id + 1
        self._clients = clients

        self._client_id_to_color = {}
        self._color_to_client_id = {}
        black_client_id = self._args['black_client_id']
        for (client_id, client) in self._clients.items():
            if client.client_id == black_client_id:
                self._client_id_to_color[client_id] = BLACK_COLOR
                self._color_to_client_id[BLACK_COLOR] = client_id
                client.prepare({'color': BLACK_COLOR})
            else:
                self._client_id_to_color[client_id] = WHITE_COLOR
                self._color_to_client_id[WHITE_COLOR] = client_id
                client.prepare({'color': WHITE_COLOR})

    def _run_internal(self, game):
        self._game = game
        turn = BLACK_COLOR
        while True:
            client_id = self._color_to_client_id[turn]
            next_move = self._clients[client_id].get_next_move()
            coord = next_move["coord"]
            color = next_move["color"]
            game.get_board().place_stone(coord, ColoredStone(color))
            game.update_renderer({"coord": coord, "stone": ColoredStone(color)})
            game_result = self._check_result(coord, color)
            if game_result != None:
                self.__notify_game_end(game_result)
                break
            if turn == BLACK_COLOR:
                turn = WHITE_COLOR
            else:
                turn = BLACK_COLOR

    def __notify_game_end(self, game_result):
        for (client_id, client) in self._clients.items():
            client.on_game_end(game_result)

    def _can_start(self):
        return len(self._clients) == 2

    def on_ui_terminate(self):
        self.__notify_game_end(None)
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
