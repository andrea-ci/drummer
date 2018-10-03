#!/usr/bin/python3
# -*- coding: utf-8 -*-
from workers.worker import Worker
from time import sleep

class Scheduler(Worker):

    def work(self):

        while True:

            sleep(1)
