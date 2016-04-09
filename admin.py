from user import User
from db import Base, Session
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
import json
import itertools
from datetime import datetime
import enums
from organization import Organization
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash

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

    def asdict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
                dict_[key] = getattr(self, key)
        return dict_

    def __init__(self, name, email, passwordhash, phone, master, birthdate=None, bio=None, gender=None):
        #will contain all these fields from user
        self.name = name
        self.email = email
        self.set_password(passwordhash)
        if len(phone) > 15:
            raise ValueError('phone number is too long')
        elif len(phone) < 10:
            raise ValueError('phone number is too short')
        elif phone.isdigit() == False:
            raise ValueError('phone number must be a string of integers')
        else:
            self.phone = phone
        self.last_active = datetime.now()
        self.master = master
        self.birthdate = birthdate
        self.bio = bio
        self.gender = gender

    def set_password(self, password):
        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)

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

    def getAdmin(self, id):
        s = Session()
        content = s.query(Admin).filter_by(id = id).first()
        s.close()
        if content:
            return content
        else:
            raise ValueError("user does not exist")

    def deleteAccount(self):
        s = Session()
        try:
            s.delete(self)
            s.commit()
        except:
            return False
        finally:
            s.close()
        return True

    def deleteOrg(self, orgID):
        s = Session()
        org = s.query(Organization).filter_by(id=orgID).first()
        if org:
            isSuccessful = org.deleteSelf(s)
            if isSuccessful:
                s.commit()
        else:
            raise exc.NoReferenceError
        s.close()
        return isSuccessful



