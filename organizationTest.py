from db import Session
import unittest
from organization import *
from datetime import datetime
from sqlalchemy import exc
import random
import string
from user import User
from event import Event

#allowed = ('name', 'address', 'city', 'state', 'zip', 'mission', 'email', 'phone', 'activity')
class OrganizationTests(unittest.TestCase):



	 #checks if the events fields are initialized correctly
    def test_01_init(self):
        N=15
        logemail = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        pocemail = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        org = Organization('Test Org', logemail, 'fire', '6208675309',
                            'Mass Ave', 'Boston', 'MA', '02115', 
                            'doing charity things', pocemail)
        self.assertTrue(org.name == 'Test Org')
        #self.assertTrue(org.email == 'wood.jos@gmail.com')
        #password encrypted
        self.assertTrue(org.phone == '6208675309')
        self.assertTrue(org.address == 'Mass Ave')
        self.assertTrue(org.city == 'Boston')
        self.assertTrue(org.state == 'MA')
        self.assertTrue(org.zip == '02115')
        self.assertTrue(org.mission == 'doing charity things')
        #self.assertTrue(org.poc == 'jos.wood@husky.neu.edu')


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
        q = q.update({"email":"jos.wood@husky.neu.edu"})
        test = session.query(User).filter_by(id=test.id).first()
        self.assertTrue(test.email == 'jos.wood@husky.neu.edu')
        session.close()

#    def test_06_add_event(self):
#        s = Session()
#        org = s.query(Organization).filter_by(name="Test Org").first()
#        race = Event('Race for the Cure', 'Mass Ave', 'Boston', 'MA', '02115',
#                     'Running a marathon to raise money for cancer research', datetime(2016, 4, 2, 13, 0, 0),
#                     datetime(2016, 4, 2, 14, 0, 0), org.id, 30)
#
#        s.add(race)
#        s.commit()
#        s.close()
#        if s.query(Event).filter_by(name='Race for the Cure').first():
#            self.assertTrue(True)
#        else:
#            self.assertTrue(False)

    def test_07_password_check(self):
        session = Session()
        test = session.query(User).filter_by(name='Test Org').first()
        try:
            self.assertTrue(test.passwordhash != 'fire')
            self.assertTrue(test.check_password('fire'))
            self.assertFalse(test.check_password('Fire'))
            self.assertFalse(test.check_password('firee'))
        except exc.SQLAlchemyError:
            self.assertTrue(False)
        session.close()

    def test_08_create_org(self):
        session = Session()
        N = 15
        logemail = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        pocemail = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        json = {'name':'Test Org', 'email':logemail, 'passwordhash':'fire',
                           'phone':'6208675309', 'address':'Mass Ave', 'city':'Boston',
                           'state':'MA', 'zip':'02115', 'mission':'doing charity things',
                           'poc':pocemail}
        try:
            organization.createOrganization(json)
        except exc.SQLAlchemyError:
            self.assertTrue(False)


    def test_09_delete_self(self):
        session = Session()
        test = session.query(User).filter_by(name='Test Org').first()
        tid = test.id
        self.assertTrue(test != None)
        test.deleteSelf(session)
        org = session.query(User).filter_by(id=tid).first()
        self.assertTrue(org == None)
        events = session.query(Event).filter_by(org=id).first()
        self.assertTrue(events == None)
        session.close()

        

    def test_10_zip_long(self):
        self.assertRaises(ValueError, Organization, 'Test Org', 'wood.jos@gmail.com', 'fire', '6208675309',
                            'Mass Ave', 'Boston', 'MA', '021155', 
                            'doing charity things', 'jos.wood@husky.neu.edu')


    def test_11_zip_short(self):
        self.assertRaises(ValueError, Organization, 'Test Org', 'wood.jos@gmail.com', 'fire', '6208675309',
                            'Mass Ave', 'Boston', 'MA', '0211', 
                            'doing charity things', 'jos.wood@husky.neu.edu')

    def test_12_zip_letters(self):
        self.assertRaises(ValueError, Organization, 'Test Org', 'wood.jos@gmail.com', 'fire', '6208675309',
                            'Mass Ave', 'Boston', 'MA', 'abcde', 
                            'doing charity things', 'jos.wood@husky.neu.edu')

    def test_13_phone_long(self):
        self.assertRaises(ValueError, Organization, 'Test Org', 'wood.jos@gmail.com', 'fire', '62086753099',
                            'Mass Ave', 'Boston', 'MA', '02115', 
                            'doing charity things', 'jos.wood@husky.neu.edu')

    def test_14_phone_short(self):
        self.assertRaises(ValueError, Organization, 'Test Org', 'wood.jos@gmail.com', 'fire', '620867530',
                            'Mass Ave', 'Boston', 'MA', '02115', 
                            'doing charity things', 'jos.wood@husky.neu.edu')

    def test_15_phone_letters(self):
        self.assertRaises(ValueError, Organization, 'Test Org', 'wood.jos@gmail.com', 'fire', 'abcdefghij',
                            'Mass Ave', 'Boston', 'MA', '02115', 
                            'doing charity things', 'jos.wood@husky.neu.edu')

    
               
        

if __name__ == '__main__':
	unittest.main()
