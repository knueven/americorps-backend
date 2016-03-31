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
            'doing charity things', 
            '12345@gmail.com', '1234567890', 'walking')
        print('\n')
        print(race.activity)
        self.assertTrue(race.name == 'tTest Org' and
                        race.address == 'Mass Ave' and
                        race.city == 'Boston' and
                        race.state == 'MA' and
                        race.zip == '02115' and
                        race.mission == 'doing charity things' and
                        race.email == '12345@gmail.com' and
                        race.phone == '1234567890' and
                        race.activity == 'walking')


        #test object write to the database.    
    def test_db_write(self):
        race = Organization('Test Org', 'Mass Ave', 'Boston', 'MA', '02115', 
           'doing charity things', 
           '12345@gmail.com', '1234567890', 'walking around aimlessly')
        s = Session()
        try:
            s.add(race)
            s.commit()
            s.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

if __name__ == '__main__':
	unittest.main()