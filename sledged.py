#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from core.workers import Listener
from scheduling import Scheduler
from utils import Configuration, FileLogger, Queued, ClassLoader
from core.foundation import TaskManager, JobManager
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

        # create scheduler package
        self.scheduler_bundle = self.create_scheduler()

        # create listener package
        self.listener_bundle = self.create_listener()


    def start(self):

        # [INIT]
        # ----------------------------------------------- #

        # get logger
        logger = self.logger
        logger.info('Starting Sledged service now...')

        # load internal queues
        queue_tasks_todo = self.queue_tasks_todo
        queue_tasks_done = self.queue_tasks_done

        # load config
        idle_time = self.config['idle-time']

        # create task runner
        task_manager = TaskManager()

        # create job manager
        job_manager = JobManager()

        # handle runners
        #runner_conns = []
        #max_runners = 4


        # [MAIN LOOP]
        # ----------------------------------------------- #
        while True:

            # [HEALTH CHECK]
            # ----------------------------------------------- #

            # check scheduler
            if not self.scheduler_bundle['handle'].is_alive():

                # create new scheduler
                self.logger.warning('Scheduler has exited, going to restart it')
                self.scheduler_bundle = self.create_scheduler()

            # check listener
            if not self.listener_bundle['handle'].is_alive():

                # create new listener
                self.logger.warning('Listener has exited, going to restart it')
                self.listener_bundle = self.create_listener()


            # [MESSAGE CHECK]
            # ----------------------------------------------- #

            # check for messages from listener
            self.check_messages_from_listener()

            # check for messages from scheduler
            job_manager = self.check_messages_from_scheduler(job_manager)


            # [TASK/JOB CHECK]
            # ----------------------------------------------- #

            # check for finished tasks
            queue_tasks_done = task_manager.load_results(queue_tasks_done)

            # check for task timeouts
            task_manager.check_timeouts()

            # check tasks to be executed
            queue_tasks_todo = task_manager.run_task(queue_tasks_todo)

            # update todo queue
            queue_tasks_todo, queue_tasks_done = job_manager.update_status(queue_tasks_todo, queue_tasks_done)


            # idle time
            sleep(idle_time)

        return


    def load_event(self, request):

        # load event class to exec
        classname = request.classname
        classpath = request.classpath

        # execute the event and get result
        EventToExec = ClassLoader().load(classpath, classname)
        response, follow_up = EventToExec().execute(request)

        return response, follow_up


    def check_messages_from_listener(self):

        logger = self.logger

        # get listener components
        listener_bundle = self.listener_bundle
        listener_queue_w2m = listener_bundle['queue_w2m']

        # check for requests from listener
        if not listener_queue_w2m.empty():

            # handle request from listener
            logger.info('Serving a new request from console')

            # get the request
            request = listener_queue_w2m.get()

            # run the request
            response, follow_up = self.load_event(request)

            # send the response
            listener_queue_m2w = listener_bundle['queue_m2w']
            listener_queue_m2w.put(response)

            # process the event follow-up
            if follow_up.action:
                self.process_follow_up(follow_up)

        return


    def check_messages_from_scheduler(self, job_manager):

        logger = self.logger

        scheduler_bundle = self.scheduler_bundle
        scheduler_queue_w2m = scheduler_bundle['queue_w2m']

        queue_tasks_todo = self.queue_tasks_todo

        while not scheduler_queue_w2m.empty():

            # pick job to be executed
            job = scheduler_queue_w2m.get()

            # handle request from scheduler
            logger.info('Job {0} is going to be executed'.format(job))

            # add job to be managed
            queue_tasks_todo = job_manager.add_job(job, queue_tasks_todo)

        return job_manager


    def create_listener(self):

        logger = self.logger
        logger.info('Starting Listener')

        listener = Listener()
        listener_queue_w2m, listener_queue_m2w = listener.get_queues()

        listener.start()
        pid = listener_queue_w2m.get()

        logger.info('Listener successfully started with pid {0}'.format(pid))

        listener_bundle = {
            'handle': listener,
            'queue_w2m': listener_queue_w2m,
            'queue_m2w': listener_queue_m2w,
        }

        return listener_bundle


    def create_scheduler(self):

        logger = self.logger
        logger.info('Starting Scheduler')

        scheduler = Scheduler()
        scheduler_queue_w2m = scheduler.get_queues()

        scheduler.start()
        pid = scheduler_queue_w2m.get()

        logger.info('Scheduler successfully started with pid {0}'.format(pid))

        scheduler_bundle = {
            'handle': scheduler,
            'queue_w2m': scheduler_queue_w2m
        }
        return scheduler_bundle


    def process_follow_up(self, follow_up):

        scheduler_bundle = self.scheduler_bundle

        if follow_up.action == 'RELOAD':

            self.logger.info('Schedulation has changed, restarting Scheduler')

            # terminate current scheduler
            scheduler_bundle['handle'].terminate()
            scheduler_bundle['handle'].join()

            # start new scheduler
            self.scheduler_bundle = self.create_scheduler()

        elif follow_up.action == 'EXECUTE':
            pass

        return


if __name__ == "__main__":

    sledged = Sledged()
    sledged.start()
