from core.database.models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlite3 import dbapi2 as sqlite


# create engine
db_engine = create_engine('sqlite+pysqlite:///database/sledge.db', module=sqlite)

# create session
Session = sessionmaker(bind=db_engine)
session = Session()

# create and add object
schedule = Schedule(name='pippo', description='pop', cronexp='30 0 * * *')
session.add(schedule)

# save
session.commit()
session.close()
