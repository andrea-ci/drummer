#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.database import SessionHandler, Schedule

class ScheduleManager(SessionHandler):

    def is_empty(self):
        """ check if schedule table is empty """
        
        session = self.create_session()
        empty = session.query(Schedule).count()==0
        session.close()

        return empty


    def get_all(self):
        """ get all schedule objects from database """

        session = self.create_session()

        q = session.query(Schedule).group_by(Schedule.name)
        res = q.all()

        session.close()

        return res


    def set_schedule(self, schedulation):
        """ save a schedule object from the user-defined schedulation """

        session = self.create_session()

        name = schedulation.get('name')
        description = schedulation.get('description')
        cronexp = schedulation.get('cronexp')
        parameters = schedulation.get('parameters')
        status = schedulation.get('status')

        # create and add schedule object
        schedule = Schedule(name=name, description=description, cronexp=cronexp, parameters=parameters, enabled=status)

        # save
        session.add(schedule)

        session.commit()
        session.close()

        return True


    def set_status(self, status):
        """ enable/disable a schdule """
        pass
