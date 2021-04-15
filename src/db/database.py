from typing import Callable
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SessionType

# https://stackoverflow.com/q/34009296
# there isn't anything multi-threaded here so i haven't a clue
# why i'm getting thread issues. sqlalchemy bug maybe?
# if there are db corruption issues, check_same_thread=False
# is almost certainly the cause (right now it just generates exceptions
# on the thread)
path = f"sqlite:///{os.getenv('RW_DB_PATH', ':memory:')}"#?check_same_thread=False"
engine = create_engine(path)

Session: Callable[[], SessionType] = sessionmaker(bind=engine, expire_on_commit=False)