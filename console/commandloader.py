#!/usr/bin/python3
# -*- coding: utf-8 -*-

class CommandException(Exception):
    pass


class CommandLoader:

    @staticmethod
    def execute(command, args = {}):

        try:

            # get command classname
            class_name = command.task_class

            # import the right command
            mod_to_import = 'core.commands.{0}'.format(class_name.lower())
            mod = __import__(mod_to_import, fromlist=[command.task_class])
            CommandClass = getattr(mod, command.task_class)

        except:
            raise CommandException('unable to load command')

        # execute the command
        response = CommandClass().execute(args)

        return response
