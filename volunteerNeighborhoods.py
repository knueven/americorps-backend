from db import Base, Session
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from enums import NeighborhoodsEnum

class VolunteerNeighborhoods(Base):
	__tablename__ = 'volunteerNeighborhoods'

	id = Column(Integer, primary_key=True)
	neighborhood = Column('neighborhood',NeighborhoodsEnum, nullable=False)
	volunteer_id = Column(Integer, ForeignKey('volunteers.id'))

	volunteer = relationship("Volunteer", back_populates="volunteerNeighborhoods")

	def __init__(self, id, neighborhood, volunteer_id):
		self.id = id
		self.neighborhood = neighborhood

	def __repr__(self):
		return "<VolunteerNeighborhoods(neighborhood='%s')>" % (self.neighborhood)
