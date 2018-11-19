#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from core.foundation.messages import Request, StatusCode
from core.sockets.client import SocketClient
from prettytable import PrettyTable
from sys import exit as sys_exit
from .base import BaseCommand
from croniter import croniter
import json


class ScheduleCommand(BaseCommand):

    def test_socket_connection(self):

        # prepare request to listener
        request = Request()
        request.set_classname('SocketTest')
        request.set_classpath('core/events')

        try:

            # send request to listener
            sc = SocketClient()
            response = sc.send_request(request)

            assert response.status == StatusCode.STATUS_OK

            return True

        except:

            print('Connection test failed, maybe socket is down.')
            sys_exit()

        else:
            return


class ScheduleAdd(ScheduleCommand):

    def execute(self, request):

        # test socket connection
        self.test_socket_connection()

        registered_tasks = self.config['tasks']

        # test socket connection
        # TBD

        # handle command parameters
        # parameters = request.parameters
        # ...

        # get schedulation data from the user
        schedulation = {}
        schedulation['name'] = self.set_name()
        schedulation['description'] = self.set_description()
        schedulation['cronexp'] = self.set_cronexp()
        schedulation['parameters'] = self.set_schedulation_parameters(registered_tasks)
        schedulation['enabled'] = self.set_job_status()

        # prepare request to listener
        request = Request()
        request.set_classname('JobAdd')
        request.set_classpath('core/events')
        request.set_data(schedulation)

        # send request to listener
        sc = SocketClient()
        response = sc.send_request(request)

        print('Result: {0} -> {1}'.format(response.status, response.description))

        return


    def set_name(self):
        # get job information
        name = input('Name of the Job: ')
        return name


    def set_description(self):
        description = input('Brief description of job: ')
        return description


    def set_cronexp(self):

        # cron expression
        cronexp = input('Cron expression: ')

        if not croniter.is_valid(cronexp):
            print('cron expression not valid')
            sys_exit()
        return cronexp


    def set_task(self, registered_tasks, schedulation_parameters):

        # select a task
        print('\nChoose a task to execute:')

        for ii,tsk in enumerate(registered_tasks):
            print('[{0}]: {1} - {2}'.format(ii, tsk['classname'], tsk['description']))

        task_no = int(input('Task no.: '))
        classname = registered_tasks[task_no]['classname']

        # set task parameters
        task = {}
        task['timeout'] = self.set_timeout()
        task['parameters'] = self.set_task_parameters(classname)
        task['onPipe'] = None
        task['onSuccess'] = None
        task['onFail'] = None

        schedulation_parameters['tasklist'][classname] = task

        return schedulation_parameters, classname


    def set_task_parameters(self, classname):
        ans = input('[{0}] Set task parameters (none)'.format(classname))


    def set_connection(self, registered_tasks, parameters, base_task):

        ans = input('[{0}] Do you want to pipe another task? (n)'.format(base_task))
        if ans == 'y':
            parameters, next_task = self.set_task(registered_tasks, parameters)
            parameters['tasklist'][base_task]['onPipe'] = next_task
            parameters = self.set_connection(registered_tasks, parameters, next_task)

        ans = input('[{0}] Do you want to execute another task OnSuccess? (n)'.format(base_task))
        if ans == 'y':
            parameters, next_task = self.set_task(registered_tasks, parameters)
            parameters['tasklist'][base_task]['onSuccess'] = next_task
            parameters = self.set_connection(registered_tasks, parameters, next_task)

        ans = input('[{0}] Do you want to execute another task OnFail? (n)'.format(base_task))
        if ans == 'y':
            parameters, next_task = self.set_task(registered_tasks, parameters)
            parameters['tasklist'][base_task]['onFail'] = next_task
            parameters = self.set_connection(registered_tasks, parameters, next_task)

        return parameters


    def set_schedulation_parameters(self, registered_tasks):

        schedulation_parameters = {'tasklist': {}}

        # get a task and set connections
        schedulation_parameters, classname = self.set_task(registered_tasks, schedulation_parameters)

        schedulation_parameters['root'] = classname
        schedulation_parameters = self.set_connection(registered_tasks, schedulation_parameters, classname)

        # serialize to json
        schedulation_parameters = json.dumps(schedulation_parameters)

        return schedulation_parameters


    def set_timeout(self):

        timeout = input('Task timeout [s] (600): ')
        try:
            timeout = int(timeout)
        except:
            timeout = 600
        return timeout


    def set_job_status(self):

        status = 1
        enabled = input('Enable schedule? (y): ')
        if enabled == 'n':
            status = 0

        return status


class ScheduleList(ScheduleCommand):

    def execute(self, args):

        # test socket connection
        self.test_socket_connection()

        # handle command parameters
        # args = request.args
        # ...

        # prepare request to listener
        request = Request()
        request.set_classname('JobList')
        request.set_classpath('core/events')
        request.set_data(args)

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


class ScheduleEnable(ScheduleCommand):
    pass


class ScheduleDisable(ScheduleCommand):
    pass


class ScheduleExec(ScheduleCommand):
    pass
