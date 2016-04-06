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

<<<<<<< HEAD

	volunteers = relationship("Volunteer", back_populates="volunteerSkills")
=======
	#volunteers = relationship("Volunteer", back_populates="volunteerSkills")
>>>>>>> enum-fixes

	def __init__(self, skill, volunteer_id):
		self.skill = skill
		self.volunteer_id = volunteer_id

	def __repr__(self):
		return "<VolunteerSkills(skill='%s')>" % (self.day)


