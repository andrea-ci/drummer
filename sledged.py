#!/usr/bin/python3
# -*- coding: utf-8 -*-
from workers import Scheduler, Listener, Runner
from utils.filelogger import FileLogger
from multiprocessing import Pipe
from time import sleep

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

        # start listener and scheduler
        master2socket = self.start_worker(Listener)
        master2scheduler = self.start_worker(Scheduler)

        # handle runners
        runner_conns = []
        max_runners = 4

        while True:

            # check for requests from listener
            if master2socket.poll():

                # handle request from listener
                logger.info('Serving a new request from console')

                # get the request
                request = master2socket.recv()

                # start a new runner
                m2socketrunner = self.start_worker(Runner)

                # send request to runner
                m2socketrunner.send(request)

                # get response from runner
                response = m2socketrunner.recv()

                # send response to listener
                master2socket.send(response)


            # check messages from scheduler
            if master2scheduler.poll():

                # handle request from listener
                logger.info('Starting a new request from scheduler')

                # get the request
                request = master2scheduler.recv()

            # check
            if len(runner_conns)>0:
                for conn in runner_conns:
                    pass

            # idle time
            sleep(0.5)


if __name__ == "__main__":

    sledged = Sledged()
    sledged.start()
