#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.filelogger import FileLogger
from core.sockets.client import SocketClient
from core.sockets.messages import Message

class RemoteDummy():

    def execute(self, parameters):

        logger = FileLogger.get()

        logger.info('starting remote-dummy command')

        # send request to socket server
        request = (
            Message()
            .add_entry('type', 'request')
            .add_entry('content', 'ciao ciao')
            .add_entry('exec_path', '/opt/sledge/tasks/remotedummy')
            .add_entry('parameters', 'verbose')
            .to_bytes()
        )

        sc = SocketClient()
        response = sc.send(request)

        print(Message.from_bytes(response))
