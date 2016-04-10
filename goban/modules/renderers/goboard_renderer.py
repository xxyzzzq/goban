# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import threading
import pygame
from goban.game.board import GoBoard
from goban.game.renderer import Renderer

class GoBoardRenderer(Renderer):
    def __init__(self, args):
        if not pygame.init():
            raise Exception("failed to init pygame")
        self.__args = args
        self.__GRID_SIZE = 50
        self.__STONE_RADIUS = 20
        self.__BOARD_MARGIN = 100
        self.__GRID_WIDTH = 5
        self.__STONE_COLORS = [pygame.Color("black"), pygame.Color("white")]
        self.__BOARD_COLOR = pygame.Color("yellow")
        self.__lock = threading.Lock()

    def start(self, game, render_cb):
        if not isinstance(game.get_board(), GoBoard):
            raise Exception("renderer only accept GoBoard")
        if len(game.get_board().get_dims()) != 2:
            raise Exception("incorrect number of dimensions")
        ((self.__lb, self.__rb), (self.__ub, self.__bb)) = game.get_board().get_dims()

        self.__game = game
        self.__screen = pygame.display.set_mode(self.__get_display_size())
        self.__draw_board()
        while True:
            self.__lock.aquire()
            event = pygame.event.wait()
            if (event.type == pygame.VIDEOEXPOSE):
                pygame.display.flip()
                continue
            if (event.type == pygame.VIDEORESIZE):
                raise Exception("resizing not supported")
                continue
            if (event.type == pygame.QUIT):
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONUP):
                self.__handle_mouse_up()
            self.__lock.release()

    def update(self, args):
        self.__lock.aquire()
        self.__draw_stone(self, coord, color)
        pygame.event.post(pygame.Event(pygame.VIDEOEXPOSE, None))
        self.__lock.release()

    def __get_display_size(self):
        h_size = (self.__rb - self.__lb) * self._GRID_SIZE + 2 * self.__BOARD_MARGIN
        v_size = (self.__bb - self.__ub) * self._GRID_SIZE + 2 * self.__BOARD_MARGIN

        return (h_size, v_size)

    def __get_stone_position(self, coord):
        if not self.__board.check_coord(coord):
            raise Exception("out of board")
        h_pos = (coord[0] - self.__lb) * self._GRID_SIZE + self.__BOARD_MARGIN - self.__STONE_RADIUS
        v_pos = (coord[1] - self.__ub) * self._GRID_SIZE + self.__BOARD_MARGIN - self.__STONE_RADIUS
        return (h_pos, v_pos)

    def __draw_board(self):
        self.__screen.fill(self.__BOARD_COLOR)
        for x in range(self.__lb, self.__rb):
            pygame.draw.line(self.__screen, pygame.Color("black"),
                             (self.__BOARD_MARGIN, self.__BOARD_MARGIN + self.__GRID_SIZE * x)
                             (self.__BOARD_MARGIN, self.__BOARD_MARGIN + self.__GRID_SIZE *
                              (self.__rb - x)), self.__GRID_WIDTH)
        for y in range(self.__ub, self.__bb):
            pygame.draw.line(self.__screen, pygame.Color("black"),
                             (self.__BOARD_MARGIN + self.__GRID_SIZE * y, self.__BOARD_MARGIN)
                             (self.__BOARD_MARGIN + self.__GRID_SIZE * (self.__rb - y),
                              self.__BOARD_MARGIN), self.__GRID_WIDTH)

    def __draw_stone(self, coord, color):
        pygame.draw.ellipse(self.__screen, self.__STONE_COLORS[color],
                            pygame.Rect(self.__get_stone_position(coord),
                                        (self.__STONE_RADIUS, self.__STONE_RADIUS)))
