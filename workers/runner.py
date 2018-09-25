#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.configuration import Configuration
from multiprocessing import Process


class Runner(Process):

    def __init__(self, conn, request):

        super().__init__()

        self.conn = conn

        self.request = request


    def run(self):

        if self.request == 'date':

            # do stuff
            response = 'date is today!'

            self.conn.send(response)
            self.conn.close()

            return
