#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine

class SessionHandler():

    def create_session(self):

        # create engine
        db_engine = create_engine('sqlite+pysqlite:///database/sledge.db', module=sqlite)

        # create session
        Session = sessionmaker(bind=db_engine)
        session = Session()

        return session
