#!/usr/bin/env python3
import sched
import time
from extendertask import Task
from extenderjob import Job


class Extender(sched.scheduler):

    def __init__(self):

        # init scheduler
        super().__init__(time.time, time.sleep)

        # registered tasks
        self.tasks = []

        # scheduled jobs
        self.jobs = []


    def add_task(self, task_name, action_obj, task_description=''):

        # create task object
        new_task = Task(task_name, action_obj, task_description)

        # add to extender
        self.tasks.append( new_task )

        return new_task.uid


    def list_tasks():
        return self.tasks


    def add_job(self, task_uid, cronexp, job_description=''):

        # find task object
        task = [task for task in self.tasks if task.uid==task_uid][0]

        # create job object
        new_job = Job(task, cronexp)

        # add to extender
        self.jobs.append(new_job)

        return new_job.uid


    def execute(self, task_to_exec):
        """ executes immediately a task out of scheduling """
        pass


    def _ext_action(self, job):

        # get next exec time
        exec_time = job._get_exec_time()

        # schedule next job
        self.enterabs(exec_time, 1, self._ext_action, argument=(job,), kwargs={})

        # run the job
        job.run()


    def run(self):

        for job in self.jobs:

            # get next exec time
            exec_time = job._get_exec_time()

            # schedule next job
            self.enterabs(exec_time, 1, self._ext_action, argument=(job,), kwargs={})

        # run scheduled events
        super().run()
