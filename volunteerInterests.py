from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from db import Base, Session
from enums import InterestsEnum

class VolunteerInterests(Base):
	__tablename__ = 'volunteerInterests'

	id = Column(Integer, primary_key=True)
	interest = Column(Enum("Youth","Seniors","Education","Environment/Sustainability","Health","Arts and Culture","Financial Empowerment","Veterans","Immigration","Animals","Mentoring","Homeless/Housing","Lesbian, gay, bisexual, transgender","Domestic Violence","Hunger","People with Disabilities",
				name="interests_enum"), nullable=False)
	volunteer_id = Column(Integer, ForeignKey('volunteers.id'))

	volunteers = relationship("Volunteer", back_populates="volunteerInterests")

	def __init__(self, id, interest, volunteer_id):
		self.id = id
		self.interest = interest

	def __repr__(self):
		return "<VolunteerInterests(interest='%s')>" % (self.interest)