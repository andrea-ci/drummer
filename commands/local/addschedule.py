#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.sockets.client import SocketClient
from base import Configuration
from base.messages import Request
from sys import exit as sys_exit
from croniter import croniter

class AddSchedule():

    def execute(self, request):

        config = Configuration.load()
        registered_tasks = config['tasks']

        # test socket connection
        # TBD

        # handle command parameters
        # parameters = request.parameters
        # ...

        # get job parameters
        parameters = {}
        parameters['name'] = self.get_name()
        parameters['description'] = self.get_description()
        parameters['cronexp'] = self.get_cronexp()
        parameters['task_chain'] = self.get_task_chain(registered_tasks)
        parameters['enabled'] = self.get_status()

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


    def pick_task(self, registered_tasks):

        # select a task
        print('\nChoose a task to execute:')

        for ii,tsk in enumerate(registered_tasks):
            print('[{0}]: {1} - {2}'.format(ii, tsk['classname'], tsk['description']))

        task_no = int(input('Task no.: '))
        task_class = registered_tasks[task_no]['classname']

        return task_class


    def set_connection(self, registered_tasks, task_chain, task_class):

        ans = input('[{0}] Do you want to pipe another task? (n)'.format(task_class))
        if ans == 'y':
            new_task = self.pick_task(registered_tasks)
            task_chain += '{0}[0]:{1};'.format(task_class, new_task)
            task_chain = self.set_connection(registered_tasks, task_chain, new_task)
        else:
            task_chain += '{0}[0]:None;'.format(task_class)

        ans = input('[{0}] Do you want to execute another task OnSuccess? (n)'.format(task_class))
        if ans == 'y':
            new_task = self.pick_task(registered_tasks)
            task_chain += '{0}[1]:{1};'.format(task_class, new_task)
            task_chain = self.set_connection(registered_tasks, task_chain, new_task)
        else:
            task_chain += '{0}[1]:None;'.format(task_class)

        ans = input('[{0}] Do you want to execute another task OnFail? (n)'.format(task_class))
        if ans == 'y':
            new_task = self.pick_task(registered_tasks)
            task_chain += '{0}[2]:{1};'.format(task_class, new_task)
            task_chain = self.set_connection(registered_tasks, task_chain, new_task)
        else:
            task_chain += '{0}[2]:None;'.format(task_class)

        return task_chain


    def get_task_chain(self, registered_tasks):

        task_chain = ''

        # get a task and set connections
        task_class = self.pick_task(registered_tasks)
        task_chain = self.set_connection(registered_tasks, task_chain, task_class)

        print(task_chain)
        return task_chain

    def get_status(self):

        status = 1

        enabled = input('Enable schedule? (y): ')
        if enabled == 'n':
            status = 0

        return status
