from orgmember import OrgMember
from db import Session
import unittest
from datetime import datetime
from sqlalchemy import exc
# volunteer contains: self, name, email, passwordhash, phone, birthdate=None,
#             bio=None, gender=None, vhours=None, neighborhood=None, interests=None, 
#			education=None, availability=None, events=None, org=None, poc=None

class OrgMemberTests(unittest.TestCase):

    #checks if the orgmembers's fields are initialized correctly
    def test_init(self):
        michael = OrgMember('Michael Jordan', 'ballin@aol.com', 'bulls', '6208675309', True, 1, birthdate='02/04/2006',
                            bio='They see me rollin...', gender='Female')
        self.assertTrue(michael.name == 'Michael Jordan')
        self.assertTrue(michael.email == 'ballin@aol.com')
        self.assertTrue(michael.phone == '6208675309')
        self.assertTrue(michael.poc)
        self.assertTrue(michael.org == 1)
        #self.assertTrue(michael.last_active == )
        self.assertTrue(michael.birthdate == '02/04/2006')
        self.assertTrue(michael.permissions == 'orgmember')
        self.assertTrue(michael.bio == 'They see me rollin...')
        self.assertTrue(michael.gender == 'Female')

    def test_db_write(self):
        michael = OrgMember('Michael Jordan', 'ballin@aol.com', 'bulls', '6208675309', True, 1, birthdate='02/04/2006',
                            bio='They see me rollin...', gender='Female')
        s = Session()
        try:
            s.add(michael)
            s.commit()
            s.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_db_pull(self):
        session = Session()
        michael = OrgMember('Michael Jordan', 'ballin@aol.com', 'bulls', '6208675309', True, 1, birthdate='02/04/2006',
                            bio='They see me rollin...', gender='Female')
        sichael = session.query(OrgMember).filter_by(name='Michael Jordan').first()
        self.assertTrue(michael.name == sichael.name)
        self.assertTrue(michael.email == sichael.email)
        self.assertTrue(michael.passwordhash != sichael.passwordhash)
        self.assertTrue(michael.phone == sichael.phone)
        self.assertTrue(michael.birthdate == sichael.birthdate)
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






