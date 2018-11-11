#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from core.foundation.messages import Request, StatusCode
from core.sockets.client import SocketClient
from prettytable import PrettyTable
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

            result = response.data['Result']

            table = PrettyTable()
            table.field_names = ['No.', 'Name', 'Description', 'Cronexp']
            table.align['Name'] = 'l'
            table.align['Description'] = 'l'
            table.align['Cronexp'] = 'l'

            print('\nScheduled jobs:')

            for ii in range(len(result)):

                schedule = result[str(ii)]

                name = schedule.get('name')
                description = schedule.get('description')
                cronexp = schedule.get('cronexp')

                table.add_row([ii, name, description, cronexp])

            print(table)
            print()
            
        else:
            print('Impossible to execute the command')
