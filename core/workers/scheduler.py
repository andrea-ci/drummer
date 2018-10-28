#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation import Request
from core.scheduling import Extender
from threading import Thread
from .worker import Worker
from queue import Queue
from time import sleep


class Scheduler(Worker):
    """ This worker starts the scheduling extender as a thread """

    def __init__(self, queue_w2m, queue_m2w):

        # worker init
        super().__init__(queue_w2m, queue_m2w)

        # create queue for messages
        self.queue_extender = Queue(100)


    def start_extender(self):
        """ start extender thread """

        extender = Extender(self.queue_extender)

        extender.load_jobs()
        extender.run()


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
