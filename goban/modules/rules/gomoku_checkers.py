# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import copy

from abc import ABCMeta, abstractmethod

from goban.game.board import GoBoard
from goban.game.stone import ColoredStone
from goban.modules.rules.gomoku_utils import *

def _next_coord(coord, direction):
    return (coord[0] + direction[0], coord[1] + direction[1])

def _prev_coord(coord, direction):
    return (coord[0] - direction[0], coord[1] - direction[1])

def _distance(from_coord, to_coord, direction):
    if from_coord == to_coord:
        return 0
    diff = (to_coord[0] - from_coord[0], to_coord[1] - from_coord[1])
    if diff[0] == 0:
        return diff[1] / direction[1]
    return diff[0] / direction[0]

def _coord_at_distance(from_coord, direction, distance):
    return (from_coord[0] + direction[0] * distance, from_coord[1] + direction[1] * distance)

def _sort_coords(coords, direction):
    if len(coords) == 0:
        return []
    distances = []
    ref_coord = coords[0]
    for coord in coords:
        distances.append(_distance(ref_coord, coord, direction))
    distances = sorted(distances)
    sorted_coords = []
    for distance in distances:
        sorted_coords.append(_coord_at_distance(ref_coord, direction, distance))

    return sorted_coords

class GomokuChecker:
    __metaclass__ = ABCMeta

    _DIRECTIONS = {
        'l': (-1, 0),
        'lu': (-1, -1),
        'u': (0, -1),
        'ru': (1, -1),
    }

    def __init__(self):
        pass

    @abstractmethod
    def check(self, board, coord, color):
        ''' Returns true when matches the criteria'''
        pass

    def _opposite_direction(self, direction):
        return (-direction[0], -direction[1])

    def _walk(self, board, start_coord, color, direction, max_steps, max_empty_slots):
        result = []
        coord = start_coord
        steps = 0
        empty_slots_remaining = max_empty_slots
        while steps <= max_steps:
            if not board.check_coord(coord):
                break
            if board.get_stone_at(coord) == None:
                if empty_slots_remaining == 0:
                    break
                empty_slots_remaining = empty_slots_remaining - 1
                coord = _next_coord(coord, direction)
                continue
            if board.get_stone_at(coord).get_color() != color:
                break
            steps = steps + 1
            result.append(coord)
            coord = _next_coord(coord, direction)
        return result

class _GomokuChecker_Win(GomokuChecker):
    def __init__(self):
        GomokuChecker.__init__(self)

    def check(self, board, coord, color):
        for (dir_code, direction) in self._DIRECTIONS.items():
            coords1 = self._walk(board, coord, color, direction,
                                 max_steps = 4,
                                 max_empty_slots = 0)
            coords2 = self._walk(board, coord, color,
                                 self._opposite_direction(direction),
                                 max_steps = 4,
                                 max_empty_slots = 0)
            length = len(coords1) + len(coords2) - 1
            if color == WHITE_COLOR and length > 5:
                return True
            if color == BLACK_COLOR and length == 5:
                return True
        return False

class _GomokuChecker_LongConnection(GomokuChecker):
    def __init__(self):
        GomokuChecker.__init__(self)

    def check(self, board, coord, color):
        if color != BLACK_COLOR:
            return False
        for (dir_code, direction) in self._DIRECTIONS.items():
            coords1 = self._walk(board, coord, color, direction,
                                 max_steps = 4,
                                 max_empty_slots = 0)
            coords2 = self._walk(board, coord, color,
                                 self._opposite_direction(direction),
                                 max_steps = 4,
                                 max_empty_slots = 0)
            length = len(coords1) + len(coords2) - 1
            if color == BLACK_COLOR and length > 5:
                return True
        return False

def _get_slots(board, coords, direction):
    start_coord = _prev_coord(coords[0], direction)
    end_coord = _next_coord(coords[-1], direction)
    slots = []
    slot = start_coord
    while True:
        if (slot not in coords and
            board.check_coord(slot) and
            board.get_stone_at(slot) == None):
            slots.append(slot)
        slot = _next_coord(slot, direction)
        if slot == end_coord:
            break
    if (slot not in coords and
        board.check_coord(slot) and
        board.get_stone_at(slot) == None):
        slots.append(slot)

    return slots

def _check_live3(board, coords, direction, color):
    ''' must be on a line in |direction|, and sorted, and has a maximum of
    1 empty slot in between the stones '''

    slots = _get_slots(board, coords, direction)
    for slot in slots:
        board.place_stone(slot, ColoredStone(color))
        new_slots = copy.deepcopy(coords)
        new_slots.append(slot)
        new_slots = _sort_coords(new_slots, direction)
        result = _check_live4(board, new_slots, direction, color)
        board.remove_stone(slot)
        if result:
            return True
    return False

def _liveness4(board, coords, direction, color):
    ''' must be 4 consequtive stones in line '''
    win_move_count = 0
    slots = _get_slots(board, coords, direction)
    for slot in slots:
        board.place_stone(slot, ColoredStone(color))
        if _GomokuChecker_Win().check(board, slot, color):
            win_move_count = win_move_count + 1
        board.remove_stone(slot)

    return win_move_count

def _check_live4(board, coords, direction, color):
    return _liveness4(board, coords, direction, color) == 2

def _check_hlive4(board, coords, direction, color):
    return _liveness4(board, coords, direction, color) == 1


def _join_coords(coords1, coords2):
    return coords1 + coords2[1:]


class _GomokuChecker_33(GomokuChecker):
    def __init__(self):
        GomokuChecker.__init__(self)

    def check(self, board, coord, color):
        count_3 = 0
        if color != BLACK_COLOR:
            return False
        for (dir_code, direction) in self._DIRECTIONS.items():
            for i in range(0,3):
                coords1 = self._walk(board, coord, color,
                                     self._opposite_direction(direction), i, 1)
                coords1.reverse()
                coords2 = self._walk(board, coord, color, direction, 2 - i, 1)
                coords = _join_coords(coords1, coords2)
                if len(coords) != 3:
                    continue
                if _check_live3(board, coords, direction, color):
                    count_3 = count_3 + 1

        return count_3 >= 2

class _GomokuChecker_44(GomokuChecker):
    def __init__(self):
        GomokuChecker.__init__(self)

    def check(self, board, coord, color):
        count_4 = 0
        if color != BLACK_COLOR:
            return False
        for (dir_code, direction) in self._DIRECTIONS.items():
            for i in range(0,4):
                coords1 = self._walk(board, coord, color,
                                     self._opposite_direction(direction), i, 1)
                coords1.reverse()
                coords2 = self._walk(board, coord, color, direction, 3 - i, 1)
                coords = _join_coords(coords1, coords2)
                if len(coords) != 4:
                    continue
                if _check_live4(board, coords, direction, color):
                    count_4 = count_4 + 1

        return count_4 >= 2

class GomokuCheckerManager(GomokuChecker):
    def __init__(self):
        GomokuChecker.__init__(self)

    def check(self, board, coord, color):
        copy_board = copy.deepcopy(board)
        if _GomokuChecker_Win().check(copy_board, coord, color):
            return color, "5 in a row"
        if _GomokuChecker_LongConnection().check(copy_board, coord, color):
            return other_color(color), "long connection"
        if _GomokuChecker_33().check(copy_board, coord, color):
            return other_color(color), "33"
        if _GomokuChecker_44().check(copy_board, coord, color):
            return other_color(color), "44"
        return None, None
