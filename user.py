from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from db import Base, Session


# abstract base class for Users
class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True, nullable=False)
	name = Column(String(75), nullable=False)
	email = Column(String(60), nullable=False, unique=True)
	passwordhash = Column(String(255), nullable=False) 
	phone = Column(String(15), nullable=False)
	permissions = Column(Enum('volunteer', 'organization', 'admin'), nullable=False)
	last_active = Column(DateTime(timezone=False), nullable=True)
	token = Column(String(50))
	__mapper_args__ = {
		'polymorphic_identity':'user',
		'polymorphic_on': permissions
	}
		

	def __repr__(self):
		return "User(%s, %s)" % (self.id, self.name)







	
