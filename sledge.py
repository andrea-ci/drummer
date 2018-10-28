#!/usr/bin/env python3
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
    Command().execute(request)
