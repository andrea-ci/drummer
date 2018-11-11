#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from core.foundation.messages import Request
from sys import exit as sys_exit
from sys import argv as sys_argv
import argparse

class ArgParser:

    def process(self, sys_argv):

        parser = self.define_parsers()
        args = vars(parser.parse_args(sys_argv[1:]))

        # get command classname
        if args:
            classname = args.get('classname')
            del args['classname']

            # command parameters
            params = args

            return classname, params

        else:
            print('Syntax error. Use -h option for help.')
            sys_exit()


    def define_parsers(self):

        # create the top-level parser
        parser = argparse.ArgumentParser(prog='Sledge')

        # add subparsers
        subparsers = parser.add_subparsers(help='command help', title='Sledge commands', description='Featured operations')

        # task:list
        parser_tl = subparsers.add_parser('task:list', help='List available tasks')
        #parser_tl.add_argument('bar', type=int, help='bar help')
        parser_tl.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_tl.set_defaults(classname='TaskList')

        # task:exec
        parser_te = subparsers.add_parser('task:exec', help='Execute a task')
        parser_te.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_te.set_defaults(classname='TaskExec')

        # schedule:add
        parser_sa = subparsers.add_parser('schedule:add', help='Add a new schedule')
        parser_sa.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_sa.set_defaults(classname='ScheduleAdd')

        # schedule:list
        parser_sa = subparsers.add_parser('schedule:list', help='List aviable schedules')
        parser_sa.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_sa.set_defaults(classname='ScheduleList')

        # schedule:exec
        parser_se = subparsers.add_parser('schedule:exec', help='Execute immediately a schedule')
        parser_se.add_argument('job_id', action='store', help='Job ID to execute')
        parser_se.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_se.set_defaults(classname='ScheduleExec')

        # schedule:enable
        parser_sen = subparsers.add_parser('schedule:enable', help='Enable a schedule')
        parser_sen.add_argument('job_id', action='store', help='Job ID to enable')
        parser_sen.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_sen.set_defaults(classname='ScheduleEnable')

        # schedule:disable
        parser_sd = subparsers.add_parser('schedule:disable', help='Disable a schedule')
        parser_sd.add_argument('job_id', action='store', help='Job ID to disable')
        parser_sd.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_sd.set_defaults(classname='ScheduleDisable')

        return parser
