#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from core.sockets.client import SocketClient
from core.foundation.messages import Request, StatusCode
from .base import BaseCommand


class ScheduleList(BaseCommand):

    def execute(self, params):

        # test socket connection
        # TBD

        # handle command parameters
        # args = request.args
        # ...

        # prepare request to listener
        request = Request()
        request.set_classname('JobList')
        request.set_classpath('core/events')
        request.set_data(params)

        # send request to listener
        sc = SocketClient()
        response = sc.send_request(request)

        if response.status == StatusCode.STATUS_OK:

            result = response.data['result']

            print(' Scheduled jobs:')

            for ii in range(len(result)):

                schedule = result[str(ii)]

                name = schedule.get('name')
                description = schedule.get('description')
                cronexp = schedule.get('cronexp')

                print('{0} - {1} - {2}'.format(name, description, cronexp))

        else:
            print('Impossible to execute the command')
