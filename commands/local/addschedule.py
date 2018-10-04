#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.sockets.client import SocketClient
from base import Configuration
from base.messages import Request
from sys import exit as sys_exit
from croniter import croniter

class AddSchedule():

    def execute(self, request):

        # test socket connection
        # TBD

        # handle command parameters
        # parameters = request.parameters
        # ...

        # get job parameters
        parameters = {}
        parameters['name'] = self.get_name()
        parameters['description'] = self.get_description()

        # cron expression
        parameters['cronexp'] = self.get_cronexp()

        # prepare request to listener
        message = Request()
        request.set_classname('JobAdd')
        request.set_classpath('commands/remote')
        request.set_parameters(parameters)

        # send request to listener
        sc = SocketClient()
        response = sc.send_request(request)

        return response

    def get_name(self):
        # get job information
        name = input('Name of the Job: ')
        return name

    def get_description(self):
        description = input('Brief description of job: ')
        return description

    def get_cronexp(self):
        # cron expression
        cronexp = input('Cron expression: ')

        if not croniter.is_valid(cronexp):
            print('cron expression not valid')
            sys_exit()
        return cronexp
