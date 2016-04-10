# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import pygame
import sys
import time

from goban.game.renderer import Renderer

class DummyRenderer(Renderer):
    def __init__(self, args):
        self.__args = args
        self.__GRID_SIZE = 50
        self.__STONE_SIZE = 40

    def start(self, game):
        if not pygame.init():
            raise Exception("failed to init pygame")
        display_size = self.__args['display_size']
        screen = pygame.display.set_mode(display_size)
        screen.fill(pygame.Color("white"))
        pygame.draw.ellipse(screen, pygame.Color("black"), pygame.Rect((100, 100), (50, 50)))
        while 1:
            event = pygame.event.wait()
            print event
            if event.type == pygame.QUIT: sys.exit()
            pygame.display.flip()

if __name__ == "__main__":
    renderer = DummyRenderer({'display_size': (500, 500)})
    renderer.start({'display_size': (500, 500)})
