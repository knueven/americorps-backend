from user import User
from db import Base, Session
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
import json
from flask import json
import itertools
from datetime import datetime, date
import enums
from enums import EducationEnum
from volunteerNeighborhoods import VolunteerNeighborhoods
from volunteerSkills import VolunteerSkills
from volunteerInterests import VolunteerInterests
from volunteerAvailability import VolunteerAvailability
from attendee import Attendee
from event import Event
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash

class Volunteer(User):
    __tablename__ = "volunteers"
    __mapper_args__ = {'polymorphic_identity' : 'volunteer'}
    id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    # the Volunteer will have all User fields
    uhours = Column(Integer)
    vhours = Column(Integer)
    education = Column(Enum("Less than High School","High School diploma or equivalent","Some college, no degree"
                            ,"Postsecondary non-degree award","Associate's degree", "Bachelor's degree",
                            "Master's degree", "Doctoral or professional degree", name="education_enum"))


    @classmethod
    def fromdict(cls, d):
        allowed = ('name', 'email', 'passwordhash', 'phone', 'last_active', 'birthdate', 
            'bio', 'gender', 'uhours', 'vhours','education', 'events')
        df = {k : v for k, v in d.items() if k in allowed}
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

    def __init__(self, name, email, passwordhash, phone,
                 birthdate=None, bio=None, gender=None, uhours=None, vhours=None,
                 education=None):
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
        self.birthdate = birthdate
        self.permissions = 'volunteer'
        self.bio = bio
        self.gender = gender
        self.uhours = uhours
        self.vhours = vhours
        self.education = education
        

    def set_password(self, password):
        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)

    def grab_neighborhoods(volun_id, json1):
        neighborhoods = json1['neighborhoods']
        #print(neighborhoods)
        VolunteerNeighborhoods.create_v_neighborhood(volun_id, neighborhoods)

    def grab_skills(volun_id, json1):
        skills = json1['skills']
        VolunteerSkills.createvskills(volun_id, skills)

    def grab_interests(volun_id, json1):
        interests = json1['interests']
        VolunteerInterests.create_v_interests(volun_id, interests)

    def grab_availability(volun_id, json1):
        avail = json1['availability']
        VolunteerAvailability.create_v_availability(volun_id, avail)

    # take in a user id, grab the volunteer from the database and return it
    def getVolunteer(self, id):
        s = Session()
        content = s.query(Volunteer).filter_by(id = id).first()
        s.close()
        if content:
            return content
        else:
            raise ValueError("user does not exist")

    # take an event and add it to this user's events
    def addEvent(self, eventid):
        s = Session()
        event = s.query(Event).filter_by(id=eventid).first()
        a = Attendee(id, eventid)
        if event == null:
            raise ValueError("event does not exist")
        else:
            try:
                a.addRelation(self.id, eventid)
            except False:
                raise exc.ArgumentError('commit failed')
            finally:
                s.close()

    def deleteSelf(self):
        s = Session()
        attendees = s.query(Attendee).filter_by(userID=self.id)
        if not(attendees):
            return False
        else:
            try:
                for a in attendees:
                    s.delete(a)
                s.delete(self)
                s.commit()
            except:
                print("delete failed")
                return False
            finally:
                s.close()
            return True

    # create a volunteer from a json blob
def createVolunteer(json):
    v = Volunteer.fromdict(json)
    s = Session()
    try:
        s.add(v)
        s.commit()
        n = True
    except:
        s.close()
        return False
    s.close()
    v2 = Volunteer.fromdict(json)
    if createEnums(v2, json):
        return True
    else:
        return False

def createEnums(v, json):
    s = Session()
    try:
        v1 = s.query(User).filter_by(email=v.email).first()
        Volunteer.grab_neighborhoods(v1.id, json)
        Volunteer.grab_skills(v1.id, json)
        Volunteer.grab_interests(v1.id, json)
        Volunteer.grab_availability(v1.id, json)
    except:
        return False
    finally:
        s.close()
    return True






