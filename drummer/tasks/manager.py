# -*- coding: utf-8 -*-
from datetime import datetime
from drummer.workers import Runner
from drummer.messages import Response, StatusCode

class TaskManager:
    """Class for managing tasks to be run."""

    def __init__(self, config, logger):

        # get facilities
        self.config = config
        self.logger = logger

        # management of runners
        self.execution_data = []

    def run_tasks(self, queue_tasks_todo):
        """Picks a task from local queue and starts a new runner to execute it.

        Tasks are executed only if there are runners available (see max-runners
        parameter).
        """

        config = self.config
        logger = self.logger

        max_runners = config['max-runners']

        if not queue_tasks_todo.empty() and len(self.execution_data) < max_runners:

            # pick a task
            active_task = queue_tasks_todo.get()

            name = active_task.task.classname
            uid = active_task.uid
            logger.info(f'Task {name} is going to run with UID {uid}')

            # start a new runner for task
            logger.debug('Starting a new <Runner> process.')
            runner = Runner(config, logger, active_task)

            # get runner queue
            queue_runner_w2m = runner.get_queues()

            # start runner process
            runner.start()

            # get pid
            pid = queue_runner_w2m.get()
            logger.info(f'Runner has successfully started with pid {pid}.')

            # add task data object
            self.execution_data.append({
                'active_task':  active_task,
                'handle':       runner,
                'queue':        queue_runner_w2m,
                'timestamp':    datetime.now(),
                'timeout':      active_task.task.timeout,
            })

        return queue_tasks_todo

    def check_tasks(self, queue_tasks_done):
        """Loads task results from runners and save to local queue.
        Manages also tasks in timeout.
        """

        logger = self.logger
        idx_runners_to_terminate = []

        for ii, runner_data in enumerate(self.execution_data):

            # check task execution
            if not runner_data['queue'].empty():

                # pick the task
                executed = runner_data['queue'].get() # active_task
                task_name = runner_data['active_task'].task.classname
                uid = runner_data['active_task'].uid

                logger.info(f'Task {task_name} (UID {uid}) has terminated with result {executed.result.status}.')
                logger.info(f'Task {uid} says: {str(executed.result.data)}.')

                # update executed queue
                queue_tasks_done.put(executed)

                # prepare for cleanup
                idx_runners_to_terminate.append(ii)

            # check for task timeout
            else:
                total_seconds = (datetime.now() - runner_data['timestamp']).total_seconds()

                if (total_seconds > runner_data['active_task'].task.timeout):

                    classname = runner_data['active_task'].task.classname
                    uid = runner_data['active_task'].uid
                    logger.info(f'Timeout exceeded, task {classname} (UID: {uid}) will be terminated.')

                    # timeout gives error result
                    response = Response()
                    response.set_status(StatusCode.STATUS_ERROR)
                    response.set_data({'result': 'Task went in timeout.'})

                    # update executed queue
                    executed = runner_data['active_task']
                    executed.result = response
                    queue_tasks_done.put(executed)

                    # prepare for cleanup
                    idx_runners_to_terminate.append(ii)

        # clean-up finished runners
        if idx_runners_to_terminate:
            self._cleanup_runners(idx_runners_to_terminate)

        return queue_tasks_done

    def _cleanup_runners(self, idx_runners_to_terminate):
        """Performs clean-up of runners marked for termination.

        Runners are explicitly terminated and their queues are removed.
        """

        # clean handles
        execution_data = []
        for ii, execution in enumerate(self.execution_data):

            if ii in idx_runners_to_terminate:
                execution['handle'].terminate()
                execution['handle'].join()
            else:
                execution_data.append(execution)

        self.execution_data = execution_data
