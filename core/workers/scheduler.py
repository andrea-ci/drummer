#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.scheduling.extender import Extender
from multiprocessing import Process, Queue
from queue import Queue as threading_queue
from os import getpid as os_getpid
from threading import Thread
from time import sleep


class Scheduler(Process):
    """ This worker starts the scheduling extender as a thread """

    def __init__(self):

        # worker init
        super().__init__()

        # queue worker -> master
        self.queue_w2m = Queue(100)

        # create queue for messages
        self.queue_extender = threading_queue(100)


    def get_queues(self):
        return self.queue_w2m


    def start_extender(self):
        """ start extender thread """

        extender = Extender(self.queue_extender)

        extender.load_jobs()
        extender.run()


    def run(self):

        # get pid and send to master
        pid = os_getpid()
        self.queue_w2m.put(pid)

        # begin working
        self.work()


    def work(self):

        # connection to master
        queue_w2m = self.queue_w2m

        # start extender thread
        thread_extender = Thread(target=self.start_extender, args=())
        thread_extender.start()

        while True:

            # check for messages from extender thread
            while not self.queue_extender.empty():

                job = self.queue_extender.get()

                queue_w2m.put(job)

            sleep(0.1)
