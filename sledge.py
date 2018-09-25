#!/usr/bin/python3
# -*- coding: utf-8 -*-
from console import parser as console_parser
from console.commandloader import CommandLoader
from utils.filelogger import FileLogger
from sys import argv as sys_argv

if __name__ == '__main__':

    # get logger
    logger = FileLogger.get()

    # parse console input
    command, args = console_parser.process_input(sys_argv)

    # execute command
    response = CommandLoader.execute(command, args)

    """
    # create request
    request = Request(command, args)

    response = Router().perform_request(request)

    # send serialized request
    response = SocketClient().send(request)

    print(response)
    """
