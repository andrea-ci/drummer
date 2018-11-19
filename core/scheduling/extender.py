#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.database import SqliteSession, Schedule
from core.foundation.jobs import Job
import sched
import time

class Extender(sched.scheduler):

    def __init__(self, message_queue):

        # init scheduler
        super().__init__(time.time, time.sleep)
        # threading queue
        self.message_queue = message_queue
        # list of jobs
        self.jobs = []


    def load_jobs(self):
        """ build job objects from database schedules """

        schedules = self.load_schedules()

        for schedule in schedules:

            # create a job object
            job = Job(schedule)

            self.jobs.append(job)


    def load_schedules(self):
        """ load enabled schedules from database """

        # get all enabled schedules
        session = SqliteSession.create()

        schedules = session.query(Schedule).filter(Schedule.enabled==True).all()

        session.close()

        return schedules


    def ext_action(self, job):
        """ re-schedules next execution time and writes into the scheduler queue """

        # get next exec time
        exec_time = job.get_next_exec_time()

        # schedule next job
        self.enterabs(exec_time, 1, self.ext_action, argument=(job,), kwargs={})

        # write to the queue
        self.message_queue.put(job)

        return


    def run(self):

        # create job objects
        for job in self.jobs:

            # get next exec time of job
            exec_time = job.get_next_exec_time()

            # enter next schedulation
            self.enterabs(exec_time, 1, self.ext_action, argument=(job,), kwargs={})

        # run scheduled events
        super().run()
