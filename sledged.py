#!/usr/bin/python3
# -*- coding: utf-8 -*-
from workers import Scheduler, Listener, Runner
from multiprocessing import Process, Pipe
from utils.filelogger import FileLogger


if __name__ == "__main__":

    import sys
    print(sys.path)
    exit()

    
    # pipe between master and listener
    conn_m2s, conn_s2m = Pipe()

    # start socket listener
    listener = Listener(conn_s2m)
    listener.start()

    while True:

        # check messages from console
        if conn_m2s.poll():

            print('processing a new request')
            request = conn_m2s.recv()

            print('received request:')
            print(request)

            """
            # pipe between master and runner
            conn_m2r, conn_r2m = Pipe()

            # start runner
            runner = Runner(conn_r2m, request)
            runner.start()

            # get response from runner
            response = conn_m2r.recv()
            conn_m2r.close()

            # send response to console
            conn_m2s.send(response)
            """

        # check messages from scheduler
        # pass
