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
    education = Column(Enum("lesshigh","highschool","somecoll"
                            ,"postsec","associate", "bachelor",
                            "master", "doctoral", name="education_enum"))
    birthdate = Column(Date)
    bio = Column(String(10000))
    gender = Column(Enum('Male', 'Female', 'Other'))
    contact = Column(Boolean, nullable=False)
    pic = Column(String(1000))


    @classmethod
    def fromdict(cls, d):
        allowed = ('name', 'email', 'passwordhash', 'phone', 'contact', 'last_active', 'birthdate', 
            'bio', 'gender', 'uhours', 'vhours','education', 'events', 'pic')
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

    def __init__(self, name, email, passwordhash, phone, contact, uhours=None, vhours=None,
                 education=None, birthdate=None, bio=None, gender=None, pic=None):
        self.name = name
        # needs an @ and a .~~~
        self.email = email
        self.set_password(passwordhash)
        if len(phone) > 10:
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
        self.contact = contact
        self.pic = pic
        

    def set_password(self, password):
        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)

    def grab_neighborhoods(volun_id, json1):
        if json1['neighborhoods']:
            neighborhoods = json1['neighborhoods']
            #print(neighborhoods)
            VolunteerNeighborhoods.create_v_neighborhood(volun_id, neighborhoods)
        else:
            return

    def grab_skills(volun_id, json1):
        if json1['skills']:
            skills = json1['skills']
            VolunteerSkills.createvskills(volun_id, skills)
        else:
            return

    def grab_interests(volun_id, json1):
        if json1['interests']:
            interests = json1['interests']
            VolunteerInterests.create_v_interests(volun_id, interests)
        else:
            return

    def grab_availability(volun_id, json1):
        if json1['availability']:
            avail = json1['availability']
            VolunteerAvailability.create_v_availability(volun_id, avail)
        else:
            return

    # take in a user id, grab the volunteer from the database and return it
    def getVolunteer(self, id):
        s = Session()
        content = s.query(Volunteer).filter_by(id = id).first()
        s.close()
        if content:
            return content
        else:
            raise ValueError("user does not exist")

    def deleteSelfFrom(self, table, session):
        rows = session.query(table).filter_by(volunteer_id=self.id)
        if rows:
            for r in rows:
                try:
                    session.delete(r)
                except:
                    raise exc.SQLAlchemyError("failed to delete availability " + r.id)

    def deleteSelf(self, session):
        # delete all the attendee rows involving this user
        attendees = session.query(Attendee).filter_by(userID=self.id)
        if attendees:
            for a in attendees:
                try:
                    session.delete(a)
                except:
                    raise exc.SQLAlchemyError("failed to delete " + table.__tablename__ + " " + a.key)

        session.commit()
        # delete all the availability rows involving this user
        self.deleteSelfFrom(VolunteerAvailability, session)
        print(self.id)
        # delete all the interest rows involving this user
        self.deleteSelfFrom(VolunteerInterests, session)
        print("2")
        # delete all the neighborhood rows involving this user
        self.deleteSelfFrom(VolunteerNeighborhoods, session)
        print("3")
        # delete all the skill rows involving this user
        self.deleteSelfFrom(VolunteerSkills, session)
        print("4")
        session.commit()
        # delete this user
        try:
            print("5")
            session.delete(id=self.id)
            session.commit()
            print("6")
        except:
            print("failed to delete volunteer ")

    def log_hours(self, eventid, hours):
        s = Session()
        self.vhours = hours
        attendee = s.query(Attendee).filter_by(eventID=eventid, userID=self.id).first()
        if attendee:
            try:
                attendee.hours = hours
                s.commit()
            except:
                print("hour log failed")
                return False
            finally:
                s.close()
            return True
        else:
            return False

    def getEvents(self, session):
        return session.query(Attendee).filter_by(userID)
        

    # create a volunteer from a json blob
def createVolunteer(json):
    v = Volunteer.fromdict(json)
    s = Session()
    try:
        s.add(v)
        s.commit()
        n = True
    except:
        print("here3")
        s.close()
        return False
    s.close()
    v2 = Volunteer.fromdict(json)
    if createEnums(v2, json):
        return True
    else:
        print("here2")
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
        print("here4")
        return False
    finally:
        s.close()
    return True

# take an event and add it to this user's events
def addEvent(eventid, userid):
    s = Session()
    event = s.query(Event).filter_by(id=eventid).first()
    a = Attendee(userid, eventid)
    if event == null:
        raise ValueError("event does not exist")
    else:
        try:
            a.addRelation(userid, eventid)
        except False:
            raise exc.ArgumentError('commit failed')
        finally:
            s.close()
        return True






