# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

class GobanEvent:
    def __init__(self, type, args):
        self.type = type
        self.args = args
