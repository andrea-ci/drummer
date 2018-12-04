#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from drummer.utils import ClassLoader
from drummer.console import ArgParser

class Drummer:

    def start(self, sys_argv):

        # get command from console
        classname, args = ArgParser().process(sys_argv)

        # load command
        Command = ClassLoader().load('drummer/console/commands', classname)

        # execute command
        Command().execute(args)
