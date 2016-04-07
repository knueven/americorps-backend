from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from db import Base, Session
from enums import InterestsEnum

class EventInterests(Base):
	__tablename__ = 'eventInterests'

	id = Column(Integer, primary_key=True)
	interest = Column(Enum("Youth","Seniors","Education","Environment/Sustainability","Health","Arts and Culture","Financial Empowerment","Veterans","Immigration","Animals","Mentoring","Homeless/Housing","Lesbian, gay, bisexual, transgender","Domestic Violence","Hunger","People with Disabilities",
				name="interests_enum"), nullable=False)
	event_id = Column(Integer, ForeignKey('events.id'))

	events = relationship("Event", back_populates="eventInterests")

	def __init__(self, id, interest, event_id):
		self.id = id
		self.interest = interest

	def __repr__(self):
		return "<EventInterests(interest='%s')>" % (self.interest)