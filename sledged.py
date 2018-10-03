#!/usr/bin/python3
# -*- coding: utf-8 -*-
from workers import Scheduler, Listener, Runner
from utils.filelogger import FileLogger
from multiprocessing import Pipe

class Sledged():

    def __init__(self):

        self.logger = FileLogger.get()


    def start_worker(self, WorkerClass):

        worker_name = WorkerClass.__name__

        logger = self.logger
        logger.info('Starting {0} worker'.format(worker_name))

        conn1, conn2 = Pipe()

        worker = WorkerClass(conn1)
        worker.start()

        pid = conn2.recv()

        logger.info('Worker {0} successfully started with pid {1}'.format(worker_name, pid))

        return conn2


    def start(self):

        # get logger
        logger = self.logger
        logger.info('Starting Sledged now...')

        # start workers
        master2socket = self.start_worker(Listener)
        master2scheduler = self.start_worker(Scheduler)

        while True:

            # check for requests from listener
            if master2socket.poll():

                logger.info('Serving a new request')

                # get the request
                request = master2socket.recv()

                # start a new runner
                master2runner = self.start_worker(Runner)

                # send request to runner
                master2runner.send(request)

                #print('received request:')
                #print(request)

                # send response
                master2socket.send('ok')

            # check messages from scheduler
            # pass


if __name__ == "__main__":

    sledged = Sledged()
    sledged.start()
