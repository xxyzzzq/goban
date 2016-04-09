# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from abc import ABCMeta, abstractmethod

class Renderer:
    def __init__(self, args):
        self.__args = args

    @abstractmethod:
    def start(self, args):
        pass

    @abstractmethod:
    def update():
        pass
