#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from core.sockets.client import SocketClient
from core.foundation.messages import Request
from .base import BaseCommand


class ScheduleList(BaseCommand):

    def execute(self, request):

        # test socket connection
        # TBD

        # handle command parameters
        # args = request.args
        # ...

        # prepare request to listener
        request = Request()
        request.set_classname('JobList')
        request.set_classpath('core/events')

        # send request to listener
        sc = SocketClient()
        response = sc.send_request(request)

        data = response.data
        print(' Scheduled jobs:')
        print(data)
        for schedule in data.values():

            print(schedule)

            name = schedule.get('name')
            description = schedule.get('description')
            cronexp = schedule.get('cronexp')

            print('{0} - {1} - {2}'.format(name, description, cronexp))
