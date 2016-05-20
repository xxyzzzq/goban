# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import pygame
import copy

class Button:
    def __init__(self, surface, rect, color, text):
        self.__surface = surface
        self.__rect = copy.deepcopy(rect)
        self.__color = color
        self.__text = text
        self.__BUTTON_BORDER_WIDTH = 5
        self.__BUTTON_BORDER_COLOR = pygame.Color("black")

    def draw(self):
        pygame.draw.rect(self.__surface, self.__color,
                         self.__rect);
        pygame.draw.rect(self.__surface, self.__BUTTON_BORDER_COLOR,
                         self.__rect, self.__BUTTON_BORDER_WIDTH);
        text_height = int(self.__rect.height / 2)
        font = pygame.font.Font(None, text_height)
        text_surface = font.render(self.__text, True, self.__BUTTON_BORDER_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = self.__rect.center
        self.__surface.blit(text_surface, text_rect)

    def catch_click(self, coord):
        return self.__rect.collidepoint(coord)
