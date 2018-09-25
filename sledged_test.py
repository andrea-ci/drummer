#!/usr/bin/python3
# -*- coding: utf-8 -*-
from multiprocessing import Process, Pipe
from utils.filelogger import FileLogger
from workers.scheduler import Scheduler
from workers.listener import Listener
from workers.runner import Runner


if __name__ == "__main__":

    # pipe between master and listener
    m2s_conn, s2m_conn = Pipe()

    # start socket listener
    listener = Listener(s2m_conn)
    listener.start()

    while True:

        # check messages from console
        if m2s_conn.poll():

            print('processing a new request')
            request = m2s_conn.recv()

            print('command: {0}'.format(request.body['command']))
            print('params: {0}'.format(request.body['parameters']))

            # pipe between master and runner
            m2r_conn, r2m_conn = Pipe()

            # start runner
            runner = Runner(r2m_conn, request)
            runner.start()

            # get response from runner
            response = m2r_conn.recv()
            m2r_conn.close()

            # send response to console
            m2s_conn.send(response)


        # check messages from scheduler
        # pass
