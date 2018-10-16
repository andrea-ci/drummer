#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils import Configuration

class BaseCommand():
    """ Base command to be subclassed """

    def __init__(self):

        # load configuration
        self.config = Configuration.load()

    def test_socket_connection(self):
        return True
