from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from enum import Enum

Base = declarative_base()
#replace with config setting for database
database_engine = create_engine("mysql://...")
Session.configure(bind=database_engine)

class VolunteerNeighborhoods(Base):
	__tablename__ = 'volunteerNeighborhoods'

	id = Colum(Integer, primary_key=True)
	neighborhood = Column(Enum(NeighborhoodsEnum), nullable=False)
	volunteer_id = Column(Integer, ForeignKey('volunteers.id'))

	volunteer = relationship("Volunteer", back_populates="volunteerNeighborhoods")

	def __init__(self, id, neighborhood, volunteer_id):
		self.id = id
		self.neighborhood = neighborhood

	def __repr__(self):
		return "<VolunteerNeighborhoods(neighborhood='%s')>" % (self.neighborhood)
