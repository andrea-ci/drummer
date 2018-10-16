#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .base import BaseCommand

class TaskList(BaseCommand):

    def execute(self, request):

        try:
            registered_tasks = self.config['tasks']

            print('\nList of registered tasks:\n')

            for tsk in registered_tasks:

                print('name: {0}'.format(tsk['classname']))
                print('description: {0}\n'.format(tsk['description']))

        except:
            raise Exception('unable to load task list')

        return None
