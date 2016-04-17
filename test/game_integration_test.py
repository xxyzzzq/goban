# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from goban.game.game import Game
from goban.modules.renderers.goboard_renderer import GoBoardRenderer

from test.dummy_client import DummyClient
from test.dummy_rule import DummyRule

def main():
    game = Game(DummyRule, GoBoardRenderer)
    game.prepare(None)
    client1 = DummyClient(0, 0)
    client2 = DummyClient(5, 5)
    game.connect(client1)
    game.connect(client2)
    game.start_game()
    game.run()
    game.finalize()

if __name__ == "__main__":
    main()
