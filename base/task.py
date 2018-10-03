#!/usr/bin/python3
# -*- coding: utf-8 -*-

class TaskException(Exception):
    pass

class Task():
    def __init__(self, description = 'generic task'):

        # task info
        if not description:
            raise TaskException('Task must have a description')

        self.description = description

    def run(self):
        raise TaskException('this is a base method and must be overriden')
