from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .database import engine

Base = declarative_base()

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    url = Column(String)
    last_up = Column(DateTime)

    def __repr__(self):
        return f"<Site {self.actor}>"

class Leak(Base):
    __tablename__ = "leaks"

    id = Column(Integer, primary_key=True)
    org = Column(String)
    url = Column(String)
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)

    site_id = Column(Integer, ForeignKey("sites.id"))
    site = relationship("Site")

    def __repr__(self):
        return f"<Leak {self.org}>"

Base.metadata.create_all(engine)