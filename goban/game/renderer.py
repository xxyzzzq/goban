# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from abc import ABCMeta, abstractmethod

class Renderer:
    __metaclass__ = ABCMeta

    def __init__(self, game):
        self._game = game

    @abstractmethod
    def start(self, game, renderer_cb):
        pass

    @abstractmethod
    def finalize(self):
        pass

    def update(self, args):
        pass
