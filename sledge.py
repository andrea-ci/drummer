#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import argv as sys_argv
from utils import ClassLoader
from console import ArgParser

if __name__ == '__main__':

    # get command from console
    classname, args = ArgParser().process(sys_argv)

    # load command
    Command = ClassLoader().load('console/commands', classname)

    # execute command
    Command().execute(args)
