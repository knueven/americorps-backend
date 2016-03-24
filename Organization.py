from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker

Base = declarative_base()
# replace with config setting for database
database_engine = create_engine("mysql://...")
Session = sessionmaker(bind=database_engine)


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
        self.id = id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.mission = missionStatement
        self.email = email
        self.phone = phone
        self.activity = lastActivity

    def __repr__(self):
        return "Organization(%s, %s)" % (self.id, self.name)

    def updateOrg(self, org_id, update_data):
        session = Session()
        try:
            session.query(organizations).filter_by(id=org_id).update(json.loads(update_data))
        except:
            session.rollback()
            raise ValueError("id not found")
        finally:
            session.close()
