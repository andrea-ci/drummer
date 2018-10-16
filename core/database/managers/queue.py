#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.database import SessionHandler, Queue

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
