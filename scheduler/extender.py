#!/usr/bin/python3
# -*- coding: utf-8 -*-
from database.models.schedule import ScheduleReader
from scheduler.jobs import Job
import sched
import time

class Extender(sched.scheduler):

    def __init__(self):

        # init scheduler
        super().__init__(time.time, time.sleep)

        self.jobs = []


    def load_jobs(self):
        """ build job objects from database schedules """

        schedules = self.load_schedules()

        for schedule in schedules:

            name = schedule[0]
            cronexp = schedule[1]
            task_chain = schedule[2]

            # create a job object
            job = Job(name, cronexp, task_chain)

            self.jobs.append(job)


    def load_schedules(self):
        """ load schedules from database """

        # init schedule reader and get schedules
        schedule_reader = ScheduleReader()

        schedule_reader.create_session()

        schedules = []
        for schedule in schedule_reader.get_all():
            # only enabled schedules
            if schedule[3]:
                schedules.append(schedule)

        schedule_reader.close_session()

        return schedules


    def ext_action(self, job):

        # get next exec time
        exec_time = job.get_next_exec_time()

        # schedule next job
        self.enterabs(exec_time, 1, self.ext_action, argument=(job,), kwargs={})

        # run current job
        job.run()


    def run(self):

        # init job schedulation
        for job in self.jobs:

            # get next exec time
            exec_time = job.get_next_exec_time()

            # schedule next job
            self.enterabs(exec_time, 1, self.ext_action, argument=(job,), kwargs={})

        # run scheduled events
        super().run()
