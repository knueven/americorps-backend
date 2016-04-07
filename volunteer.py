from user import User
from db import Base, Session
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from flask import json
import itertools
from datetime import datetime
import enums
from enums import EducationEnum
#import volunteerNeighborhoods
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
    education = Column(Enum("Less than High School","High School diploma or equivalent","Some college, no degree"
                            ,"Postsecondary non-degree award","Associate's degree", "Bachelor's degree",
                            "Master's degree", "Doctoral or professional degree", name="education_enum"))

    # volunteerNeighborhoods = relationship("VolunteerNeighborhoods", order_by=VolunteerNeighborhoods.id,
    #     back_populates='volunteers') #enum
    # volunteerInterests = relationship("VolunteerInterests", order_by=VolunteerInterests.id,
    #     back_populates='volunteers') #enum?
    # volunteerSkills = relationship("VolunteerSkills", order_by=VolunteerSkills.id, back_populates='volunteers')
    # volunteerAvailability = relationship("VolunteerAvailability", order_by=VolunteerAvailability.id,
    #     back_populates='volunteers') #this will need some discussion
    vhours = Column(Integer) #will be a seperate table later, could be merged into events

    @classmethod
    def fromdict(cls, d):
        allowed = ('name', 'email', 'passwordhash', 'phone', 'last_active', 'birthdate', 
            'bio', 'gender', 'vhours','education', 'events')
        df = {k : v for k, v in d.items() if k in allowed}
        return cls(**df)

    def asdict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
                dict_[key] = getattr(self, key)
        return dict_

    def __init__(self, name, email, passwordhash, phone,
        birthdate=None, bio=None, gender=None,
        vhours=None, volunteerNeighborhoods=None, volunteerInterests=None, 
        volunteerSkills=None, education=None, volunteerAvailability=None):
        self.name = name
        self.email = email
        self.set_password(passwordhash)
        self.phone = phone
        self.last_active = datetime.now()
        self.birthdate = birthdate
        self.permissions = 'volunteer'
        self.bio = bio
        self.gender = gender
        self.vhours = vhours
        #self.volunteerNeighboorhoods = volunteerNeighborhoods
        self.education = education
        # if volunteerInterests is None:
        #     self.volunteerInterests = []
        # else:
        #     self.volunteerInterests = volunteerInterests
        # if volunteerSkills is None:
        #     self.volunteerSkills = []
        # else:
        #     self.volunteerSkills = volunteerSkills
        # if volunteerAvailability is None:
        #     self.volunteerAvailability = []
        # else:
        #     self.volunteerAvailability = volunteerAvailability

    def set_password(self, password):
        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)

    def grab_neighborhoods(volun_id, json1):
        n = json.loads(json.dumps(json1))
        neighborhoods = n['neighborhoods']
        VolunteerNeighborhoods.create_v_neighborhood(volun_id, neighborhoods)

    def grab_skills(volun_id, json1):
        s = json.loads(json.dumps(json1))
        skills = s['skills']
        VolunteerSkills.createvskills(volun_id, skills)

    def grab_interests(volun_id, json1):
        i = json.loads(json.dumps(json1))
        interests = i['interests']
        VolunteerInterests.create_v_interests(volun_id, interests)

    def grab_availability(volun_id, json1):
        a = json.loads(json.dumps(json1))
        avail = a['availability']
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
        a = Attendee()
        if event == null:
            raise ValueError("event does not exist")
        else:
            try:
                a.addRelation(self.id, eventid)
            except False:
                raise exc.ArgumentError('commit failed')





