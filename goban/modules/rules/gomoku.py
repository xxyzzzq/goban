# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from goban.game.rule import Rule
from goban.game.board import GoBoard
from goban.game.stone import ColoredStone

class GomokuRule(Rule):
    BLACK_COLOR = 0
    WHITE_COLOR = 1

    def __init__(self, args):
        Rule.__init__(self, args)
        self.__args = args

    def create_board(self):
        return GoBoard(self.__args['dims'])

    def can_connect(self, client):
        return len(self._clients) < 2

    def set_up(self, args):
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
        black_client_uuid = args['black_client_uuid']
        for (client_id, client) in self._clients.items():
            if client.uuid == start_client_uuid:
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

    def __notify_game_end(self, game_result):
        for (client_id, client) in self._clients.items():
            client.on_game_end(game_result)

    def _can_start(self):
        return len(self._clients) == 2

    def on_ui_terminate(self):
        self.__notify_game_end(None)
        self._game.finalize()
