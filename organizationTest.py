from db import Session
import unittest
from organization import Organization
from datetime import datetime
from sqlalchemy import exc
import random
import string
from user import User

#allowed = ('name', 'address', 'city', 'state', 'zip', 'mission', 'email', 'phone', 'activity')
class OrganizationTests(unittest.TestCase):

	 #checks if the events fields are initialized correctly
    def test_01_init(self):
        
        org = Organization('Test Org', 'wood.jos@gmail.com', 'fire', '6208675309',
                            'Mass Ave', 'Boston', 'MA', '02115', 
                            'doing charity things', 'jos.wood@husky.neu.edu')
        self.assertTrue(org.name == 'Test Org')
        self.assertTrue(org.email == 'wood.jos@gmail.com')
        #password encrypted
        self.assertTrue(org.phone == '6208675309')
        self.assertTrue(org.address == 'Mass Ave')
        self.assertTrue(org.city == 'Boston')
        self.assertTrue(org.state == 'MA')
        self.assertTrue(org.zip == '02115')
        self.assertTrue(org.mission == 'doing charity things')
        self.assertTrue(org.poc == 'jos.wood@husky.neu.edu')


    def test_02_db_write(self):
        N=15
        logemail = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        pocemail = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        org = Organization('Test Org', logemail, 'fire', '6208675309',
                            'Mass Ave', 'Boston', 'MA', '02115', 
                            'doing charity things', pocemail)

        s = Session()
        try:
            s.add(org)
            s.commit()
            s.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_03_db_pull(self):
        session = Session()
        org = Organization('Test Org', 'wood.jos@gmail.com', 'fire', '6208675309',
                            'Mass Ave', 'Boston', 'MA', '02115', 
                            'doing charity things', 'jos.wood@husky.neu.edu')

        borg = session.query(Organization).filter_by(address='Mass Ave').first()
        self.assertTrue(org.name == borg.name)
        self.assertTrue(org.phone == borg.phone)
        self.assertTrue(org.address == borg.address)
        self.assertTrue(org.zip == borg.zip)
        self.assertTrue(org.city == borg.city)
        self.assertTrue(org.state == borg.state)
        self.assertTrue(org.mission == borg.mission)

    def test_04_updating_name(self):
        session = Session()
        test = session.query(User).filter_by(name='Test Org').first()
        q = session.query(User).filter_by(id=test.id)
        q = q.update({"name":"Wood Joey"})
        test = session.query(User).filter_by(id=test.id).first()
        self.assertTrue(test.name == 'Wood Joey')
        session.close()

    def test_05_updating_email(self):
        session = Session()
        test = session.query(User).filter_by(name='Test Org').first()
        q = session.query(User).filter_by(id=test.id)
        q = q.update({"email":"wood.jos@husky.neu.edu"})
        test = session.query(User).filter_by(id=test.id).first()
        self.assertTrue(test.email == 'wood.jos@husky.neu.edu')
        session.close()
        

if __name__ == '__main__':
	unittest.main()
