#!/usr/bin/python3
# -*- coding: utf-8 -*-
from drummer.utils.filelogger import FileLogger
from drummer.workers import Runner
from datetime import datetime
import uuid

class TaskManager:
    """ manages tasks to be run """

    def __init__(self, config):

        self.config = config

        # get logger
        self.logger = FileLogger.get(config)

        # management of runners
        self.execution_data = []


    def run_task(self, queue_tasks_todo):
        """ pick a task from local queue and start runners """

        config = self.config
        logger = self.logger

        max_runners = config['max-runners']

        if not queue_tasks_todo.empty() and len(self.execution_data)<max_runners:

            # pick a task
            task_to_exec = queue_tasks_todo.get()
            logger.info('Task {0} is going to run with UID {1}'.format(task_to_exec.classname, task_to_exec.uid))

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
                'classname':    task_to_exec.classname,
                'uid':          task_to_exec.uid,
                'handle':       runner,
                'queue':        queue_runner_w2m,
                'timestamp':    datetime.now(),
                'timeout':      task_to_exec.timeout,
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

            self._cleanup_runners(idx_runners_to_terminate)

        return queue_tasks_done


    def check_timeouts(self):

        logger = self.logger

        for ii,runner_data in enumerate(self.execution_data):

            total_seconds = (datetime.now()-runner_data['timestamp']).total_seconds()

            if (total_seconds > runner_data['timeout']):
                # inserire dati del task
                logger.debug('Timeout exceeded, going to terminate task {0} (UID: {1})'.format(runner_data['classname'], runner_data['uid']))
                self._cleanup_runners([ii])

        return True


    def _cleanup_runners(self, idx_runners_to_terminate):
        """ clean-up: explicitly terminate runner processes and remove their queues """

        # clean handles
        execution_data = []
        for ii,execution in enumerate(self.execution_data):

            if ii in idx_runners_to_terminate:
                execution['handle'].terminate()
                execution['handle'].join()
            else:
                execution_data.append(execution)

        self.execution_data = execution_data

        return


class Task:

    def __init__(self):

        self.classname = None
        self.timeout = None
        self.params = None
        self.on_pipe = None
        self.on_done = None
        self.on_fail = None
        self.result = None


    @staticmethod
    def create_from_dict(classname, data):

        task = Task()

        task.classname = classname
        task.timeout = int(data['timeout'])
        task.params = data['parameters']
        task.on_pipe = data['onPipe']
        task.on_done = data['onSuccess']
        task.on_fail = data['onFail']

        return task


class TaskExecution(Task):
    """ TaskExecution is an active instance of a Task """

    def __init__(self, task, job_name):

        # get attributes from superclass
        self.classname = task.classname
        self.timeout = task.timeout
        self.params = task.params
        self.on_pipe = task.on_pipe
        self.on_done = task.on_done
        self.on_fail = task.on_fail
        self.result = task.result

        # execution attributes
        self.uid = uuid.uuid4()
        self.related_job = job_name
        self.result = None
