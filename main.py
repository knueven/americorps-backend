from views import *
from db import Base, Session, database_engine
from app import app
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker
from sqlalchemy import create_engine
import config
import volunteer
import volunteerAvailability
import volunteerInterests
import volunteerNeighborhoods
import volunteerSkills
import user
import admin
import organization
import orgmember
import event
import eventInterests
import eventNeighborhoods
import eventSkills
import attendee
import sys


def setup():
    Base.metadata.create_all(database_engine)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		setup()
		sys.exit()
	else:
		app.run(debug=config.isDev)

