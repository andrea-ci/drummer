#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from core.workers import Listener, Scheduler, EventRunner
from utils import Configuration, FileLogger, Queued
from core.foundation.tasks import TaskManager
from core.foundation.jobs import JobManager
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
        task_manager = TaskManager()

        # create job manager
        job_manager = JobManager()

        # create event runner
        event_runner = EventRunner()

        # [LISTENER]
        listener, queue_listener_w2m, queue_listener_m2w = self.create_listener()

        # [SCHEDULER]
        scheduler, queue_scheduler_w2m = self.create_scheduler()

        # handle runners
        #runner_conns = []
        #max_runners = 4

        # main loop
        while True:

            # check scheduler
            scheduler, queue_scheduler_w2m = self.check_scheduler(scheduler, queue_scheduler_w2m)

            # check listener
            listener, queue_listener_w2m, queue_listener_m2w = self.check_listener(listener, queue_listener_w2m, queue_listener_m2w)

            # check for messages from listener
            self.check_messages_from_listener(event_runner, queue_listener_w2m, queue_listener_m2w)

            # check for messages from scheduler
            job_manager = self.check_messages_from_scheduler(job_manager, queue_scheduler_w2m)

            # check task done
            queue_tasks_done = task_manager.load_results(queue_tasks_done)

            # check tasks to be executed
            queue_tasks_todo = task_manager.run_task(queue_tasks_todo)

            # update todo queue
            queue_tasks_todo, queue_tasks_done = job_manager.update_status(queue_tasks_todo, queue_tasks_done)

            # idle time
            sleep(idle_time)

        return


    def check_messages_from_listener(self, event_runner, queue_listener_w2m, queue_listener_m2w):

        logger = self.logger

        # check for requests from listener
        if not queue_listener_w2m.empty():

            # handle request from listener
            logger.info('Serving a new request from console')

            # get the request
            request = queue_listener_w2m.get()

            # run the request
            response = event_runner.work(request)

            # send the response
            queue_listener_m2w.put(response)

        return


    def check_messages_from_scheduler(self, job_manager, queue_scheduler_w2m):

        logger = self.logger

        queue_tasks_todo = self.queue_tasks_todo

        while not queue_scheduler_w2m.empty():

            # pick job to be executed
            job = queue_scheduler_w2m.get()

            # handle request from scheduler
            logger.info('Job {0} is going to be executed'.format(job))

            # add job to be managed
            queue_tasks_todo = job_manager.add_job(job, queue_tasks_todo)

            #print(queue_tasks_todo.get())

        return job_manager


    def create_listener(self):

        logger = self.logger
        logger.info('Starting Listener')

        listener = Listener()
        queue_listener_w2m, queue_listener_m2w = listener.get_queues()

        listener.start()
        pid = queue_listener_w2m.get()

        logger.info('Listener successfully started with pid {0}'.format(pid))

        return listener, queue_listener_w2m, queue_listener_m2w


    def create_scheduler(self):

        logger = self.logger
        logger.info('Starting Scheduler')

        scheduler = Scheduler()
        queue_scheduler_w2m = scheduler.get_queues()

        scheduler.start()
        pid = queue_scheduler_w2m.get()

        logger.info('Scheduler successfully started with pid {0}'.format(pid))

        return scheduler, queue_scheduler_w2m


    def check_listener(self, listener, queue_listener_w2m, queue_listener_m2w):

        if not listener.is_alive():
            self.logger.warning('Listener has exited, going to restart')
            listener, queue_listener_w2m, queue_listener_m2w = self.create_listener()

        return listener, queue_listener_w2m, queue_listener_m2w


    def check_scheduler(self, scheduler, queue_scheduler_w2m):

        if not scheduler.is_alive():

            self.logger.warning('Scheduler has exited, going to restart')
            scheduler, queue_scheduler_w2m = self.create_scheduler()

        return scheduler, queue_scheduler_w2m


if __name__ == "__main__":

    sledged = Sledged()
    sledged.start()
