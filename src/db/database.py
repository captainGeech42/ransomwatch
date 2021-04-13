import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

path = f"sqlite:///{os.getenv('RW_DB_PATH', ':memory:')}"
engine = create_engine(path)

Session = sessionmaker(bind=engine)