from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker
from sqlalchemy import create_engine
import user, organization, volunteer, orgmember, admin, event
from app import Base, Session, database_engine

def setup():
	Base.metadata.create_all(database_engine)

if __name__ == '__main__':
	setup()