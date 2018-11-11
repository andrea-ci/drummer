#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite
from core.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# parsing
from sys import exit as sys_exit
from sys import argv as sys_argv
import argparse


class ArgParser:
    def process(self, sys_argv):
        parser = self.define_parsers()
        args = vars(parser.parse_args(sys_argv[1:]))
        # get command classname
        if args:
            return args
        else:
            print('Syntax error. Use -h option for help.')
            sys_exit()

    def define_parsers(self):
        # create the top-level parser
        parser = argparse.ArgumentParser(prog='Sledge DbManager')
        # add subparsers
        subparsers = parser.add_subparsers(help='command help', title='DbManager commands', description='Featured operations')
        # db:create
        parser_tl = subparsers.add_parser('db:create', help='Create a fresh new database')
        parser_tl.add_argument('-v', '--verbose', help = 'increase output verbosity', action = 'count', default = 0)
        parser_tl.set_defaults(command='db_create')

        return parser


if __name__ == '__main__':

    # get command from console
    args = ArgParser().process(sys_argv)

    if args.get('command') == 'db_create':

        de = create_engine('sqlite+pysqlite:///database/sledge.db', module=sqlite)

        #from core.database.entities.queue import Queue
        from core.database.entities.schedule import Schedule
        from core.database.entities.worklog import Worklog

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
