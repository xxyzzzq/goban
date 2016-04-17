# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from goban.game.rule import Rule
from goban.game.board import GoBoard
from goban.game.stone import ColoredStone

class DummyRule(Rule):
    def __init__(self, args):
        Rule.__init__(self, args)

    def create_board(self):
        return GoBoard(((0, 10), (0, 10)))

    def can_connect(self, client):
        return true

    def set_up(self):
        if len(self._clients) == 0:
            raise Exception("clients not ready")
        for (client_id, client) in self._clients.items():
            client.prepare({'color': client_id})

    def _run_internal(self, game):
        for i in range(0, 5):
            for (client_id, client) in self._clients.items():
                next_move = client.get_next_move()
                coord = next_move["coord"]
                color = next_move["color"]
                game.get_board().place_stone(coord, ColoredStone(color))
                game.update_renderer({"coord": coord, "stone": ColoredStone(color)})

    def _can_start(self):
        return True
