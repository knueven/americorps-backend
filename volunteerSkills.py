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
	skill = Column(Enum("public",
						"teaching",
						"it",
						"administrative",
						"legal",
						"coaching",
						"handiwork",
						"arts",
						"tefl",
						"writing",
						"language",
						"event",
						"management",
						"sports", name="skills_enum"), nullable=False)
	volunteer_id = Column(Integer, ForeignKey('volunteers.id'))

	#volunteers = relationship("Volunteer", back_populates="volunteerSkills")

	def __init__(self, skill, volunteer_id):
		self.skill = skill
		self.volunteer_id = volunteer_id

	def __repr__(self):
		return "<VolunteerSkills(skill='%s')>" % (self.skill)

	def createvskills(volunteer_id, skills):
		s = Session()
		try:
			for sk in skills: 
				v = VolunteerSkills(sk, volunteer_id)
				s.add(v)

			s.commit()
		except:
			return False
		finally:
			s.close()
		return True

	def get_skills(id):
		s = Session()
		result = []
		q = s.query(VolunteerSkills).filter_by(volunteer_id=id)
		for sk in q:
				result.append(sk.skill)
		s.close()
		return result



