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

            schedule_dict = {}
            for ii,s in enumerate(schedules):

                d = {}
                d['name'] = s.name
                d['description'] = s.description
                d['cronexp'] = s.cronexp
                d['enabled'] = s.enabled

                schedule_dict[ii] = d

            data['Result'] = schedule_dict

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)

        else:
            response.set_status(StatusCode.STATUS_OK)

        finally:
            response.set_data(data)

        return response
