#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine

class SessionHandler():

    def __init__(self):
        self.session = None

    def create_session(self):

        if not self.session:

            # create engine
            db_engine = create_engine('sqlite+pysqlite:///database/sledge.db', module=sqlite)

            # create session
            Session = sessionmaker(bind=db_engine)
            self.session = Session()

        return

    def close_session(self):

        if self.session:
            self.session.close()

        return
