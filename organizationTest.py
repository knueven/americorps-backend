from db import Session
import unittest
from organization import Organization
from datetime import datetime
from sqlalchemy import exc
#allowed = ('name', 'address', 'city', 'state', 'zip', 'mission', 'email', 'phone', 'activity')
class OrganizationTests(unittest.TestCase):

	 #checks if the events fields are initialized correctly
    def test_init(self):
        race = Organization('Test Org', 'Mass Ave', 'Boston', 'MA', '02115', 
            'doing charity things')
        print('\n')
        self.assertTrue(race.name == 'Test Org')
        self.assertTrue(race.address == 'Mass Ave')
        self.assertTrue(race.city == 'Boston')
        self.assertTrue(race.state == 'MA')
        self.assertTrue(race.zip == '02115')
        self.assertTrue(race.mission == 'doing charity things')


    def test_db_write(self):
        race = Organization('Test Org', 'Mass Ave', 'Boston', 'MA', '02115', 
           'doing charity things')
        print(race.poc)
        s = Session()
        try:
            s.add(race)
            s.commit()
            s.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_db_pull(self):
        session = Session()
        race = Organization('Test Org', 'Mass Ave', 'Boston', 'MA', '02115', 
           'doing charity things')
        face = session.query(Organization).filter_by(address='Mass Ave').first()
        self.assertTrue(race.name == face.name)
        self.assertTrue(race.city == face.city)
        self.assertTrue(race.state == face.state)
        self.assertTrue(race.mission == face.mission)

        

if __name__ == '__main__':
	unittest.main()
