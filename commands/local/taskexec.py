#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.configuration import Configuration
from utils.classloader import ClassLoader

class TaskExec():

    def execute(self, request):

        # load configuration
        config = Configuration.load()

        # read tasks
        try:
            registered_tasks = config['tasks']

        except:
            print('unable to read task list')

        # task choice
        try:
            print('Select a task to run:\n')

            for ii, tsk in enumerate(registered_tasks):
                print('Id {0} - Name: {1}'.format(ii, tsk['classname']))
            print('')

            task_to_run = int(input('> '))

            if task_to_run<=ii:

                classpath = 'tasks/'
                classname = registered_tasks[task_to_run]['classname']

            else:
                raise Exception

        except:
            print('task choice not supported')

        # loading task class
        Task = ClassLoader().load(classpath, classname)

        # task execution
        response = Task().run()

        print('Task executed:')
        print('Status: {0}'.format(response.status))
        print('Message: {0}'.format(response.description))
