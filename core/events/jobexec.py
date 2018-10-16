#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation import Response, StatusCode
from core.database import QueueManager

class JobExec:

    def execute(self, job):
        """ takes the job to execute from scheduler """

        try:

            # get job data
            job_data = request.data
            job_name = job_data.get('name')
            job_parameters = job_data.get('parameters')


            """
            qui dobbiamo estrarre le informazioni del job e in particolare:
                - l'elenco dei task da eseguire
                - il flusso logico da seguire per decidere l'ordine di esecuzione
                - i parametri dei task (per es. il timeout)
            """


            # wait for task result

            # queue next task

            # end job


        except Exception:

            response.set_status(StatusCode.STATUS_ERROR)
            response.set_description('Impossible to add schedule')

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_description('Schedule has been added!')

        return response


    def get_task_parameters(self, task):

        # first task to be executed
        root_task = parameters['root']

        task_parameters = parameters[task]

        'onPipe'
        'onSuccess'
        'onFail'


    def start_job(self):
        pass
