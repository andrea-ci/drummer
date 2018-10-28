#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation.messages import Response, StatusCode
from core.database import ScheduleManager

class JobList():

    def execute(self, request):

        response = Response()

        try:
            # create and add new schedule
            schedule_manager = ScheduleManager()
            schedules = schedule_manager.get_all()

            data = {}
            for ii,s in enumerate(schedules):

                d = {}
                d['name'] = s.name
                d['description'] = s.description
                d['cronexp'] = s.cronexp
                d['enabled'] = s.enabled

                data[ii] = d

            print(data)
            response.set_data(data)

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)
            response.set_description('Impossible to list schedules')

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_description('List of schedule generated')

        return response
