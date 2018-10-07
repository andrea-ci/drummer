#!/usr/bin/python3
# -*- coding: utf-8 -*-
from multiprocessing import Process
from os import getpid as os_getpid

class Worker(Process):

    def __init__(self, conn):

        super().__init__()

        self.conn = conn


    def run(self):

        # get pid and send to master
        pid = os_getpid()
        self.conn.send(pid)

        # begin working
        self.work()


    def work():
        raise NotImplementedError('Worker must override this method')
