from user import User
from db import Base, Session
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker
import json
from datetime import datetime
import itertools


class Admin(User):
    __tablename__ = 'admins'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    # the only additional field an admin has is the master admin flag
    master = Column(Boolean, nullable=false)

    __mapper_args__ = {'polymorphic_identity' : 'admin'}

    @classmethod
    def fromdict(cls, d):
        allowed = ('name', 'email', 'passwordhash', 'phone', 'last_active', 'birthdate', 'bio', 'gender', 'master')
        df = {k : v for k, v in d.items() if k in allowed}
        return cls(**df)

    def __init__(self, name, email, passwordhash, phone, master, birthdate=None, bio=None, gender=None, last_active=datetime.now()):
        #will contain all these fields from user
        self.name = name
        self.email = email
        self.passwordhash = passwordhash
        self.phone = phone
        self.last_active = last_active
        self.master = master
        self.birthdate = birthdate
        self.bio = bio
        self.gender = gender

    #create an admin from a json blob
    def createAdmin(json):
        a = Admin.fromdict(json)
        s = Session()
        try:
            s.add(a)
            s.commit()
        except:
            return False
        finally:
            s.close()
        return True


