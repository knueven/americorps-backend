from sqlalchemy import *
from sqlalchemy import exc
from sqlalchemy.orm import relation, sessionmaker, relationship
from db import Base, Session
import json
import enums
from eventNeighborhoods import EventNeighborhoods
from eventSkills import EventSkills
from eventInterests import EventInterests
from datetime import *
from attendee import Attendee

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(30), nullable=False)
    state = Column(String(15), nullable=False)
    zip = Column(String(5), nullable=False)
    about = Column(String(255), nullable=False)
    start_at = Column(DateTime(255), nullable=False)
    posted_at = Column(DateTime(255), nullable=False)
    end_at = Column(DateTime(255), nullable=False)
    org = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    org_name = Column(String(255))
    capacity = Column(Integer, nullable=True)
    featured = Column(Boolean)
    

    @classmethod
    def fromdict(cls, d):
        allowed = ('name', 'address', 'city', 'state', 'zip', 'about', 
                   'start_at', 'end_at', 'org', 'org_name', 'capacity', 'featured')
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

    # all these fields are strings
    def __init__(self, name, address, city, state,
                 zip, about, start_at, end_at, org, org_name=None, capacity=None, featured=None):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        if len(zip) != 5 or zip.isdigit() == False:
            raise ValueError("zip codes must be 5 digits long")
        else:
            self.zip = zip
        self.about = about
        self.start_at = start_at
        self.posted_at = datetime.now()
        self.end_at = end_at
        self.org = org
        self.org_name = org_name
        if capacity < 0:
            raise ValueError("capacity cannot be less than zero")
        else:
            self.capacity = capacity
        self.featured = featured

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
        print("skills")
        s = json.loads(json.dumps(json1))
        skills = s['skills']
        print(skills)
        EventSkills.createvskills(volun_id, skills)
        return

    def grab_interests(volun_id, json1):
        i = json.loads(json.dumps(json1))
        interests = i['interests']
        EventInterests.create_v_interests(volun_id, interests)

    def deleteSelf(self, session):
        attendees = session.query(Attendee).filter_by(eventID=self.id)
        if attendees:
            for attendee in attendees:
                try:
                    session.delete(attendee)
                except:
                    raise exc.SQLAlchemyError("failed to delete attendee " + attendee.key)
            try:
                session.commit()
                session.delete(self)
            except:
                raise exc.SQLAlchemyError("failed to delete event " + self.id)

# create an event from a json string
def createEvent(json):
    e = Event.fromdict(json)
    s = Session()
    try:
        s.add(e)
        s.commit()
    except:
        return False
    finally:
        s.close()
    v2 = Event.fromdict(json)
    createEventEnums(v2, json)
    return True

def createEventEnums(v, json):
    s = Session()
    try:
        v1 = s.query(Event).filter_by(name=v.name).first()
        Event.grab_skills(v1.id, json)
        Event.grab_interests(v1.id, json)
    except:
        return False
    finally:
        s.close()
    return True



