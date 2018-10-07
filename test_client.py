from database.models.schedule import ScheduleWriter
from scheduler.extender import Extender
"""
from core.database.models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlite3 import dbapi2 as sqlite
"""
if __name__ == '__main__':

    extender = Extender()

    print(extender.load_schedules())
    extender.load_jobs()

    extender.run()


"""
    parameters = dict()
    parameters['name'] = 'Poppo'
    parameters['description'] = 'hello task'
    parameters['cronexp'] = '45 0 * * *'

    schedule_writer = ScheduleWriter()
    schedule_writer.create_session()
    schedule_writer.set_schedule(parameters)
    schedule_writer.close_session()

    qp = QueueReader()
    qp.create_session()
    print(qp.is_empty())
    print(qp.get_first())
    qp.close_session()

# create engine
db_engine = create_engine('sqlite+pysqlite:///database/sledge.db', module=sqlite)

# create session
Session = sessionmaker(bind=db_engine)
session = Session()

# create and add object
queue = Queue(classname='pippo', parameters='pop')
session.add(queue)



q = session.query(Schedule).filter(Schedule.name == 'Pippo')
q = session.query(Schedule.name)

# list of tuples
res = q.all()

print(res)
# save
session.commit()
session.close()
"""
