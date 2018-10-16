#!/usr/bin/python3
# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue
from utils.classloader import ClassLoader
from utils.filelogger import FileLogger
from os import getpid as os_getpid
class Worker(Process):

    def __init__(self, queue):

        super().__init__()

        self.queue = queue


    def run(self):

        # get pid and send to master
        pid = os_getpid()
        self.queue.put(pid)

        # begin working
        self.work()


    def work():
        raise NotImplementedError('Worker must override this method')


    @staticmethod
    def from_classname(classname):

        logger = FileLogger.get()

        logger.debug('Starting {0} worker'.format(classname))

        # create queue
        queue = Queue(100)

        # load worker class
        WorkerClass = ClassLoader().load('core/workers', classname)

        # create and start worker
        worker = WorkerClass(queue)
        worker.start()

        # get worker pid
        pid = queue.get()

        logger.debug('Worker {0} successfully started with pid {1}'.format(classname, pid))

        return queue
