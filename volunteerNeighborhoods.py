from db import Base, Session
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from enums import NeighborhoodsEnum


class VolunteerNeighborhoods(Base):
    __tablename__ = 'volunteerNeighborhoods'

    id = Column(Integer, primary_key=True)
    neighborhood = Column(Enum("allston",
                               "backbay",
                               "bayvillage",
                               "beaconhill",
                               "brighton",
                               "charlestown",
                               "chinatown",
                               "dorchester",
                               "downtown",
                               "eastboston",
                               "fenwaykenmore",
                               "hyde",
                               "jamaica",
                               "mattapan",
                               "middorchester",
                               "missionhill",
                               "northend",
                               "roslindale",
                               "roxbury",
                               "southboston",
                               "southend",
                               "westend",
                               "westroxbury",
                               "greater", name="neighborhoods_enum"), nullable=False)
    volunteer_id = Column(Integer, ForeignKey('volunteers.id'))

    # volunteers = relationship("Volunteer", back_populates="volunteerNeighborhoods")

    def __init__(self, neighborhood, volunteer_id):
        self.neighborhood = neighborhood
        self.volunteer_id = volunteer_id

    def __repr__(self):
        return "<VolunteerNeighborhoods(neighborhood='%s')>" % (self.neighborhood)

    def create_v_neighborhood(volunteer_id, neighborhoods):
        s = Session()
        try:
            for n in neighborhoods:
                v = VolunteerNeighborhoods(n, volunteer_id)
                s.add(v)
            s.commit()
        except:
            s.rollback()
            return False
        finally:
            s.close()
        return True

    def get_neighborhoods(id):
        s = Session()
        result = []
        q = s.query(VolunteerNeighborhoods).filter_by(volunteer_id=id)
        for n in q:
          result.append(n.neighborhood)
        s.close()
        return result
