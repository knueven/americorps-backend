from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker

Base = declarative_base()
#replace with config setting for database
database_engine = create_engine("mysql://...")
Session = sessionmaker(bind=database_engine)



class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, nullable=False)
	name = Column(String(255), nullable=False)
	email = Column(String(255), nullable=False)
	passwordhash = Column(String(255), nullable=False) 
	phone = Column(String(255), nullable=False)
	permissions = Column(Enum('volunteer', 'orgmember', 'admin'), nullable=False)
	last_activity = Column(DateTime(), nullable=False)
	birthdate = Column(String(255))
	about = Column(String(10000))
	gender = Column(Enum('Male', 'Female', 'Other'))

	def __init__(self, id, name,  
		email, passwordhash, phone, permissions, last_activity, birthdate=None, about=None, gender=None):
		self.id = id
		self.name = name
		self.email = email
		self.passwordhash = passwordhash
		self.phone = phone
		self.permissions = permissions
		self.last_activity = last_activity
		self.birthdate = birthdate
		self.about = about
		self.gender = gender
		

	def __repr__(self):
		return "User(%s, %s)" % (self.id, self.name)

	# Update a user (must exist)
	def updateUser(self, user_id, update_data):
		session = Session()
		try:
			session.query(users).filter_by(id=user_id).update(json.loads(update_data))
		except:
			session.rollback()
			raise #exception of some sort
		finally:
			session.close()

	