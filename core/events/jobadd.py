#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation import Response, StatusCode
from core.database import ScheduleManager

class JobAdd():

    def execute(self, request):

        response = Response()

        try:

            # get schedulation data from the user
            schedulation = request.data

            # create and add new schedule
            schedule_manager = ScheduleManager()
            schedule_manager.set_schedule(schedulation)

        except Exception:

            response.set_status(StatusCode.STATUS_ERROR)
            response.set_description('Impossible to add schedule')

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_description('Schedule has been added!')

        return response
