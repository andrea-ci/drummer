#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from utils.classloader import ClassLoader
from sys import argv as sys_argv
from console import ArgParser

if __name__ == '__main__':

    # get command from console
    classname, params = ArgParser().process(sys_argv)

    # load command
    Command = ClassLoader().load('console/commands', classname)

    # execute command
    Command().execute(params)
