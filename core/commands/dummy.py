#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.filelogger import FileLogger
from datetime import datetime

class Dummy():

    def execute(self, parameters):

        logger = FileLogger.get()

        logger.debug('running local dummy command')

        print(datetime.now())
