#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
from sys import argv as sys_argv
from sys import exit as sys_exit

def get_usage(description, commands):

    # main usage help
    usage = '\n{0}\n'.format(description)
    usage += '\nCommands:\n'
    for comm in commands:
        usage += '    {0}\n'.format(comm)

    return usage


# constants
NAME = 'Sledge'
DESCRIPTION = 'Sledge console'
TASK_LIST = 'task:list'
TASK_EXEC = 'task:exec'


if __name__ == '__main__':

    # supported commands
    commands = (TASK_LIST, TASK_EXEC)

    # main usage help
    usage = get_usage(DESCRIPTION, commands)

    if len(sys_argv)==1 or sys_argv[1] in ('-h', '--help'):
        print(usage)
        sys_exit()

    # command name
    command = sys_argv[1]

    # usage for command
    command_usage = '{0} {1} [arguments] [options]'

    # create parser for each command
    if command == TASK_LIST:

        parser = argparse.ArgumentParser(description = DESCRIPTION, usage = command_usage.format(NAME, TASK_LIST))

    elif command == TASK_EXEC:

        parser = argparse.ArgumentParser(description = DESCRIPTION, usage = command_usage.format(NAME, TASK_EXEC))

        parser.add_argument('task_id',
                            action = 'store',
                            help = 'task to execute')

    else:
        print('command not supported')
        sys_exit()

    # common options
    parser.add_argument('-v', '--verbose',
                        help = 'increase output verbosity',
                        action = 'count',
                        default = 0)

    args = parser.parse_args(sys_argv[2:])
    print(args)
