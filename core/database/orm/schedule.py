#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from core.database import SessionHandler
from core.database import Base

SHORT_STRING = 30
LONG_STRING  = 400

class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)

    # job name
    name = Column(String(SHORT_STRING), nullable=False)

    # job description
    description = Column(String(LONG_STRING), nullable=False)

    # cron expression
    cronexp = Column(String(SHORT_STRING), nullable=False)

    # job parameters including task parameters and task chain
    parameters = Column(String(LONG_STRING), nullable=True)

    # enabled
    enabled = Column(Boolean, nullable=False, default=True)



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
