#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.database.base import Base
from core.database.models import Queue, Schedule, Worklog
from sqlalchemy import create_engine
from sqlite3 import dbapi2 as sqlite

de = create_engine('sqlite+pysqlite:///database/sledge.db', module=sqlite)

Base.metadata.create_all(de, checkfirst=True)
