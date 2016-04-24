# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import sys
import argparse
import importlib
import json
import goban.game.game

def main(config):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Goban launcher")
    parser.add_argument('config_file', help="json config file")
    args = parser.parse_args()
    with open(args.config_file) as config_file:
        config = json.load(config_file)
    print config
    main(config)
