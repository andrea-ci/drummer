#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.classloader import ClassLoader
from threading import Thread
from queue import Queue


class EventRunner:

    def work(self, request):

        self.running = True

        # load class to exec
        classpath = request.classpath
        classname = request.classname

        # run the task and get task result
        EventToExec = ClassLoader().load(classpath, classname)
        response = EventToExec().execute(request)

        return response
