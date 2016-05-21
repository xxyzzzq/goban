# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

class MoveRecorder:
    def __init__(self):
        self.__undo_history = []
        self.__redo_history = []

    def put(self, move):
        self.__redo_history = []
        self.__undo_history.append(move)

    def undo(self):
        if len(self.__undo_history) == 0:
            return None
        move = self.__undo_history.pop()
        self.__redo_history.append(move)
        return move

    def redo(self):
        if len(self.__redo_history) == 0:
            return None
        move = self.__redo_history.pop()
        self.__undo_history.append(move)
        return move
