#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from drummer.utils import ClassLoader
from prettytable import PrettyTable
from .base import BaseCommand
import inquirer

class TaskExec(BaseCommand):

    def execute(self, params):

        # read tasks
        try:
            registered_tasks = self.config['tasks']

        except:
            print('Sorry, unable to read task list')

        # task choice
        try:

            print('\nSelect a task to execute:')

            # select a task
            choices = ['{0} - {1}'.format(tsk['classname'], tsk['description']) for tsk in registered_tasks]

            questions = [
                inquirer.List('task_name',
                      message = "Select task to execute",
                      choices = choices,
                      carousel = True,
                  )
              ]
            ans = inquirer.prompt(questions)

            choice_idx = choices.index(ans['task_name'])

            task_to_run = registered_tasks[choice_idx]

            classname = task_to_run['classname']
            classpath = 'tasks/{0}'.format(classname.lower())

            # loading task class
            Task = ClassLoader().load(classpath, classname)

            # task execution
            response = Task().run(params)

        except:
            print('Impossible to execute task')

        else:

            result_table = PrettyTable()
            result_table.field_names = ['Response', 'Data']
            result_table.align = 'l'
            result_table.add_row(['Status', response.status])

            for k,v in response.data.items():

                result_table.add_row([k, v])
                print(result_table)
                print()


        return


class TaskList(BaseCommand):

    def execute(self, params):

        table = PrettyTable()
        table.field_names = ['No.', 'Name', 'Description']
        table.align['Name'] = 'l'
        table.align['Description'] = 'l'

        try:
            registered_tasks = self.config['tasks']

            print('\nList of registered tasks:')

            for ii,tsk in enumerate(registered_tasks):
                table.add_row([ii, tsk['classname'], tsk['description']])
            print(table)
            print()

        except:
            raise Exception('unable to load task list')

        return None
