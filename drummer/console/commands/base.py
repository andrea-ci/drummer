#!/usr/bin/python3
# -*- coding: utf-8 -*-
from drummer.utils import Configuration

class BaseCommand():
    """ Base command to be subclassed """

    CLASSPATH = 'drummer/events'
    
    def __init__(self):

        # load configuration
        self.config = Configuration.load()

    def execute(self):
        raise NotImplementedError('This is an abstract method to override')
