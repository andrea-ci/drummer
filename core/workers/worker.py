#!/usr/bin/python3
# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue
from utils.classloader import ClassLoader
from utils.filelogger import FileLogger
from os import getpid as os_getpid


class Worker(Process):
    """ Worker is a sub-class of Process and, in turn, is sub-classed by Listener, Scheduler and Runner.
        This class provides methods for creating the specialized workers and send back their PID to master process.
        Scheduler has a queue to communicate,
        Listener has two queues to write requests and read responses,
        Runner has a one-sized queue.
    """

    def __init__(self, queue_w2m, queue_m2w):

        super().__init__()

        # queue worker -> master
        self.queue_w2m = queue_w2m
        # queue master -> worker
        self.queue_m2w = queue_m2w


    def run(self):

        # get pid and send to master
        pid = os_getpid()
        self.queue_w2m.put(pid)

        # begin working
        self.work()


    def work():
        raise NotImplementedError('Worker must override this method')


    @staticmethod
    def from_classname(classname):

        logger = FileLogger.get()

        logger.debug('Starting {0} worker'.format(classname))

        # create queues
        if classname == 'Listener' or classname == 'Runner':
            queue_w2m = Queue(1)
            queue_m2w = Queue(1)

        elif classname == 'Scheduler':
            queue_w2m = Queue(100)
            queue_m2w = None

        else:
            raise TypeError('Worker type not supported')

        # load worker class
        WorkerClass = ClassLoader().load('core/workers', classname)

        # create and start worker
        worker = WorkerClass(queue_w2m, queue_m2w)
        worker.start()

        # get worker pid
        pid = queue_w2m.get()

        logger.debug('Worker {0} successfully started with pid {1}'.format(classname, pid))

        if queue_m2w:
            return queue_w2m, queue_m2w
        else:
            return queue_w2m
