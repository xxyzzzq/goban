# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

BLACK_COLOR = 0
WHITE_COLOR = 1

def other_color(color):
    if color == BLACK_COLOR:
        return WHITE_COLOR
    else:
        return BLACK_COLOR
