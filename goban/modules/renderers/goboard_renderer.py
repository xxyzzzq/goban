# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import copy
import time
import sys
import threading
from multiprocessing import Process, Queue
import pygame
from goban.game.board import GoBoard
from goban.game.renderer import RendererHost
from goban.base.event import GobanEvent
from goban.modules.renderers.button import Button

class GoBoardRendererHost(RendererHost):
    def __init__(self):
        self.__host_queue = Queue()
        self.__impl_queue = Queue()
        # Spawn the host queue listener thread
        self.__host_queue_listener_thread = threading.Thread(
            target=GoBoardRendererHost.__host_queue_loop,
            name='GoBoardRendererHostQueueListenerThread',
            args=(self,))
        self.__host_queue_listener_thread.start()
        # Spawn the Render impl process
        self.__impl_process = Process(target=_renderer_impl_main,
                              name='GoBoardRenderImplProcess',
                              args=(self.__impl_queue, self.__host_queue,))
        self.__impl_process.start()

    def start(self, game, renderer_cb):
        if not isinstance(game.get_board(), GoBoard):
            raise Exception("renderer only accept GoBoard")
        if len(game.get_board().get_dims()) != 2:
            raise Exception("incorrect number of dimensions")

        self.__game = game
        self.__renderer_cb = renderer_cb
        # send start event
        self.__impl_queue.put(GobanEvent('init', {'dims': game.get_board().get_dims()}))

    def finalize(self):
        self.__host_queue.put(GobanEvent('finalize', None))
        self.__host_queue_listener_thread.join()
        self.__impl_queue.put(GobanEvent('finalize', None))
        self.__impl_process.join()

    def update(self, args):
        self.__impl_queue.put(GobanEvent('place_stone', args))

    def __host_queue_loop(self):
        print 'host_queue_loop start'
        while True:
            event = self.__host_queue.get()
            if event.type == 'ui_click':
                self.__game.enqueue_message({'type': 'ui_click', 'coord': event.args})
            elif event.type == 'ui_exit':
                if self.__game:
                    self.__game.enqueue_message({'type': 'ui_exit'})
            elif event.type == 'finalize':
                break
            else:
                raise Exception('unknown host queue event')

def _renderer_impl_main(impl_queue, host_queue):
    impl = _GoBoardRendererImpl(impl_queue, host_queue)
    impl.run_loop()

class _GoBoardRendererImpl:

    def __init__(self, impl_queue, host_queue):
        if not pygame.init():
            raise Exception("failed to init pygame")
        self.__impl_queue = impl_queue
        self.__host_queue = host_queue
        # Start the impl queue listener thread
        self.__impl_queue_forwarder_thread = threading.Thread(
            target=_GoBoardRendererImpl.__impl_queue_loop,
            name="impl queue forwarder thread",
            args=(self,))
        self.__impl_queue_forwarder_thread.start()

    def __impl_queue_loop(self):
        '''
        Forwards the impl queue loop to pygame, must run on child thread.
        '''
        while True:
            event = self.__impl_queue.get()
            # Tries to post the event to the pygame event queue until success
            while True:
                try:
                    pygame.event.post(pygame.event.Event(
                        pygame.USEREVENT,
                        {'user_event_type': event.type, 'args': event.args}))
                    break
                except pygame.error:
                    pass
                time.sleep(0.001)

            if event.type == 'finalize':
                break

    def run_loop(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.VIDEOEXPOSE:
                print "VIDEOEXPOSE"
                pygame.display.flip()
            elif event.type == pygame.VIDEORESIZE:
                print "VIDEORESIZE"
                raise Exception("resizing not supported")
            elif event.type == pygame.QUIT:
                print "QUIT"
                self.__host_queue.put(GobanEvent('ui_exit', None))
            elif event.type == pygame.MOUSEBUTTONUP:
                print "MOUSEBUTTONUP"
                self.__handle_mouse_up(event)
            elif event.type == pygame.USEREVENT:
                event_type = event.user_event_type
                event_args = event.args
                print "USEREVENT, ", event_type, event_args
                if event_type == 'init':
                    self.__handle_init_event(event_args)
                elif event_type == 'place_stone':
                    self.__handle_place_stone_event(event_args)
                elif event_type == 'finalize':
                    self.__handle_finalize_event()
                    return
                else:
                    raise Exception("unknown user event")

    def __handle_init_event(self, args):
        self.__GRID_SIZE = 50
        self.__STONE_RADIUS = 20
        self.__BOARD_MARGIN = 100
        self.__GRID_WIDTH = 5
        self.__STONE_COLORS = [ pygame.Color("black"), pygame.Color("white") ]
        self.__STONE_LINE_COLOR = pygame.Color("black")
        self.__STONE_LINE_WIDTH = 5
        self.__GRID_COLOR = pygame.Color("black")
        self.__BOARD_COLOR = pygame.Color("white")
        self.__BUTTON_WIDTH = 80
        self.__BUTTON_HEIGHT = 40
        self.__BUTTON_COLOR = pygame.Color("yellow")

        ((self.__lb, self.__rb), (self.__ub, self.__bb)) = args['dims']

        self.__screen = pygame.display.set_mode(self.__get_display_size())
        self.__draw_board()
        self.__draw_buttons()
        pygame.event.post(pygame.event.Event(pygame.VIDEOEXPOSE, {}))

    def __handle_place_stone_event(self, args):
        self.__draw_stone(args["coord"], args["stone"])
        pygame.event.post(pygame.event.Event(pygame.VIDEOEXPOSE, {}))

    def __get_display_size(self):
        h_size = self.__board_x_dim() * self.__GRID_SIZE + 2 * self.__BOARD_MARGIN
        v_size = self.__board_y_dim() * self.__GRID_SIZE + 2 * self.__BOARD_MARGIN

        return (h_size, v_size)

    def __get_stone_position(self, coord):
        h_pos = ((coord[0] - self.__lb) * self.__GRID_SIZE +
                 self.__BOARD_MARGIN - self.__STONE_RADIUS)
        v_pos = ((coord[1] - self.__ub) * self.__GRID_SIZE +
                 self.__BOARD_MARGIN - self.__STONE_RADIUS)
        return (h_pos, v_pos)

    def __draw_board(self):
        self.__screen.fill(self.__BOARD_COLOR)
        for x in range(self.__lb, self.__rb + 1):
            pygame.draw.line(self.__screen, self.__GRID_COLOR,
                             (self.__BOARD_MARGIN,
                              self.__BOARD_MARGIN + self.__GRID_SIZE * x),
                             (self.__BOARD_MARGIN + self.__GRID_SIZE * self.__board_x_dim(),
                              self.__BOARD_MARGIN + self.__GRID_SIZE * x),
                             self.__GRID_WIDTH)
        for y in range(self.__ub, self.__bb + 1):
            pygame.draw.line(self.__screen, self.__GRID_COLOR,
                             (self.__BOARD_MARGIN + self.__GRID_SIZE * y,
                              self.__BOARD_MARGIN),
                             (self.__BOARD_MARGIN + self.__GRID_SIZE * y,
                              self.__BOARD_MARGIN + self.__GRID_SIZE * self.__board_y_dim()),
                             self.__GRID_WIDTH)

    def __draw_stone(self, coord, stone):
        color = stone.get_color()
        pygame.draw.ellipse(self.__screen, self.__STONE_COLORS[color],
                            pygame.Rect(self.__get_stone_position(coord),
                                        (self.__STONE_RADIUS * 2, self.__STONE_RADIUS * 2)))

        pygame.draw.ellipse(self.__screen, pygame.Color("black"),
                            pygame.Rect(self.__get_stone_position(coord),
                                        (self.__STONE_RADIUS * 2, self.__STONE_RADIUS * 2)), 2)

    def __draw_buttons(self):
        button_rect = pygame.Rect(0, 0, self.__BUTTON_WIDTH, self.__BUTTON_HEIGHT)
        button_rect.centerx = int(self.__BOARD_MARGIN * 1.5 +
                                  self.__GRID_SIZE * self.__board_x_dim())
        button_rect.centery = int(self.__BOARD_MARGIN * 0.5)

        self.__undo_button = Button(self.__screen, button_rect,
                                    self.__BUTTON_COLOR, "UNDO")

        button_rect.centery = int(button_rect.centery + 1.5 * self.__BUTTON_HEIGHT)
        self.__redo_button = Button(self.__screen, button_rect,
                                    self.__BUTTON_COLOR, "REDO")
        self.__undo_button.draw()
        self.__redo_button.draw()

    def __handle_mouse_up(self, event):
        if event.button != 1:
            return
        pos = list(event.pos)
        if self.__undo_button.catch_click(pos):
            self.__handle_undo()
            return
        if self.__redo_button.catch_click(pos):
            self.__handle_redo()
            return

        pos[0] = pos[0] - self.__BOARD_MARGIN + self.__GRID_SIZE / 2
        pos[1] = pos[1] - self.__BOARD_MARGIN + self.__GRID_SIZE / 2
        coord = (self.__lb + pos[0] / self.__GRID_SIZE, self.__ub + pos[1] / self.__GRID_SIZE)
        print coord
        if coord[0] > self.__rb or coord[1] > self.__bb:
            return
        self.__host_queue.put(GobanEvent('ui_click', coord))

    def __handle_finalize_event(self):
        pygame.display.quit()
        self.__impl_queue_forwarder_thread.join()

    def __board_x_dim(self):
        return self.__rb - self.__lb

    def __board_y_dim(self):
        return self.__bb - self.__ub

    def __handle_undo(self):
        pass

    def __handle_redo(self):
        pass
