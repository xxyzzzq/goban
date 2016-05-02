# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import sys
import argparse
import json

from goban.base.import_helper import import_helper
from goban.game.game import Game

def main(config):
    rule_class = import_helper(config['rule_class'])
    args = config['args']
    renderer_class = import_helper(config['renderer_class'])

    game = Game(rule_class, renderer_class)
    game.prepare(args)

    for client_config in config['clients']:
        client_class = import_helper(client_config['class_name'])
        client_args = client_config['args']
        game.connect(client_class(client_args))

    game.start_game()
    game.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Goban launcher")
    parser.add_argument('config_file', help="json config file")
    args = parser.parse_args()
    with open(args.config_file) as config_file:
        config = json.load(config_file)
    print config
    main(config)
