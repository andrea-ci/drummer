#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .patterns import PatternLoader
from core.foundation import Request
from sys import exit as sys_exit
import argparse

class ConsoleParser():
    """ validate the user input and returns a request """

    def parse(self, sys_argv):

        # load commands
        commands, usage = PatternLoader.get()

        if len(sys_argv)==1 or sys_argv[1] in ('-h', '--help'):
            print(usage)
            sys_exit()

        # command name
        command = sys_argv[1]

        # name of supported commands
        command_names = [cmd.name for cmd in commands]

        if command in command_names:

            command_to_execute = [cmd for cmd in commands if cmd.name == command][0]

            argparser = command_to_execute.argparser

        else:
            print('command not supported')
            sys_exit()

        # parse command arguments
        args = argparser.parse_args(sys_argv[2:])
        parameters = vars(args)

        # send request
        request = Request()
        request.set_classname(command_to_execute.classname)
        request.set_classpath(command_to_execute.classpath)
        request.set_data(parameters)

        return request
