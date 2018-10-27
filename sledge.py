#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.classloader import ClassLoader
from sys import argv as sys_argv
from console import ArgParser

if __name__ == '__main__':

    # get request from console
    request = ArgParser().process(sys_argv)

    # load command
    classpath = request.classpath
    classname = request.classname
    Command = ClassLoader().load(classpath, classname)

    # execute command
    response = Command().execute(request)

    if response:
        print('Result: {0} -> {1}'.format(response.status, response.description))
