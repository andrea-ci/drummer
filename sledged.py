#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation import JobManager, TaskRunner
from utils import Configuration, FileLogger, Queued
from core.workers import Worker
from time import sleep

class Sledged:

    def __init__(self):

        # get logger
        self.logger = FileLogger.get()

        # get configuration
        self.config = Configuration.load()

        # create task queues
        self.queue_tasks_todo = Queued()
        self.queue_tasks_done = Queued()


    def start(self):

        # get logger
        logger = self.logger
        logger.info('Starting Sledged service now...')

        # load config
        idle_time = self.config['idle-time']

        # load internal queues
        queue_tasks_todo = self.queue_tasks_todo
        queue_tasks_done = self.queue_tasks_done

        # create task runner
        task_runner = TaskRunner()

        # create job manager
        job_manager = JobManager()

        # start listener and scheduler workers
        queue_listener = Worker.from_classname('Listener')
        queue_scheduler = Worker.from_classname('Scheduler')

        # handle runners
        #runner_conns = []
        #max_runners = 4

        # main loop
        while True:

            # check for messages from listener
            self.check_messages_from_listener(queue_listener)

            # check for messages from scheduler
            job_manager = self.check_messages_from_scheduler(job_manager, queue_scheduler)

            # check task done
            queue_tasks_done = task_runner.load_task_result(queue_tasks_done)

            # check tasks to be executed
            queue_tasks_todo = task_runner.run_task(queue_tasks_todo)

            # update todo queue
            queue_tasks_todo, queue_tasks_done = job_manager.update_status(queue_tasks_todo, queue_tasks_done)

            # idle time
            sleep(idle_time)

        return


    def check_messages_from_listener(self, queue_listener):

        logger = self.logger

        # check for requests from listener
        if not queue_listener.empty():

            # handle request from listener
            logger.debug('Serving a new request from console')

            # get the request
            request = queue_listener.get()

            # start a new runner
            logger.debug('Creating a new runner instance')
            conn_event_runner = Worker.from_classname('Runner')

            # send request to runner
            conn_event_runner.send(request)

            # get response from runner
            response = conn_event_runner.recv()

            # send response to listener
            queue_listener.send(response)

        return


    def check_messages_from_scheduler(self, job_manager, queue_scheduler):

        logger = self.logger
        queue_tasks_todo = self.queue_tasks_todo

        while not queue_scheduler.empty():

            # handle request from scheduler
            logger.debug('A new job to execute has been sent from scheduler')

            # pick job to be executed
            job = queue_scheduler.get()

            # add job to be managed
            queue_tasks_todo = job_manager.add_job(job, queue_tasks_todo)

            #print(queue_tasks_todo.get())

        return job_manager





if __name__ == "__main__":

    sledged = Sledged()
    sledged.start()
