# Volunteer Availability Table

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum, exc
from db import Base, Session
from enums import DaysEnum


class VolunteerAvailability(Base):
    __tablename__ = 'volunteerAvailability'

    id = Column(Integer, primary_key=True)
    day = Column(Enum("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", name="days_enum"),
                 nullable=False)
    volunteer_id = Column(Integer, ForeignKey('volunteers.id'))

    # volunteers = relationship("Volunteer", back_populates="volunteerAvailability")

    def __init__(self, day, volunteer_id):
        self.day = day
        self.volunteer_id = volunteer_id

    def __repr__(self):
        return "<VolunteerAvailability(day='%s')>" % (self.day)

    def create_v_availability(volunteer_id, avail):
        s = Session()
        try:
            for a in avail:
                v = VolunteerAvailability(a, volunteer_id)
                s.add(v)
                s.commit()
        except:
            s.rollback()
            return False
        finally:
            s.close()
        return True
