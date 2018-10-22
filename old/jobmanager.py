#!/usr/bin/python3
# -*- coding: utf-8 -*-
#from .taskexecution import TaskExecution
from .tasking import TaskExecution
from .messages import StatusCode
from utils import FileLogger

class JobManager:
    """ manages status of jobs to be executed """

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

                # get job object
                job = self.get_job_by_name(executed_task.related_job)

                queue_tasks_todo = self.add_to_queue(job, next_task, queue_tasks_todo)

            else:
                self.remove_job(executed_task.related_job)

        return queue_tasks_todo, queue_tasks_done


    def get_next_task(self, executed_task):

        # init next task classname
        next_task = None

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
            pass

        return next_task


    def get_job_by_name(self, job_name):

        job = [j for j in self.jobs if j._name == job_name][0]

        return job


    def remove_job(self, job_name):

        idx = [ii for ii in range(len(self.jobs)) if self.jobs[ii]._name == job_name][0]

        del self.jobs[idx]

        return
