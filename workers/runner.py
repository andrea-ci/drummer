#!/usr/bin/python3
# -*- coding: utf-8 -*-
from workers.worker import Worker
from utils.classloader import ClassLoader

class Runner(Worker):
    """ this worker executes commands and tasks"""

    def work(self):

        conn = self.conn

        running = True
        while running:

            # check for requests from listener
            if conn.poll():

                # get the request
                request = conn.recv()

                # load class to exec
                classname = request.classname
                classpath = request.classpath

                ClassToExec = ClassLoader().load(classpath, classname)

                response = ClassToExec().execute(request)

                conn.send(response)

                # done
                running = False

        return
