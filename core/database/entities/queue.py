#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from core.database import Base

SHORT_STRING = 30
LONG_STRING  = 200

class Queue(Base):
    __tablename__ = 'queues'

    id = Column(Integer, primary_key=True)

    classname = Column(String(SHORT_STRING), nullable=False)

    data = Column(String(LONG_STRING), nullable=False)
