from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from db import Base, Session
from enums import SkillsEnum

class EventSkills(Base):
	__tablename__ = 'eventSkills'

	id = Column(Integer, primary_key=True)
	skill = Column(Enum("Public Relations/Public Speaking",
						"Teaching/Tutoring",
						"IT/Computer",
						"Administrative",
						"Legal",
						"Coaching/Mentoring",
						"Handiwork",
						"Fine Arts",
						"TEFL/TESOL",
						"Writing/Editing",
						"Foreign Language",
						"Event Planning",
						"Management",
						"Sports/Recreation", name="skills_enum"), nullable=False)
	event_id = Column(Integer, ForeignKey('events.id'))

	#events = relationship("Event", back_populates="eventSkills")

	def __init__(self, skill, event_id):
		#self.id = id
		self.skill = skill
		self.event_id = event_id

	def __repr__(self):
		return "<EventSkills(skill='%s')>" % (self.day)

	def createvskills(event_id, skills):
		s = Session()
		try:
			for sk in skills: 
				v = EventSkills(sk, event_id)
				s.add(v)

			s.commit()
		except:
			return False
		finally:
			s.close()
		return True