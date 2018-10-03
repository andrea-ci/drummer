#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.sockets.server import SocketServer
from workers.worker import Worker

class Listener(Worker):
    """ this worker starts socket server """

    def work(self):

        # run socket server
        server = SocketServer(self.conn)

        server.run()
