#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from database.sessionhandler import SessionHandler
from database.base import Base

SHORT_STRING = 30
LONG_STRING  = 200

class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    # job name
    name = Column(String(SHORT_STRING), nullable=False)
    # job description
    description = Column(String(LONG_STRING), nullable=False)
    # cron expression
    cronexp = Column(String(SHORT_STRING), nullable=False)
    # chain of tasks
    task_chain = Column(String(LONG_STRING), nullable=True)


class ScheduleReader(SessionHandler):

    def is_empty(self):
        return self.session.query(Schedule).count()==0

    def get_all():

        q = self.session.query(Schedule.name, Schedule.description, Schedule.cronexp).group_by(Schedule.name)

        res = q.all()

        return res



class ScheduleWriter(SessionHandler):

    def set_schedule(self, data):

        name = data.get('name')
        description = data.get('description')
        cronexp = data.get('cronexp')
        task_chain = data.get('task_chain')

        # create and add object
        schedule = Schedule(name=name, description=description, cronexp=cronexp)

        # save
        self.session.add(schedule)
        self.session.commit()

        return
