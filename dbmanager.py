#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite
from database.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

de = create_engine('sqlite+pysqlite:///database/sledge.db', module=sqlite)

from database.models.queue import Queue
from database.models.schedule import Schedule
#from database.models.worklog import Worklog

Base.metadata.create_all(de, checkfirst=True)

"""
# create session
Session = sessionmaker(bind=de)
session = Session()

# create and add object
queue = Queue(classname='pippo', parameters='pop')
session.add(queue)

schedule = Schedule(name='a dummy job', description='dummy descr', cronexp='*/1 * * * *')
session.add(schedule)

session.commit()
session.close()
"""
