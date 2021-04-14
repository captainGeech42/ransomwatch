from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import engine

Base = declarative_base()

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    url = Column(String)
    added = Column(DateTime(timezone=True), server_default=func.now())
    last_scanned = Column(DateTime(timezone=True))
    last_up = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<Site {self.actor}>"

class Victim(Base):
    __tablename__ = "leaks"

    id = Column(Integer, primary_key=True)
    org = Column(String)
    url = Column(String)
    published = Column(DateTime(timezone=True))
    first_seen = Column(DateTime(timezone=True))
    last_seen = Column(DateTime(timezone=True))

    site_id = Column(Integer, ForeignKey("sites.id"))
    site = relationship("Site")

    def __repr__(self):
        return f"<Victim {self.org} by {self.site.actor}>"

Site.victims = relationship("Victim", order_by=Victim.id, back_populates="site")

Base.metadata.create_all(engine)