#!/usr/bin/python3
# -*- coding: utf-8 -*-
from logging.handlers import TimedRotatingFileHandler
from base.configuration import Configuration
from os import path
import logging


class LoggerException(Exception):
    pass


class FileLogger():
    """ get a logger for the application """

    @staticmethod
    def get():

        config = Configuration.load()

        # log configuration
        # ------------------------------------------------------- #

        name = config.get('application-name')

        logger = logging.getLogger(name)

        # avoid multiple initializations
        if not logger.handlers:

            logging_config = config.get('logging')

            logpath = logging_config.get('path')
            filename = logging_config.get('filename')
            log_level = logging_config.get('level')

            logfile = path.join(logpath, filename)

            fileLogFormatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s', datefmt='%Y-%m-%d %H:%M')
            fileLogHandler = TimedRotatingFileHandler(logfile, when='d', interval=7, backupCount=4)
            fileLogHandler.setFormatter(fileLogFormatter)

            #streamLogFormatter = logging.Formatter('%(levelname)s : %(message)s')
            #streamLogHandler = logging.StreamHandler()
            #streamLogHandler.setFormatter(streamLogFormatter)

            #logger.addHandler(streamLogHandler)
            logger.addHandler(fileLogHandler)

            logger.setLevel(log_level)

        return logger