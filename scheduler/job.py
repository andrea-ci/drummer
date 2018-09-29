#!/usr/bin/env python3
from croniter import croniter
from datetime import datetime
import uuid
import time

class Job():

    def __init__(self, task, cronexp):

        self.uid = uuid.uuid4()

        self.task = task

        self._cronexp = cronexp

        # cron evaluation
        _base = datetime.now()
        self._croniter = croniter(self._cronexp, _base)


    def _get_exec_time(self):

        # get next execution absolute time
        dt_obj = self._croniter.get_next(datetime)

        return time.mktime(dt_obj.timetuple())


    def run(self):

        # execute task
        res = self.task._action_obj.run()
        return
