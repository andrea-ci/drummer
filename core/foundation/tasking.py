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
            task_to_exec = queue_tasks_todo.get()
            logger.debug('Task {0} is going to run with UID {1}'.format(task_to_exec.task.classname, task_to_exec.uid))

            # start a new runner for task
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
                executed_task = q.get()
                logger.debug('Task ended with result {0}'.format(executed_task.result.status))

                queue_tasks_done.put(executed_task)

        return queue_tasks_done


class TaskExecution:

    def __init__(self, task, job_name):

        self.uid = uuid.uuid4()

        self.task = task
        self.related_job = job_name

        self.result = None


class Task:

    def __init__(self):

        self._classname = None
        self._timeout = None
        self._params = None
        self._on_pipe = None
        self._on_done = None
        self._on_fail = None
        self._terminated = False
        self._result = None
        self._uid = None


    @staticmethod
    def create_from_dict(classname, data):

        task = Task()

        task.classname = classname
        task.timeout = data['timeout']
        task.params = data['parameters']
        task.on_pipe = data['onPipe']
        task.on_done = data['onSuccess']
        task.on_fail = data['onFail']

        return task


    @property
    def classname(self):
        return self._classname
    @classname.setter
    def classname(self, value):
        self._classname = value

    @property
    def timeout(self):
        return self._timeout
    @timeout.setter
    def timeout(self, value):
        self._timeout = int(value)

    @property
    def on_pipe(self):
        return self._on_pipe
    @on_pipe.setter
    def on_pipe(self, value):
        self._on_pipe = value

    @property
    def on_done(self):
        return self._on_done
    @on_done.setter
    def on_done(self, value):
        self._on_done = value

    @property
    def on_fail(self):
        return self._on_fail
    @on_fail.setter
    def on_fail(self, value):
        self._on_fail = value

    @property
    def params(self):
        return self._params
    @params.setter
    def params(self, value):
        self._params = value
