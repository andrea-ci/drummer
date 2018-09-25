#!/usr/bin/python3
# -*- coding: utf-8 -*-
from console.patterns import PatternLoader
from sys import exit as sys_exit
import argparse


def process_input(sys_argv):

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

        selected_command = [cmd for cmd in commands if cmd.name == command][0]

        argparser = selected_command.argparser

    else:
        print('command not supported')
        sys_exit()

    # parse command arguments
    args = argparser.parse_args(sys_argv[2:])
    args = vars(args)

    return (selected_command, args)
