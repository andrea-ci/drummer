#!/usr/bin/env python3
from database.models.queue import QueueWriter
from croniter import croniter
from datetime import datetime
import time


class Job():
    """ Job with scheduling information """

    def __init__(self, classname, cronexp, task_chain):

        self.classname = classname

        # cron evaluation
        self.cron_obj = croniter(cronexp, datetime.now())


    def get_next_exec_time(self):

        # get next execution absolute time
        cron_time = self.cron_obj.get_next(datetime)
        next_exec_time = time.mktime(cron_time.timetuple())

        return next_exec_time


    def run(self):

        print('running')

        data = dict()
        data['classname'] = self.classname
        data['parameters'] = ''

        qw = QueueWriter()

        qw.create_session()
        qw.set_queue(data)
        qw.close_session()

        return
