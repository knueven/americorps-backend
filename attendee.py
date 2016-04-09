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

class Attendee(Base):
    __tablename__ = 'attendees'
    key = Column(Integer, primary_key=True, nullable=False)
    userID = Column(Integer, ForeignKey('users.id'), nullable=False)
    eventID = Column(Integer, ForeignKey('events.id'), nullable=False)
    confirmed = Column(Boolean, nullable=False)
    hours = Column(Integer)
    hoursValidated = Column(Boolean, nullable=False)

    def __init__(self, user, event):
        self.userID = user
        self.eventID = event
        self.confirmed = True
        self.hours = 0
        self.hoursValidated = True

    def addRelation(self, user, event):
        s = Session()
        attendee = Attendee(user,event)
        try:
            s.add(attendee)
            s.commit()
        except:
            return False
        finally:
            s.close()
        return True





