#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.database.models import Schedule
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlite3 import dbapi2 as sqlite
from base.messages import Response, StatusCode

class JobAdd():

    def execute(self, request):

        response = Response()

        try:

            # create engine
            db_engine = create_engine('sqlite+pysqlite:///database/sledge.db', module=sqlite)

            # create session
            Session = sessionmaker(bind=db_engine)
            session = Session()

            # create and add new schedule
            name = request.parameters.get('name')
            description = request.parameters.get('description')
            cronexp = request.parameters.get('cronexp')

            schedule = Schedule(name=name, description=description, cronexp=cronexp)
            session.add(schedule)

            # save schedule
            session.commit()

        except Exception:

            response.set_status(StatusCode.STATUS_ERROR)
            response.set_description('Impossible to add schedule')

        else:
            response.set_status(StatusCode.STATUS_OK)
            response.set_description('Schedule has been added!')

        finally:
            session.close()


        return response
