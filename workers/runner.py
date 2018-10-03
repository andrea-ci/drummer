#!/usr/bin/python3
# -*- coding: utf-8 -*-
from workers.worker import Worker

class Runner(Worker):
    """ this worker executes commands and tasks"""

    def work(self):

        conn = self.conn

        while True:

            # check for requests from listener
            if conn.poll():

                # get the request
                request = conn.recv()

                # get class name
                class_name = request['class_name']

                mod_to_import = 'commands.remote.{0}'.format(class_name.lower())
                mod = __import__(mod_to_import, fromlist=[class_name])

                CommandClass = getattr(mod, class_name)

                CommandClass().execute(request)

                break
