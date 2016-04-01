from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from db import Base, Session
from enums import SkillsEnum

class VolunteerSkills(Base):
	__tablename__ = 'volunteerSkills'

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
	volunteer_id = Column(Integer, ForeignKey('volunteers.id'))

	volunteer = relationship("Volunteer", back_populates="volunteerSkills")

	def __init__(self, id, skill, volunteer_id):
		self.id = id
		self.skill = skill

	def __repr__(self):
		return "<VolunteerSkills(skill='%s')>" % (self.day)
