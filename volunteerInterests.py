from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from enum import Enum

Base = declarative_base()
#replace with config setting for database
database_engine = create_engine("mysql://...")
Session.configure(bind=database_engine)

class VolunteerInterests(Base):
	__tablename__ = 'volunteerInterests'

	id = Column(Integer, primary_key=True)
	interest = Column(Enum(InterestsEnum), nullable=False)
	volunteer_id = Column(Integer, ForeignKey('volunteers.id'))

	volunteer = relationship("Volunteer", back_populates="volunteerInterests")

	def __init__(self, id, interest, volunteer_id):
		self.id = id
		self.interest = interest

	def __repr__(self):
		return "<VolunteerInterests(interest='%s')>" % (self.interest)