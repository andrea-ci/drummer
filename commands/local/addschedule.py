#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base import Configuration, Message
from sys import exit as sys_exit
from croniter import croniter
from core.sockets.client import SocketClient

class AddSchedule():

    def execute(self, args):

        # test socket connection

        # get job information
        name = input('Name of the Job: ')
        description = input('Brief description: ')

        # cron expression
        cronexp = input('Cron expression: ')

        if not croniter.is_valid(cronexp):
            print('cron expression not valid')
            sys_exit()

        config = Configuration.load()
        MSG_LEN = config['socket']['message_len']

        # prepare message
        message = Message()
        message.add_entry('type', 'command')
        message.add_entry('class_name', 'JobAdd')
        message.add_entry('name', name)
        message.add_entry('description', description)
        message.add_entry('cronexp', cronexp)
        data = message.to_bytes(MSG_LEN)

        # send message to listener
        sc = SocketClient()
        response = sc.send_request(data)

        print(response)
