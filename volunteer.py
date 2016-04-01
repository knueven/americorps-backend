from user import User
from db import Base, Session
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
import json
import itertools
from datetime import datetime
import enums
from enums import EducationEnum
from volunteerNeighborhoods import VolunteerNeighborhoods
from volunteerSkills import VolunteerSkills
from volunteerInterests import VolunteerInterests
from volunteerAvailability import VolunteerAvailability

class Volunteer(User):
    __tablename__ = "volunteers"
    __mapper_args__ = {'polymorphic_identity' : 'volunteer'}
    id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    # the Volunteer will have all User fields
    education = Column(Enum("Less than High School","High School diploma or equivalent","Some college, no degree","Postsecondary non-degree award","Associate's degree", "Bachelor's degree", "Master's degree", "Doctoral or professional degree", name="education_enum")) 

    neighborhoods = relationship("VolunteerNeighborhoods", order_by=VolunteerNeighborhoods.id,
        back_populates='volunteers') #enum
    interests = relationship("VolunteerInterests", order_by=VolunteerInterests.id,
        back_populates='volunteers') #enum?
    skills = relationship("VolunteerSkills", order_by=VolunteerSkills.id, back_populates='volunteers')
    availability = relationship("VolunteerAvailability", order_by=VolunteerAvailability.id,
        back_populates='volunteers') #this will need some discussion

    vhours = Column(Integer) #will be a seperate table later, could be merged into events
    events = Column(String(255)) #will need to foreignkey to another table later

    @classmethod
    def fromdict(cls, d):
        allowed = ('name', 'email', 'passwordhash', 'phone', 'last_active', 'birthdate', 
            'bio', 'gender', 'vhours', 'neighborhoods', 'interests', 'skills', 
            'education', 'availabilty', 'events')
        df = {k : v for k, v in d.items() if k in allowed}
        return cls(**df)

    def __init__(self, name, email, passwordhash, phone, last_active=datetime.now(),
        birthdate=None, bio=None, gender=None,
        vhours=None, neighborhoods=None, interests=None, 
        skills=None, education=None, availability=None, events=None):
        self.name = name
        self.email = email
        self.passwordhash = passwordhash
        self.phone = phone
        self.last_active = last_active
        self.birthdate = birthdate
        self.permissions = 'volunteer'
        self.bio = bio
        self.gender = gender
        self.vhours = vhours
        self.neighboorhoods = neighborhoods
        self.interests = interests
        self.skills = skills
        self.education = education
        self.availability = availability
        self.events = events

    # create a volunteer from a json blob
    def createVolunteer(json1):
        json_dict = json.loads(json1)
        v = Volunteer.fromdict(json_dict)
        s = Session()
        try:
            s.add(v)
            s.commit()
        except:
            return False
        finally:
            s.close()
            return True

    # take in a user id, grab the volunteer from the database and return it
    def getVolunteer(self, id):
        s = Session()
        content = s.query(Volunteer).filter_by(id = id).first()
        s.close()
        if content:
            return content
        else:
            raise ValueError("user does not exist")