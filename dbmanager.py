#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite
from database.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

de = create_engine('sqlite+pysqlite:///database/sledge.db', module=sqlite)

from database.models import Schedule, Queue, Worklog

Base.metadata.create_all(de, checkfirst=True)

# create session
Session = sessionmaker(bind=de)
session = Session()

# create and add object
queue = Queue(classname='pippo', parameters='pop')
session.add(queue)

session.commit()
session.close()
