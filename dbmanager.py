#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite
from core.database.base import Base
from sqlalchemy import create_engine

de = create_engine('sqlite+pysqlite:///database/sledge.db', module=sqlite)
from core.database.models import Queue, Schedule, Worklog

Base.metadata.create_all(de, checkfirst=True)
