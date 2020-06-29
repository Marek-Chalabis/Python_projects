import os
from hashlib import sha256
import datetime

from sqlalchemy import Column, String, create_engine, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# name of DB, if you provide new name a new DB will be created you can go back to the old one just by passing name here
DB_NAME = "TODO_DB"

engine = create_engine(f"sqlite:///{DB_NAME}.db")
BaseClass = declarative_base(engine)


class Todo(BaseClass):
    """ Create table"""

    __tablename__ = "Todo_app"
    TASK_HASH = Column(String(64), primary_key=True)
    name = Column(String(50), nullable=False)
    deadline = Column(Date(), nullable=False)
    task = Column(String(300), nullable=False)

    def __init__(self, name, deadline, task):
        self.name = name
        self.deadline = deadline
        self.task = task
        # hashes task by its task ! current time added to hash to make hash unique even when updating
        self.TASK_HASH = sha256(
            (name + str(deadline) + task + str(datetime.datetime.now())).encode()
        ).hexdigest()


def loadSession():
    """ establish connection to DB"""
    metadata = BaseClass.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# creates DB if not exists
if not os.path.exists(DB_NAME):
    session = loadSession()
    BaseClass.metadata.create_all(engine)
