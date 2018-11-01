#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation.messages import Response, StatusCode
from core.database import ScheduleManager

class JobList():

    def execute(self, request):

        response = Response()

        data = {}
        try:
            # create and add new schedule
            schedule_manager = ScheduleManager()
            schedules = schedule_manager.get_all()

            result = {}
            for ii,s in enumerate(schedules):

                d = {}
                d['name'] = s.name
                d['description'] = s.description
                d['cronexp'] = s.cronexp
                d['enabled'] = s.enabled

                result[ii] = d

            data['result'] = result
            
        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)
            data['status'] = 'Impossible to list schedules'

        else:
            response.set_status(StatusCode.STATUS_OK)
            data['status'] = 'List of schedule generated'

        finally:
            response.set_data(data)

        return response
