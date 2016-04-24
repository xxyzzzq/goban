# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import time
import sys
import threading
from multiprocessing import Process, Queue
import pygame
from goban.game.board import GoBoard
from goban.game.renderer import Renderer
from goban.base.event import GobanEvent

class GoBoardRenderer(Renderer):
    def __init__(self):
        self.__host_queue = Queue()
        self.__slave_queue = Queue()
        # Spawn the host queue listener thread
        self.__host_queue_listener_thread = threading.Thread(
            target=GoBoardRenderer.__host_queue_loop,
            name='GoBoardRendererHostQueueListenerThread',
            args=(self,))
        self.__host_queue_listener_thread.start()
        # Spawn the Render slave process
        self.__slave = Process(target=_renderer_slave_main,
                               name='GoBoardRenderSlaveProcess',
                               args=(self.__slave_queue, self.__host_queue,))
        self.__slave.start()

    def start(self, game, renderer_cb):
        if not isinstance(game.get_board(), GoBoard):
            raise Exception("renderer only accept GoBoard")
        if len(game.get_board().get_dims()) != 2:
            raise Exception("incorrect number of dimensions")

        self.__game = game
        self.__renderer_cb = renderer_cb
        # send start event
        self.__slave_queue.put(GobanEvent('init', {'dims': game.get_board().get_dims()}))

    def finalize(self):
        self.__host_queue.put(GobanEvent('finalize', None))
        # TODO(xxyzzzq): don't join because deadlock issue, need to improve.
        # self.__host_queue_listener_thread.join()
        self.__slave_queue.put(GobanEvent('finalize', None))
        self.__slave.join()

    def update(self, args):
        self.__slave_queue.put(GobanEvent('place_stone', args))

    def __host_queue_loop(self):
        print 'host_queue_loop start'
        while True:
            event = self.__host_queue.get()
            if event.type == 'uiquit':
                if self.__game:
                    self.__game.on_ui_terminate()
            elif event.type == 'finalize':
                break
            else:
                raise Exception('unknown host queue event')

def _renderer_slave_main(slave_queue, host_queue):
    slave = _GoBoardRendererSlave(slave_queue, host_queue)
    slave.run_loop()

class _GoBoardRendererSlave:

    def __init__(self, slave_queue, host_queue):
        if not pygame.init():
            raise Exception("failed to init pygame")
        self.__slave_queue = slave_queue
        self.__host_queue = host_queue
        # Start the slave queue listener thread
        self.__slave_queue_forwarder_thread = threading.Thread(
            target=_GoBoardRendererSlave.__slave_queue_loop,
                                         name="slave queue forwarder thread",
                                         args=(self,))
        self.__slave_queue_forwarder_thread.start()

    def __slave_queue_loop(self):
        '''
        Forwards the slave queue loop to pygame, must run on child thread.
        '''
        while True:
            event = self.__slave_queue.get()
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
                self.__host_queue.put(GobanEvent('uiquit', None))
            elif event.type == pygame.MOUSEBUTTONUP:
                print "MOUSEBUTTONUP"
                self.__handle_mouse_up()
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

        ((self.__lb, self.__rb), (self.__ub, self.__bb)) = args['dims']

        self.__screen = pygame.display.set_mode(self.__get_display_size())
        self.__draw_board()
        pygame.event.post(pygame.event.Event(pygame.VIDEOEXPOSE, {}))

    def __handle_place_stone_event(self, args):
        self.__draw_stone(args["coord"], args["stone"])
        pygame.event.post(pygame.event.Event(pygame.VIDEOEXPOSE, {}))

    def __get_display_size(self):
        h_size = (self.__rb - self.__lb) * self.__GRID_SIZE + 2 * self.__BOARD_MARGIN
        v_size = (self.__bb - self.__ub) * self.__GRID_SIZE + 2 * self.__BOARD_MARGIN

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
                             (self.__BOARD_MARGIN + self.__GRID_SIZE * (self.__rb - self.__lb),
                              self.__BOARD_MARGIN + self.__GRID_SIZE * x),
                             self.__GRID_WIDTH)
        for y in range(self.__ub, self.__bb + 1):
            pygame.draw.line(self.__screen, self.__GRID_COLOR,
                             (self.__BOARD_MARGIN + self.__GRID_SIZE * y,
                              self.__BOARD_MARGIN),
                             (self.__BOARD_MARGIN + self.__GRID_SIZE * y,
                              self.__BOARD_MARGIN + self.__GRID_SIZE * (self.__bb - self.__ub)),
                             self.__GRID_WIDTH)

    def __draw_stone(self, coord, stone):
        color = stone.get_color()
        pygame.draw.ellipse(self.__screen, self.__STONE_COLORS[color],
                            pygame.Rect(self.__get_stone_position(coord),
                                        (self.__STONE_RADIUS * 2, self.__STONE_RADIUS * 2)))

        pygame.draw.ellipse(self.__screen, pygame.Color("black"),
                            pygame.Rect(self.__get_stone_position(coord),
                                        (self.__STONE_RADIUS * 2, self.__STONE_RADIUS * 2)), 2)

    def __handle_mouse_up(self):
        pass

    def __handle_finalize_event(self):
        pygame.display.quit()
        self.__slave_queue_forwarder_thread.join()
