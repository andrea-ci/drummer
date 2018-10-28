#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from core.database import SessionHandler
from core.database import Base

SHORT_STRING = 30
LONG_STRING  = 200

class Queue(Base):
    __tablename__ = 'queues'

    id = Column(Integer, primary_key=True)

    classname = Column(String(SHORT_STRING), nullable=False)

    data = Column(String(LONG_STRING), nullable=False)


class QueueManager(SessionHandler):

    def is_empty(self):

        session = self.create_session()

        return session.query(Queue).count()==0


    def pick_one(self):

        session = self.create_session()

        q = session.query(Queue).group_by(Queue.classname)

        # list of tuples
        res = q.first()

        session.close()

        return res


    def add(self, queue):

        session = self.create_session()

        session.add(queue)

        # save
        session.commit()
        session.close()

        return True
