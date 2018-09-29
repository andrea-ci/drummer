#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.configuration import Configuration
from core.sockets import SocketServer
from multiprocessing import Process

class Listener(Process):
    """ this worker starts socket server with a pipe to communicate with master """

    def __init__(self, conn):

        super().__init__()

        self.conn = conn


    def run(self):

        # run socket server
        server = SocketServer(self.conn)
        
        server.run()
