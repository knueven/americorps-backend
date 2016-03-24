from user import User
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker
from app import Base, Session


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

		def __init__(self, id, name, email, passwordhash, phone, last_activity, birthdate=None,
             about=None, gender=None, vhours=None, neighborhood=None, interests=None, 
			education=None, availability=None, events=None, org=None, poc=None):
			self.id = id
			self.vhours = vhours
			self.neighborhood = neighborhood
			self.interests = interests
			self.education = education
			self.availability = availability
			self.events = events
			self.org = org
			self.poc = poc	
