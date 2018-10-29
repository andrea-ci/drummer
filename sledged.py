#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from core.workers.listener import Listener
#from core.workers.scheduler import Scheduler
#from core.workers.eventrunner import EventRunner
from core.workers import Listener, Scheduler, EventRunner
from utils import Configuration, FileLogger, Queued
from core.foundation.tasking import TaskRunner
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
        task_runner = TaskRunner()

        # create job manager
        job_manager = JobManager()

        # create event runner
        event_runner = EventRunner()

        # start listener and scheduler workers
        #queue_listener_w2m, queue_listener_m2w  = Worker.from_classname('Listener')

        # [LISTENER]
        logger.debug('Starting Listener')
        listener = Listener()
        queue_listener_w2m, queue_listener_m2w = listener.get_queues()
        listener.start()
        pid = queue_listener_w2m.get()
        logger.debug('Listener successfully started with pid {0}'.format(pid))

        # [SCHEDULER]
        logger.debug('Starting Scheduler')
        scheduler = Scheduler()
        queue_scheduler_w2m = scheduler.get_queues()
        scheduler.start()
        pid = queue_scheduler_w2m.get()
        logger.debug('Scheduler successfully started with pid {0}'.format(pid))

        # handle runners
        #runner_conns = []
        #max_runners = 4

        # main loop
        while True:

            # check for messages from listener
            self.check_listener_requests(event_runner, queue_listener_w2m, queue_listener_m2w)

            # check for messages from scheduler
            job_manager = self.check_messages_from_scheduler(job_manager, queue_scheduler_w2m)

            # check task done
            queue_tasks_done = task_runner.load_task_result(queue_tasks_done)

            # check tasks to be executed
            queue_tasks_todo = task_runner.run_task(queue_tasks_todo)

            # update todo queue
            queue_tasks_todo, queue_tasks_done = job_manager.update_status(queue_tasks_todo, queue_tasks_done)

            # idle time
            sleep(idle_time)

        return


    def check_listener_requests(self, event_runner, queue_listener_w2m, queue_listener_m2w):

        logger = self.logger

        # check for requests from listener
        if not queue_listener_w2m.empty():

            # handle request from listener
            logger.debug('Serving a new request from console')

            # get the request
            request = queue_listener_w2m.get()

            # start a new runner
            logger.debug('Activating the EventRunner')

            response = event_runner.work(request)
            queue_listener_m2w.put(response)

        return


    def check_messages_from_scheduler(self, job_manager, queue_scheduler_w2m):

        logger = self.logger
        queue_tasks_todo = self.queue_tasks_todo

        while not queue_scheduler_w2m.empty():

            # handle request from scheduler
            logger.debug('A new job to execute has been sent from scheduler')

            # pick job to be executed
            job = queue_scheduler_w2m.get()

            # add job to be managed
            queue_tasks_todo = job_manager.add_job(job, queue_tasks_todo)

            #print(queue_tasks_todo.get())

        return job_manager


if __name__ == "__main__":

    sledged = Sledged()
    sledged.start()
