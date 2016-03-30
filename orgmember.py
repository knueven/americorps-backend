from user import User
from db import Base, Session
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker
from datetime import datetime


class OrgMember(User):
		__tablename__ = "orgmembers"
		__mapper_args__ = {'polymorphic_identity' : 'orgmember'}
		id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
		# the OrgMember will have all User fields
		vhours = Column(Integer) #will be a seperate table later, could be merged into events
		neighborhood = Column(String(255)) # seperate table Neighborhoods
		interests = Column(String(255)) #enum?
		education = Column(String(255)) #seperate table
		availability = Column(String(255)) #this will need some discussion
		events = Column(String(255)) #will need to foreignkey to another table later
		org = Column(Integer, ForeignKey('organizations.id')) #object or id?
		poc = Column(Boolean, nullable=False)

		@classmethod
		def fromdict(cls, d):
			allowed = ('name', 'email', 'passwordhash', 'phone', 'last_active', 'birthdate', 
				'bio', 'gender', 'vhours', 'neighborhood', 'interests', 
				'education', 'availabilty', 'events', 'org', 'poc')
			df = {k : v for k, v in d.items() if k in allowed}
			return cls(**df)

		def __init__(self, name, email, passwordhash, phone, last_active=datetime.now(), birthdate=None,
             bio=None, gender=None, vhours=None, neighborhood=None, interests=None, 
			education=None, availability=None, events=None, org=None, poc=None):
			self.name = name
			self.email = email
			self.passwordhash = passwordhash
			self.phone = phone
			self.last_active = last_active
			self.birthdate = birthdate
			self.bio = bio
			self.gender = gender
			self.vhours = vhours
			self.neighborhood = neighborhood
			self.interests = interests
			self.education = education
			self.availability = availability
			self.events = events
			self.org = org
			self.poc = poc	

		#create a volunteer from a json blob
		def createMember(json):
			o = OrgMember.fromdict(json)
			s = Session()
			try:
				s.add(o)
				s.commit()
			except:
				return False
			finally:
				s.close()
			return True
