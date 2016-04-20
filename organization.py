from sqlalchemy import *
from sqlalchemy import exc
from db import Base, Session
from datetime import datetime, date
from flask import json
from event import Event
from user import User
from orgmember import OrgMember
import organization
from werkzeug.security import generate_password_hash, check_password_hash

class Organization(User):
    __tablename__ = 'organizations'
    __mapper_args__ = {'polymorphic_identity' : 'organization'}
    id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(30), nullable=False)
    state = Column(String(15), nullable=False)
    zip = Column(String(5), nullable=False)
    mission = Column(String(255), nullable=False)
    poc = Column(String(60), nullable=False)
    pics = Column(String(5000))

    @classmethod
    def fromdict(cls, d):
        allowed = ('name', 'email', 'passwordhash', 'phone', 'last_active',
                   'address', 'city', 'state', 'zip', 'mission', 'poc', 'pics')
        df = {k: e for k,e in d.items() if k in allowed}
        return cls(**df)

    def asdict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
                result = getattr(self, key)
                if isinstance(result, date):
                    dict_[key] = str(result)
                else:
                    dict_[key] = result
        return dict_

    def __init__(self, name, email, passwordhash, phone, address, city, state,
                 zip, mission, poc, pics=None):

        # make sure th zip code is valid
        if len(zip) != 5 or not(zip.isdigit()):
            raise ValueError("a zip code must be 5 digits")
        else:
            self.zip = zip

        self.name = name
        self.email = email
        self.set_password(passwordhash)
        if len(phone) > 10 :
            raise ValueError("phone number is too long")
        elif len(phone) < 10:
            raise ValueError("phone number is too short")
        elif phone.isdigit() == False:
            raise ValueError("phone number must be a string of digits")
        else:
            self.phone = phone
        self.permissions = 'organization'
        self.address = address
        self.city = city
        self.state = state
        self.mission = mission
        self.poc = poc
        self.last_activity = datetime.now()
        self.pics = pics


    def __repr__(self):
        return "Organization(%s, %s)" % (self.id, self.name)

    def set_password(self, password):
        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)


    def deleteSelf(self, session):
        events = session.query(Event).filter_by(org=self.id)
        if events:
            for e in events:
                e.deleteSelf(session)
            session.commit()
        members = session.query(OrgMember).filter_by(org=self.id)
        if members:
            for m in members:
                try:
                    session.delete(m)
                except:
                    raise exc.SQLAlchemyError("failed to delete OrgMember " + m.id)
        try:
            session.delete(self)
            session.commit()
        except:
            raise exc.SQLAlchemyError("failed to delete Organization " + self.id)
        session.commit()


#def updateOrg(org_id, update_data):
#    session = Session()
#    try:
#        session.query(Organization).filter_by(id=org_id).update(json.loads(update_data))
#        session.commit()
#    except:
#        session.rollback()
#        raise ValueError("id not found")
#    finally:
#        session.close()
        
# create an event from a json string
def createOrganization(json1):
    e = Organization.fromdict(json1)
    s = Session()
    try:
        s.add(e)
        s.commit()
    except:
        print("here")
        return False
    finally:
        s.close()
    return True

