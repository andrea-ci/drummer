#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.classloader import ClassLoader
from .worker import Worker
import signal

class Runner(Worker):
    """ this worker executes commands and tasks"""

    def work(self):

        # get shared queue
        queue = self.queue

        running = True
        while running:

            # check for requests from listener
            if not queue.empty():

                # get the request
                task_executing = queue.get()

                task = task_executing.task

                # load class to exec
                classpath = 'tasks'
                classname = task.classname

                timeout = task.timeout
                params = task.params

                # run the task and get task result
                TaskToExec = ClassLoader().load(classpath, classname)
                task_result = TaskToExec().run(params)

                task_executing.terminated = True
                task_executing.result = task_result

                # queue_done
                queue.put(task_executing)

                # work is done
                running = False

        return


    def handler(signum, frame):
        """ timeout handler """
        raise Exception("task ended in timeout")
