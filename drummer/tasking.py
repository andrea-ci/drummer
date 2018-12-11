#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This module provides a convenient interface for implementing user-defined tasks """

from drummer.foundation import Response, StatusCode


class Task:

    def __init__(self, config, logger):

        self.config = config
        self.logger = logger
