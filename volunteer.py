from user import User
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker
from app import Base, Session

class Volunteer(User):
		__tablename__ = "volunteers"
		__mapper_args__ = {'polymorphic_identity' : 'volunteer'}
		id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
		# the Volunteer will have all User fields
		vhours = Column(Integer) #will be a seperate table later, could be merged into events
		neighborhood = Column(String(255)) # seperate table Neighborhoods
		interests = Column(String(255)) #enum?
		skills = Column(String(255)) 
		education = Column(String(255)) #seperate table
		availability = Column(String(255)) #this will need some discussion
		events = Column(String(255)) #will need to foreignkey to another table later

		def __init__(self, id, name, email, passwordhash, phone, last_activity,
			birthdate=None, about=None, gender=None,
			vhours=None, neighborhood=None, interests=None, 
			skills=None, education=None, availability=None, events=None):
			self.id = id
			self.name = name
			self.email = email
			self.passwordhash = passwordhash
			self.phone = phone
			self.last_activity = last_activity
			self.birthdate = birthdate
			self.about = about
			self.gender = gender
			self.vhours = vhours
			self.neighboorhood = neighborhood
			self.interests = interests
			self.skills = skills
			self.education = education
			self.availability = availability
			self.events = events