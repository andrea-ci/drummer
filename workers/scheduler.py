#!/usr/bin/python3
# -*- coding: utf-8 -*-
from workers.worker import Worker
from scheduler.extender import Extender

class Scheduler(Worker):
    """ this worker starts the scheduling extender """

    def work(self):
        """ start extender """

        extender = Extender()

        extender.load_jobs()
        extender.run()
