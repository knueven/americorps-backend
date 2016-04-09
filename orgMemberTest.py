from orgmember import OrgMember
from db import Session
import unittest
from datetime import *
from sqlalchemy import exc
import random 
import string
# volunteer contains: self, name, email, passwordhash, phone, birthdate=None,
#             bio=None, gender=None, vhours=None, neighborhood=None, interests=None, 
#			education=None, availability=None, events=None, org=None, poc=None

class OrgMemberTests(unittest.TestCase):

    #checks if the orgmembers's fields are initialized correctly
    def test_01_init(self):
        N=15
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        michael = OrgMember('Michael Jordan', email, 'bulls', '6208675309', True, 1,
                            birthdate=date(2006, 4, 2),
                            bio='They see me rollin...', gender='Female')
        self.assertTrue(michael.name == 'Michael Jordan')
        self.assertTrue(michael.email == email)
        self.assertTrue(michael.phone == '6208675309')
        self.assertTrue(michael.poc)
        self.assertTrue(michael.org == 1)
        #self.assertTrue(michael.birthdate == '2006-04-02')
        self.assertTrue(michael.permissions == 'orgmember')
        self.assertTrue(michael.bio == 'They see me rollin...')
        self.assertTrue(michael.gender == 'Female')

    def test_02_db_write(self):
        N=15
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        michael = OrgMember('Michael Jordan', email, 'bulls', '6208675309', True, 1,
                            birthdate=date(2006, 4, 2),
                            bio='They see me rollin...', gender='Female')
        s = Session()
        try:
            s.add(michael)
            s.commit()
            s.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_03_db_pull(self):
        session = Session()
        michael = OrgMember('Michael Jordan', 'ballin@aol.com', 'bulls', '6208675309', True, 1,
                            birthdate=date(2006, 4, 2),
                            bio='They see me rollin...', gender='Female')
        sichael = session.query(OrgMember).filter_by(name='Michael Jordan').first()
        self.assertTrue(michael.name == sichael.name)
        #self.assertTrue(michael.email == sichael.email)
        self.assertTrue(michael.passwordhash != sichael.passwordhash)
        self.assertTrue(michael.phone == sichael.phone)
        self.assertTrue(michael.birthdate >= sichael.birthdate)
        self.assertTrue(michael.permissions == sichael.permissions)
        self.assertTrue(michael.bio == sichael.bio)
        self.assertTrue(michael.gender == sichael.gender)  

    #def test_orgpoc_update(self):
#        s = Session()
#        sichael = s.query(OrgMember).filter_by(name='Michael Jordan').first()
#        OrgMember.link_org(sichael)
#        self.assertTrue(True)
        
                        



if __name__ == '__main__':
    unittest.main()






