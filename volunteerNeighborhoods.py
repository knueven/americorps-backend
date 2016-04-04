from db import Base, Session
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from enums import NeighborhoodsEnum

class VolunteerNeighborhoods(Base):
	__tablename__ = 'volunteerNeighborhoods'

	id = Column(Integer, primary_key=True)
	neighborhood = Column(Enum("Allston",
								"Back Bay",
								"Bay Village",
								"Beacon Hill",
								"Brighton",
								"Charlestown",
								"Chinatown/Leather District",
								"Dorchester",
								"Downtown",
								"East Boston",
								"Fenway Kenmore",
								"Hyde Park",
								"Jamaica Plain",
								"Mattapan",
								"Mid Dorchester",
								"Mission Hill",
								"North End",
								"Roslindale",
								"Roxbury",
								"South Boston",
								"South End",
								"West End",
								"West Roxbury",
								"Greater Boston Area/Outside City", name="neighborhoods_enum"), nullable=False)
	volunteer_id = Column(Integer, ForeignKey('volunteers.id'))

	volunteers = relationship("Volunteer", back_populates="volunteerNeighborhoods")

	def __init__(self, neighborhood, volunteer_id):
		self.id = id
		self.neighborhood = neighborhood
		self.volunteer_id = volunteer_id

	def __repr__(self):
		return "<VolunteerNeighborhoods(neighborhood='%s')>" % (self.neighborhood)
