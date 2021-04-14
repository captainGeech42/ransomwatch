from typing import Callable
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SessionType

path = f"sqlite:///{os.getenv('RW_DB_PATH', ':memory:')}"
engine = create_engine(path)

Session: Callable[[], SessionType] = sessionmaker(bind=engine)