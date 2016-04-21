from db import Base, Session
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from enums import NeighborhoodsEnum

class EventNeighborhoods(Base):
	__tablename__ = 'eventNeighborhoods'

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
	event_id = Column(Integer, ForeignKey('events.id'))

	#events = relationship("Event", back_populates="eventNeighborhoods")

	def __init__(self, neighborhood, event_id):
		self.neighborhood = neighborhood
		self.event_id = event_id

	def __repr__(self):
		return "<EventNeighborhoods(neighborhood='%s')>" % (self.neighborhood)
