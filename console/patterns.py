#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse

class UsagePattern():

    def __init__(self, name, description = '', argparser = None, task_class = None):

        self.name = name

        self.description = description

        self.argparser = argparser

        self.task_class = task_class


class PatternLoader():

    @staticmethod
    def get_usage(commands):

        # main usage help
        usage = '\n{0}\n'.format('Sledge console')
        usage += '\nCommands:\n'
        for comm in commands:
            usage += '    {0}\n'.format(comm.name)

        return usage


    @staticmethod
    def get():

         # init
        commands = []

        # usage string
        common_usage = 'sledge {0} [arguments] [options]'


        # task list
        # ----------------------------------------------- #

        name = 'task:list'

        parser = argparse.ArgumentParser(
            description = 'sledge {0} command'.format(name),
            usage = common_usage.format(name)
            )
        parser.add_argument(
            '-v', '--verbose',
            help = 'increase output verbosity',
            action = 'count',
            default = 0
            )

        commands.append(
            UsagePattern(
                name,
                description = 'list all tasks',
                argparser = parser,
                task_class = 'TaskList'
            )
        )


        # task execute
        # ----------------------------------------------- #

        name = 'task:exec'

        parser = argparse.ArgumentParser(
            description = 'sledge {0} command'.format(name),
            usage = common_usage.format(name)
            )
        parser.add_argument(
            'task_id',
            action = 'store',
            help = 'task to execute'
            )
        parser.add_argument(
            '-v', '--verbose',
            help = 'increase output verbosity',
            action = 'count',
            default = 0
            )

        commands.append(
            UsagePattern(
                name,
                description = 'execute a task',
                argparser = parser,
                task_class = 'TaskExec'
            )
        )


        # add a schedule
        # ----------------------------------------------- #

        name = 'schedule:add'

        parser = argparse.ArgumentParser(
            description = 'sledge {0} command'.format(name),
            usage = common_usage.format(name)
            )
        parser.add_argument(
            '-v', '--verbose',
            help = 'increase output verbosity',
            action = 'count',
            default = 0
            )

        commands.append(
            UsagePattern(
                name,
                description = 'add a schedule',
                argparser = parser,
                task_class = 'ScheduleAdd'
            )
        )


        # dummy command
        # ----------------------------------------------- #

        name = 'dummy:local'

        parser = argparse.ArgumentParser(
            description = 'sledge {0} command'.format(name),
            usage = common_usage.format(name)
            )
        parser.add_argument(
            '-v', '--verbose',
            help = 'increase output verbosity',
            action = 'count',
            default = 0
            )

        commands.append(
            UsagePattern(
                name,
                description = 'a dummy command',
                argparser = parser,
                task_class = 'Dummy'
            )
        )


        # dummy command
        # ----------------------------------------------- #

        name = 'dummy:remote'
        description = 'a remote dummy command'
        execution = 'remote'

        parser = argparse.ArgumentParser(
            description = 'sledge {0} command'.format(name),
            usage = common_usage.format(name)
            )
        parser.add_argument(
            '-v', '--verbose',
            help = 'increase output verbosity',
            action = 'count',
            default = 0
            )

        commands.append(
            UsagePattern(
                name,
                description = 'a remote dummy command',
                argparser = parser,
                task_class = 'RemoteDummy'
            )
        )


        usage = PatternLoader.get_usage(commands)

        return commands, usage
