#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.filelogger import FileLogger
from core.workers.runner import Runner
from datetime import datetime
import uuid

class TaskManager:
    """ manages tasks to be run """

    def __init__(self):

        # get logger
        self.logger = FileLogger.get()

        # management of runners
        self.execution_data = []


    def run_task(self, queue_tasks_todo):
        """ pick a task from local queue and start runners """

        logger = self.logger

        if not queue_tasks_todo.empty():

            # pick a task
            task_to_exec = queue_tasks_todo.get()
            logger.info('Task {0} is going to run with UID {1}'.format(task_to_exec.task.classname, task_to_exec.uid))

            # start a new runner for task
            logger.debug('Starting Runner')
            runner = Runner(task_to_exec)

            # get runner queue
            queue_runner_w2m = runner.get_queues()

            # start runner process
            runner.start()

            # get pid
            pid = queue_runner_w2m.get()
            logger.info('Runner successfully started with pid {0}'.format(pid))

            # add task data object
            self.execution_data.append({
                'classname':    task_to_exec.task.classname,
                'uid':          task_to_exec.uid,
                'handle':       runner,
                'queue':        queue_runner_w2m,
                'timestamp':    datetime.now(),
                'timeout':      task_to_exec.task._timeout,
            })

        return queue_tasks_todo


    def load_results(self, queue_tasks_done):
        """ load task result from runners and save to local queue """

        logger = self.logger

        idx_runners_to_terminate = []

        # check tasks executed by runners
        for ii,execution in enumerate(self.execution_data):

            if not execution['queue'].empty():

                # pick the task
                task_result = execution['queue'].get()
                logger.info('Task {0} (UID {1}) ended with result {2}'.format(
                    execution['classname'],
                    execution['uid'],
                    task_result.result.status
                ))

                # update done queue
                queue_tasks_done.put(task_result)

                # prepare runners to clean
                idx_runners_to_terminate.append(ii)

        # clean-up finished runners
        if idx_runners_to_terminate:

            logger.debug('Going to clean-up finished runners')
            self._cleanup_runners(idx_runners_to_terminate)

        return queue_tasks_done


    def check_timeouts(self):

        for ii,runner_data in enumerate(self.execution_data):

            total_seconds = (datetime.now()-runner_data['timestamp']).total_seconds()

            if (total_seconds > runner_data['timeout']):
                # inserire dati del task
                logger.debug('Timeout exceeded, going to terminate task {0} (UID: {1})'.format(runner_data['classname'], runner_data['uid']))
                self._cleanup_runners([ii])

        return True

        
    def _cleanup_runners(self, idx_runners_to_terminate):
        """ clean-up: explicitly terminate runner processes and remove their queues """

        logger = self.logger

        logger.debug('Num. of runners before cleaning: {0}'.format(len(self.execution_data)))

        # clean handles
        execution_data = []
        for ii,execution in enumerate(self.execution_data):

            if ii in idx_runners_to_terminate:
                execution['handle'].terminate()
            else:
                execution_data.append(execution)

        self.execution_data = execution_data

        logger.debug('Num. of runners after cleaning: {0}'.format(len(self.execution_data)))

        return


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
