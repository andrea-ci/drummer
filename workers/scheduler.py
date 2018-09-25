#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.configuration import Configuration
from multiprocessing import Process


class Scheduler(Process):

    def __init__(self, conn):

        super().__init__()

        self.conn = conn
