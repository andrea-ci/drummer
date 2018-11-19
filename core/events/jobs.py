#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation.messages import Response, StatusCode
from core.database import SqliteSession, Schedule

class JobAdd():

    def execute(self, request):

        response = Response()

        try:

            # get schedulation data from the user
            schedulation = request.data

            # create and add new schedule
            session = SqliteSession.create()

            # create and add schedule object
            schedule = Schedule(
                name = schedulation.get('name'),
                description = schedulation.get('description'),
                cronexp = schedulation.get('cronexp'),
                parameters = schedulation.get('parameters'),
                enabled = schedulation.get('status')
            )

            # save
            session.add(schedule)

            session.commit()
            session.close()

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)
            response.set_data({'msg': 'Impossible to add schedule'})

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_data({'msg': 'Schedule has been added!'})

        return response


class JobList():

    def execute(self, request):

        response = Response()

        data = {}

        try:

            # get all schedules
            session = SqliteSession.create()

            schedules = session.query(Schedule).group_by(Schedule.name).all()

            session.close()

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
