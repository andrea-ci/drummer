#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine

class SqliteSession():

    @staticmethod
    def create():

        # create engine
        db_engine = create_engine('sqlite+pysqlite:///../sledge.db', module=sqlite)

        # create session
        Session = sessionmaker(bind=db_engine)
        session = Session()

        return session
