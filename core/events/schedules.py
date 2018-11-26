#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation import Response, StatusCode, FollowUp
from core.database import SqliteSession, Schedule

class ScheduleAddEvent:

    def execute(self, request):

        response = Response()
        follow_up = FollowUp('RELOAD')

        # create db session
        session = SqliteSession.create()

        try:

            # get schedulation data from the user
            schedulation = request.data

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

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)
            response.set_data({'msg': 'Impossible to add the schedule.'})

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_data({'msg': 'Schedule has been added.'})

        finally:
            session.close()

        return response, follow_up


class ScheduleListEvent:

    def execute(self, request):

        response = Response()

        follow_up = FollowUp(None)

        data = {}

        try:

            # get all schedules
            session = SqliteSession.create()

            schedules = session.query(Schedule).group_by(Schedule.name).all()

            session.close()

            schedule_list = []
            for s in schedules:

                d = {}
                d['id'] = s.id
                d['name'] = s.name
                d['description'] = s.description
                d['cronexp'] = s.cronexp
                d['enabled'] = s.enabled

                schedule_list.append(d)

            data['Result'] = schedule_list

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)

        else:
            response.set_status(StatusCode.STATUS_OK)

        finally:
            response.set_data(data)

        return response, follow_up


class ScheduleRemoveEvent:

    def execute(self, request):

        # get schedulation id
        args = request.data
        schedule_id = args['schedule_id']

        response = Response()
        follow_up = FollowUp('RELOAD')

        # create db session
        session = SqliteSession.create()

        try:

            # delete
            sched_to_remove = session.query(Schedule).filter(Schedule.id==schedule_id).one()
            session.delete(sched_to_remove)

            # save
            session.commit()

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)
            response.set_data({'msg': 'Impossible to remove the schedule.'})

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_data({'msg': 'Schedule has been removed.'})

        finally:
            session.close()

        return response, follow_up


class ScheduleDisableEvent:

    def execute(self, request):

        # get schedulation id
        args = request.data
        schedule_id = args['schedule_id']

        response = Response()
        follow_up = FollowUp('RELOAD')

        # create db session
        session = SqliteSession.create()

        try:

            # disable
            sched = session.query(Schedule).filter(Schedule.id==schedule_id).one()
            sched.enabled = False

            # save
            session.add(sched)
            session.commit()

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)
            response.set_data({'msg': 'Impossible to disable the schedule.'})

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_data({'msg': 'Schedule has been disabled.'})

        finally:
            session.close()

        return response, follow_up


class ScheduleEnableEvent:

    def execute(self, request):

        # get schedulation id
        args = request.data
        schedule_id = args['schedule_id']

        response = Response()
        follow_up = FollowUp('RELOAD')

        # create db session
        session = SqliteSession.create()

        try:

            # enable
            sched = session.query(Schedule).filter(Schedule.id==schedule_id).one()
            sched.enabled = True

            # save
            session.add(sched)
            session.commit()

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)
            response.set_data({'msg': 'Impossible to enable the schedule.'})

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_data({'msg': 'Schedule has been enabled.'})

        finally:
            session.close()

        return response, follow_up
