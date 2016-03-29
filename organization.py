from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from app import Base, Session

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(30), nullable=False)
    state = Column(String(15), nullable=False)
    zip = Column(String(5), nullable=False)
    mission = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)
    activity = Column(String(255), nullable=False)

    # all these fields are strings
    def __init__(self, id, name, address, city, state,
                 zip, missionStatement, email, phone, lastActivity):

        # make sure th zip code is valid
        if len(zip) != 5 or not(zip.isdigit()):
            raise ValueError("a zip code must be 5 digits")
        else:
            self.zip = zip

        # make sure the phone number is valid
        if len(phone) < 10 or len(phone) > 15 or not(phone.isdigit()):
            raise ValueError('a phone number must be between 10 and 15 digits')
        else:
            self.phone = phone
        self.id = id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.mission = missionStatement
        self.email = email
        self.activity = lastActivity

        # add the organization to the database
        session = Session()
        session.add(self)
        session.commit()
        session.close()

    def __repr__(self):
        return "Organization(%s, %s)" % (self.id, self.name)

    def updateOrg(self, org_id, update_data):
        session = Session()
        try:
            session.query(Organization).filter_by(id=org_id).update(json.loads(update_data))
        except:
            session.rollback()
            raise ValueError("id not found")
        finally:
            session.close()
