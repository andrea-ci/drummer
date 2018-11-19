#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation.messages import Request, StatusCode
from core.sockets.client import SocketClient
from utils import Configuration

class BaseCommand():
    """ Base command to be subclassed """

    def __init__(self):

        # load configuration
        self.config = Configuration.load()


    def execute(self):
        raise NotImplementedError('This is an abstract method to override')
