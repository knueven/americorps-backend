from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker
from sqlalchemy import create_engine
import main

Base = declarative_base()
#replace with config setting for database
import config
database_engine = create_engine(config.database_config)
Session = sessionmaker(bind=database_engine)

if __name__ == '__main__':
    main.setup()

