#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation.tasking import Task, TaskExecution
from core.foundation.messages import StatusCode
from datetime import datetime
from croniter import croniter
from utils import FileLogger
import json
import time


class JobManager:
    """ Manage status of jobs to be executed """

    def __init__(self):

        # get logger
        self.logger = FileLogger.get()

        # managed jobs
        self.jobs = []


    def add_job(self, job, queue_tasks_todo):
        """ add the job to be executed """

        # update job list
        self.jobs.append(job)

        # send to queue the first task
        root_classname = job.get_root()

        queue_tasks_todo = self.add_to_queue(job, root_classname, queue_tasks_todo)

        return queue_tasks_todo


    def add_to_queue(self, job, classname, queue_tasks_todo):
        """ add a new task to todo queue """

        # get task data
        task = job.get_task_data(classname)

        task_execution = TaskExecution(task, job._name)

        queue_tasks_todo.put(task_execution)

        return queue_tasks_todo


    def update_status(self, queue_tasks_todo, queue_tasks_done):
        """ load task results and update job status"""

        while not queue_tasks_done.empty():

            # get task executed
            executed_task = queue_tasks_done.get()

            next_task = self.get_next_task(executed_task)

            if next_task:

                # add next task to todo queue
                job = self.get_job_by_name(executed_task.related_job)
                queue_tasks_todo = self.add_to_queue(job, next_task, queue_tasks_todo)

            else:
                # job is finished, remove it
                self.remove_job(executed_task.related_job)

        return queue_tasks_todo, queue_tasks_done


    def get_next_task(self, executed_task):
        """ get next task to be executed within job """

        # take result of executed task
        result = executed_task.result

        # check result consistency
        if result.status not in (StatusCode.STATUS_OK, StatusCode.STATUS_WARNING, StatusCode.STATUS_ERROR):
            raise Exception('Status code not supported')

        # get next task classname
        # if job is finished next task is None
        if executed_task.task._on_pipe:
            next_task = executed_task.task._on_pipe

        elif executed_task.task._on_done and result.status == StatusCode.STATUS_OK:
            next_task = executed_task.task._on_done

        elif executed_task.task._on_fail and result.status == StatusCode.STATUS_ERROR:
            next_task = executed_task.task._on_fail

        else:
            # no more tasks to execute
            next_task = None

        return next_task


    def get_job_by_name(self, job_name):
        """ get job by name """

        job = [j for j in self.jobs if j._name == job_name][0]

        return job


    def remove_job(self, job_name):
        """ remove a job by name """

        idx = [ii for ii in range(len(self.jobs)) if self.jobs[ii]._name == job_name][0]
        del self.jobs[idx]

        return


class Job:
    """ Job object used for manipulation from/to from schedules """

    def __init__(self, schedule):
        """ takes schedule entity """

        # job name/description
        self._name = schedule.name
        self._description = schedule.description
        # job root task and task data
        self._root, self._tasks = self._set_task_data(schedule.parameters)
        # job cron
        self._cron = croniter(schedule.cronexp, datetime.now())
        # job enabled flag
        self._enabled = schedule.enabled
        # job status
        self._terminated = False


    def __str__(self):
        return '{0} - {1}'.format(self._name, self._description)

    def __eq__(self, other):
        return self._name == other._name


    def _set_task_data(self, parameters):

        parameters = json.loads(parameters)

        root_task = parameters['root']

        task_data = parameters['tasklist']

        tasks = []
        for tsk in task_data:

            # build task
            task_dict = task_data[tsk]
            task = Task.create_from_dict(tsk, task_dict)

            tasks.append(task)

        return root_task, tasks


    def get_root(self):
        return self._root


    def get_task_data(self, classname):

        task_data = [tsk for tsk in self._tasks if tsk.classname==classname][0]

        return task_data


    def get_next_exec_time(self):

        # get next execution absolute time
        cron_time = self._cron.get_next(datetime)
        next_exec_time = time.mktime(cron_time.timetuple())

        return next_exec_time
