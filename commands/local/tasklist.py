#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base.configuration import Configuration

class TaskList():

    def execute(self, request):

        config = Configuration.load()

        try:
            registered_tasks = config['tasks']

            print('\nList of registered tasks:\n')

            for tsk in registered_tasks:

                print('name: {0}'.format(tsk['class']))
                print('description: {0}\n'.format(tsk['description']))

        except:
            raise Exception('unable to load task list')
