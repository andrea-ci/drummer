#!/usr/bin/python3
# -*- coding: utf-8 -*-
from database.models.schedule import ScheduleWriter
from base.messages import Response, StatusCode

class JobAdd():

    def execute(self, request):

        response = Response()

        try:

            parameters = request.parameters

            # create and add new schedule
            schedule_writer = ScheduleWriter()
            schedule_writer.create_session()
            schedule_writer.set_schedule(parameters)
            schedule_writer.close_session()

        except Exception:

            response.set_status(StatusCode.STATUS_ERROR)
            response.set_description('Impossible to add schedule')

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_description('Schedule has been added!')

        return response
