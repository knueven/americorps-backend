from user import User
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker
from app import Base, Session


class Admin(User):
    __tablename__ = 'admins'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    # the only additional field an admin has is the master admin flag
    master = Column(Boolean, nullable=false)

    __mapper_args__ = {'polymorphic_identity' : 'admin'}


    def __init__(self, id, name, email, passwordhash, phone, last_activity, master, birthdate=None, about=None, gender=None):
        #will contain all these fields from user
        self.id = id
        self.name = name
        self.email = email
        self.passwordhash = passwordhash
        self.phone = phone
        self.last_activity = last_activity
        self.master = master
        self.birthdate = birthdate
        self.about = about
        self.gender = gender


