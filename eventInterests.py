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


	#events = relationship("Event", back_populates="eventInterests")

	def __init__(self, interest, event_id):
		self.event_id = event_id
		self.interest = interest

	def __repr__(self):
		return "<EventInterests(interest='%s')>" % (self.interest)

	def create_v_interests(event_id, interests):
		s = Session()
		try:
			for i in interests: 
				v = EventInterests(i, event_id)
				s.add(v)

			s.commit()
		except:
			return False
		finally:
			s.close()
		return True