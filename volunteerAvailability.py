# Volunteer Availability Table

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from db import Base, Session
from enums import DaysEnum

class VolunteerAvailability(Base):
	__tablename__ = 'volunteerAvailability'

	id = Column(Integer, primary_key=True)
	day = Column(DaysEnum, nullable=False)
	voluntee_id = Column(Integer, ForeignKey('volunteers.id'))

	volunteer = relationship("Volunteer", back_populates="volunteerAvailability")

	def __init__(self, id, day, volunteer_id):
		self.id = id
		self.day = day

	def __repr__(self):
		return "<VolunteerAvailability(day='%s')>" % (self.day)