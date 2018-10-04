#!/usr/bin/python3
# -*- coding: utf-8 -*-
from commands import parser as console_parser
from utils.classloader import ClassLoader
from sys import argv as sys_argv

if __name__ == '__main__':

    # get request from console
    request = console_parser.process_input(sys_argv)

    # load command
    classpath = request.classpath
    classname = request.classname
    Command = ClassLoader().load(classpath, classname)

    # execute command
    response = Command().execute(request)

    print('Result: {0} -> {1}'.format(response.status, response.description))
