#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.database import QueueManager
from croniter import croniter
from datetime import datetime
from .task import Task
import json
import time

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

            task_dict = task_data[tsk]

            task = Task()
            task.classname = tsk
            task.timeout = task_dict['timeout']
            task.params = task_dict['parameters']
            task.on_pipe = task_dict['onPipe']
            task.on_done = task_dict['onSuccess']
            task.on_fail = task_dict['onFail']

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
