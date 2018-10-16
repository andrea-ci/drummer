#!/usr/bin/python3
# -*- coding: utf-8 -*-
import uuid

class TaskExecution:

    def __init__(self, task, job_name):

        self.uid = uuid.uuid4()

        self.task = task
        self.related_job = job_name

        self.result = None
