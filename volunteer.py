from user import User
from db import Base, Session
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker
import json
import itertools
from datetime import datetime

class Volunteer(User):
		__tablename__ = "volunteers"
		__mapper_args__ = {'polymorphic_identity' : 'volunteer'}
		id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
		# the Volunteer will have all User fields
		vhours = Column(Integer) #will be a seperate table later, could be merged into events
		neighborhood = Column(String(255)) #enum
		interests = Column(String(255)) #enum?
		skills = Column(String(255)) 
		education = Column(String(255)) #enum
		availability = Column(String(255)) #this will need some discussion
		events = Column(String(255)) #will need to foreignkey to another table later

		@classmethod
		def fromdict(cls, d):
			allowed = ('name', 'email', 'passwordhash', 'phone', 'last_active', 'birthdate', 
				'about', 'gender', 'vhours', 'neighborhood', 'interests', 'skills', 
				'education', 'availabilty', 'events')
			df = {k : v for k, v in d.items() if k in allowed}
			return cls(**df)

		def __init__(self, name, email, passwordhash, phone, last_active=datetime.now(),
			birthdate=None, about=None, gender=None,
			vhours=None, neighborhood=None, interests=None, 
			skills=None, education=None, availability=None, events=None):
			self.name = name
			self.email = email
			self.passwordhash = passwordhash
			self.phone = phone
			self.last_active = last_active
			self.birthdate = birthdate
			self.permissions = 'volunteer'
			self.about = about
			self.gender = gender
			self.vhours = vhours
			self.neighboorhood = neighborhood
			self.interests = interests
			self.skills = skills
			self.education = education
			self.availability = availability
			self.events = events

		#create a volunteer from a json blob
		def createVolunteer(json):
			v = Volunteer.fromdict(json)
			s = Session()
			try:
				s.add(v)
				s.commit()
			except:
				return False
			finally:
				s.close()
			return True