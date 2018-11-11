#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from utils.classloader import ClassLoader
from prettytable import PrettyTable
from .base import BaseCommand

class TaskExec(BaseCommand):

    def execute(self, params):

        choice_table = PrettyTable()
        choice_table.field_names = ['No.', 'Name', 'Description']
        choice_table.align['Name'] = 'l'
        choice_table.align['Description'] = 'l'

        # read tasks
        try:
            registered_tasks = self.config['tasks']

        except:
            print('Sorry, unable to read task list')

        # task choice
        try:
            print('\nSelect a task to execute:')

            for ii, tsk in enumerate(registered_tasks):
                choice_table.add_row([ii, tsk['classname'], tsk['description']])
            print(choice_table)

            task_to_run = int(input('> '))

            if task_to_run<=ii:
                classpath = 'tasks/'
                classname = registered_tasks[task_to_run]['classname']

            else:
                raise Exception

        except:
            print('Task choice not supported')

        # loading task class
        Task = ClassLoader().load(classpath, classname)

        # task execution
        response = Task().run(params)

        print('\nTask executed.')
        result_table = PrettyTable()
        result_table.field_names = ['Response', 'Data']
        result_table.align = 'l'
        result_table.add_row(['Status', response.status])
        for k,v in response.data.items():
            result_table.add_row([k, v])
        print(result_table)
        print()
