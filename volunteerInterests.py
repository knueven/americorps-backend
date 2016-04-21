from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from db import Base, Session
from enums import InterestsEnum

class VolunteerInterests(Base):
    __tablename__ = 'volunteerInterests'

    id = Column(Integer, primary_key=True)
    interest = Column(Enum("youth","seniors","education","environment","health","arts","financialemp","veterans","immigration","animals","mentoring","homeless","lgbt","domestic","hunger","disabilities",
                name="interests_enum"), nullable=False)
    volunteer_id = Column(Integer, ForeignKey('volunteers.id'))

    #volunteers = relationship("Volunteer", back_populates="volunteerInterests")

    def __init__(self, interest, volunteer_id):
        self.interest = interest
        self.volunteer_id = volunteer_id

    def __repr__(self):
        return "<VolunteerInterests(interest='%s')>" % (self.interest)


    def create_v_interests(volunteer_id, interests):
        s = Session()
        try:
            for i in interests: 
                v = VolunteerInterests(i, volunteer_id)
                s.add(v)

            s.commit()
        except:
            return False
        finally:
            s.close()
        return True

    def get_interests(id):
        s = Session()
        result = []
        q = s.query(VolunteerInterests).filter_by(volunteer_id=id)
        for n in q:
            result.append(n.interest)
        s.close()
        return result

