#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import exit as sys_exit
from sys import argv as sys_argv
import argparse

class ArgParser:

    def process(self, sys_argv):

        if len(sys_argv)==1:
            print('Command missing. See -h for usage.')
            sys_exit()

        parser = self.define_parsers()
        args = vars(parser.parse_args(sys_argv[1:]))

        classname = args.get('classname')
        del args['classname']

        return classname, args


    def define_parsers(self):

        # create the top-level parser
        parser = argparse.ArgumentParser(prog='Drummer')

        # add subparsers
        subparsers = parser.add_subparsers(help='command help', title='Commands', description='Console operations')

        # service:start
        parser_00 = subparsers.add_parser('service:start', help='Start drummer service')
        parser_00.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_00.set_defaults(classname='ServiceStart')

        # task:list
        parser_01 = subparsers.add_parser('task:list', help='List available tasks')
        #parser_01.add_argument('bar', type=int, help='bar help')
        parser_01.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_01.set_defaults(classname='TaskList')

        # task:exec
        parser_te = subparsers.add_parser('task:exec', help='Execute a task')
        parser_te.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_te.set_defaults(classname='TaskExec')

        # schedule:list
        parser_s01 = subparsers.add_parser('schedule:list', help='List aviable schedules')
        parser_s01.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_s01.set_defaults(classname='ScheduleList')

        # schedule:add
        parser_s02 = subparsers.add_parser('schedule:add', help='Add a new schedule')
        parser_s02.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_s02.set_defaults(classname='ScheduleAdd')

        # schedule:remove
        parser_s03 = subparsers.add_parser('schedule:remove', help='Remove a schedule')
        parser_s03.add_argument('schedule_id', action='store', help='ID of schedule to remove')
        parser_s03.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_s03.set_defaults(classname='ScheduleRemove')

        # schedule:enable
        parser_s04 = subparsers.add_parser('schedule:enable', help='Enable a schedule')
        parser_s04.add_argument('schedule_id', action='store', help='ID of schedule to enable')
        parser_s04.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_s04.set_defaults(classname='ScheduleEnable')

        # schedule:disable
        parser_s06 = subparsers.add_parser('schedule:disable', help='Disable a schedule')
        parser_s06.add_argument('schedule_id', action='store', help='ID of schedule to disable')
        parser_s06.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_s06.set_defaults(classname='ScheduleDisable')

        # schedule:exec
        parser_s07 = subparsers.add_parser('schedule:exec', help='Execute immediately a schedule')
        parser_s07.add_argument('schedule_id', action='store', help='ID of schedule to execute')
        parser_s07.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_s07.set_defaults(classname='ScheduleExec')

        # schedule:get
        parser_s08 = subparsers.add_parser('schedule:get', help='Get information about a schedule')
        parser_s08.add_argument('schedule_id', action='store', help='ID of schedule to get info about')
        parser_s08.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_s08.set_defaults(classname='ScheduleGet')

        return parser
