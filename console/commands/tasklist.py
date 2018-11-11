#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import BaseCommand
from prettytable import PrettyTable

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
