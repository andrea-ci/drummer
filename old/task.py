#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Task:

    def __init__(self):

        self._classname = None
        self._timeout = None
        self._params = None
        self._on_pipe = None
        self._on_done = None
        self._on_fail = None
        self._terminated = False
        self._result = None
        self._uid = None

    @property
    def classname(self):
        return self._classname
    @classname.setter
    def classname(self, value):
        self._classname = value

    @property
    def timeout(self):
        return self._timeout
    @timeout.setter
    def timeout(self, value):
        self._timeout = int(value)

    @property
    def on_pipe(self):
        return self._on_pipe
    @on_pipe.setter
    def on_pipe(self, value):
        self._on_pipe = value

    @property
    def on_done(self):
        return self._on_done
    @on_done.setter
    def on_done(self, value):
        self._on_done = value

    @property
    def on_fail(self):
        return self._on_fail
    @on_fail.setter
    def on_fail(self, value):
        self._on_fail = value

    @property
    def params(self):
        return self._params
    @params.setter
    def params(self, value):
        self._params = value
