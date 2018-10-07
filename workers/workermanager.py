#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.classloader import ClassLoader
from utils.filelogger import FileLogger
from multiprocessing import Pipe

class WorkerManager():

    def __init__(self):
        self.logger = FileLogger.get()

    def create_worker(self, worker_name):

        logger = self.logger
        logger.info('Starting {0} worker'.format(worker_name))

        # create connections
        conn1, conn2 = Pipe()

        # load worker class
        WorkerClass = ClassLoader().load('workers', worker_name)

        # create and start worker
        worker = WorkerClass(conn1)
        worker.start()

        pid = conn2.recv()

        logger.info('Worker {0} successfully started with pid {1}'.format(worker_name, pid))

        return conn2
