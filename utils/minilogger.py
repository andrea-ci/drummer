#!/usr/bin/python3
# -*- coding: utf-8 -*-
from logging.handlers import TimedRotatingFileHandler
import logging
from os import path


class LoggerException(Exception):
    pass


class MiniLogger():
    """ get a logger for the application """

    @staticmethod
    def get(configuration):

        # log configuration
        # ------------------------------------------------------- #

        name = configuration.get('application-name')
        logging_config = configuration.get('logging')

        logger = logging.getLogger(name)

        # avoid multiple initializations
        if not logger.handlers:

            logpath = logging_config.get('path')
            logfile = path.join(logpath, name)

            fileLogFormatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s', datefmt='%Y-%m-%d %H:%M')
            fileLogHandler = TimedRotatingFileHandler(logfile, when='d', interval=7, backupCount=4)
            fileLogHandler.setFormatter(fileLogFormatter)

            streamLogFormatter = logging.Formatter('%(levelname)s : %(message)s')
            streamLogHandler = logging.StreamHandler()
            streamLogHandler.setFormatter(streamLogFormatter)

            logger.addHandler(streamLogHandler)
            logger.addHandler(fileLogHandler)

        logger.setLevel(logging_config.get('level'))

        return logger
