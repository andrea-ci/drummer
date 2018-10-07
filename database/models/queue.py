#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from database.sessionhandler import SessionHandler
from database.base import Base

SHORT_STRING = 30
LONG_STRING  = 200

class Queue(Base):
    __tablename__ = 'queues'

    id = Column(Integer, primary_key=True)

    classname = Column(String(SHORT_STRING), nullable=False)

    parameters = Column(String(LONG_STRING), nullable=False)


class QueueReader(SessionHandler):

    def is_empty(self):
        return self.session.query(Queue).count()==0

    def get_first(self):

        #q = session.query(Queue).filter(Queue.name == 'Pippo')
        #q = session.query(Queue.name)
        q = self.session.query(Queue.classname).group_by(Queue.classname)

        # list of tuples
        res = q.first()

        return res


class QueueWriter(SessionHandler):

    def set_queue(self, data):

        session = self.session
        
        classname = data.get('classname')
        parameters = data.get('parameters')

        # create and add object
        queue = Queue(classname=classname, parameters=parameters)
        session.add(queue)

        # save
        session.commit()

        return
