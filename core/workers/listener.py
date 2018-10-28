#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.sockets.server import SocketServer
from multiprocessing import Pipe
from .worker import Worker

class Listener(Worker):
    """ this worker starts socket server """

    def work(self):

        # run socket server
        server = SocketServer(self.queue_w2m, self.queue_m2w)

        server.run()
