#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.filelogger import FileLogger
from core.workers import Worker
import uuid

class TaskRunner:
    """ manages tasks to be run """

    def __init__(self):

        # get logger
        self.logger = FileLogger.get()

        # list of queues with runners
        self.runners = []


    def run_task(self, queue_tasks_todo):
        """ pick a task from local queue and start runners """

        logger = self.logger

        if not queue_tasks_todo.empty():

            # pick the task
            logger.debug('Get a new task to run')
            task_to_exec = queue_tasks_todo.get()

            # start a new runner
            logger.debug('Creating a new runner instance')

            # run the task
            queue_runner = Worker.from_classname('Runner')
            queue_runner.put(task_to_exec)

            self.runners.append(queue_runner)

        return queue_tasks_todo


    def load_task_result(self, queue_tasks_done):
        """ load task result from runners and save to local queue """

        logger = self.logger

        # check runners' results
        for q in self.runners:

            if not q.empty():

                # pick the task
                logger.debug('Get a new task result')
                executed_task = q.get()

                queue_tasks_done.put(executed_task)

        return queue_tasks_done
