#!/usr/bin/python3
# -*- coding: utf-8 -*-
from workers.workermanager import WorkerManager
from utils.filelogger import FileLogger
from time import sleep

class Sledged():

    def __init__(self):
        self.logger = FileLogger.get()


    def start(self):

        # get logger
        logger = self.logger
        logger.info('Starting Sledged now...')

        worker_manager = WorkerManager()

        # start listener and scheduler
        master2socket = worker_manager.create_worker('Listener')
        master2scheduler = worker_manager.create_worker('Scheduler')

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
                conn_socketrunner = worker_manager.create_worker('Runner')

                # send request to runner
                conn_socketrunner.send(request)

                # get response from runner
                response = conn_socketrunner.recv()

                # send response to listener
                master2socket.send(response)


            # check status of scheduler

            # check
            if len(runner_conns)>0:
                for conn in runner_conns:
                    pass

            # idle time
            sleep(0.5)


if __name__ == "__main__":

    sledged = Sledged()
    sledged.start()
