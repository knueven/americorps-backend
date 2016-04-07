from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship
from db import Base, Session
import organization
import json
import enums
from eventNeighborhoods import EventNeighborhoods
from eventSkills import EventSkills
from eventInterests import EventInterests

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(30), nullable=False)
    state = Column(String(15), nullable=False)
    zip = Column(String(5), nullable=False)
    about = Column(String(255), nullable=False)
    start_at = Column(String(255), nullable=False)    
    posted_at = Column(String(255), nullable=False)
    end_at = Column(String(255), nullable=False)
    org = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    capacity = Column(Integer, nullable=True)

    @classmethod
    def fromdict(cls, d):
        allowed = ('name', 'address', 'city', 'state', 'zip', 'about', 
                   'start_at', 'posted_at', 'duration', 'eventNeighborhoods',
                    'eventInterests', 'eventSkills', 'org', 'capacity')
        df = {k: e for k,e in d.items() if k in allowed}
        return cls(**df)


    # all these fields are strings
    def __init__(self, name, address, city, state,
                 zip, about, start_at, posted_at, duration, eventNeighborhoods,
                 eventInterests, eventSkills, org, capacity=None):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.about = about
        self.start_at = start_at
        self.posted_at = posted_at
        self.duration = duration
        # self.eventNeighborhoods = eventNeighborhoods
        # self.eventInterests = eventInterests
        # self.eventSkills = eventSkills
        self.org = org
        self.capacity = capacity

        # if eventInterests is None:
        #     self.eventInterests = []
        # else:
        #     self.eventInterests = eventInterests
        # if eventSkills is None:
        #     self.eventSkils = []
        # else:
        #     self.eventSkills = eventSkills

        # Update a user (must exist)
    def updateEvent(self, event_id, update_data):
        session = Session()
        try:
            session.query(Event).filter_by(id=event_id).update(json.loads(update_data))
        except:
            session.rollback()
            raise #exception of some sort
        finally:
            session.close()


    def grab_skills(volun_id, json1):
        s = json.loads(json.dumps(json1))
        skills = s['skills']
        EventSkills.createvskills(volun_id, skills)

    def grab_interests(volun_id, json1):
        i = json.loads(json.dumps(json1))
        interests = i['interests']
        EventInterests.create_v_interests(volun_id, interests)

