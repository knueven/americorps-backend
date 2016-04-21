from admin import Admin
from db import Session
import unittest
from user import User
from datetime import *
from sqlalchemy import exc
import random
import string
# volunteer contains: name, email, passwordhash, phone, last_active,
#			birthdate=None, permissions, bio=None, gender=None,
#			vhours=None, neighborhood=None, interests=None, 
#			skills=None, education=None, availability=None, events=None

class AdminTests(unittest.TestCase):



    #checks if the volunteer's fields are initialized correctly
    def test_01_init(self):
        N=10
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        mickey = Admin('Mickey Mouse', email, 'mouse', '0765434567', True,
                       birthdate=date(2006, 6, 6), bio='Peace Walt', gender='Male')
        self.assertTrue(mickey.name == 'Mickey Mouse')
        #self.assertTrue(mickey.email == 'wood.jos@husky.neu.edu')
        #self.assertTrue(mickey.passwordhash == 'mouse')
        self.assertTrue(mickey.phone == '0765434567')
        self.assertTrue(mickey.master)
        #self.assertTrue(mickey.last_active == )
        #self.assertTrue(mickey.birthdate == '06/06/2006')
        self.assertTrue(mickey.permissions == 'admin')
        self.assertTrue(mickey.bio == 'Peace Walt')
        self.assertTrue(mickey.gender == 'Male')
        
    #test object write to the database.    
    def test_02_db_write(self):
        N=15
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        mickey = Admin('Mickey Mouse', email, 'mouse', '0765434567', True,
                         birthdate=date(2006, 6, 6), bio='Peace Walt', gender='Male')
        s = Session()
        try:
            s.add(mickey)
            s.commit()
            s.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

# checks if the volunteer was added to the database after initialization
    def test_03_queryName(self):
        session = Session()
        mickey = Admin('Mickey Mouse', 'mickey@disney.com', 'mouse', '0765434567', True,
                         birthdate=date(2006, 6, 6), bio='Peace Walt', gender='Male')
        sickey = session.query(Admin).filter_by(name='Mickey Mouse').first()
        self.assertTrue(mickey.name == sickey.name)
        #self.assertTrue(mickey.email == sickey.email)
        #self.assertTrue(mickey.passwordhash == sickey.passwordhash)
        self.assertTrue(mickey.phone == sickey.phone)
        self.assertTrue(mickey.master)
        #self.assertTrue(mickey.last_active == )
        self.assertTrue(mickey.birthdate == sickey.birthdate)
        self.assertTrue(mickey.permissions == sickey.permissions)
        self.assertTrue(mickey.bio == sickey.bio)
        self.assertTrue(mickey.gender == sickey.gender)
                        
                        

    # checks if the volunteer can be queried by phone
    def test_05_queryPhone(self):
        session = Session()
        mickey = Admin('Mickey Mouse', 'mickey@disney.com', 'mouse', '0765434567', True,
                         birthdate=date(2006, 6, 6), bio='Peace Walt', gender='Male')
        sickey = session.query(Admin).filter_by(name='Mickey Mouse').first()
        self.assertTrue(mickey.name == sickey.name)
        #cself.assertTrue(mickey.email == sickey.email)
        #self.assertTrue(mickey.passwordhash == sickey.passwordhash)
        self.assertTrue(mickey.phone == sickey.phone)
        self.assertTrue(mickey.master)
        #self.assertTrue(mickey.last_active == )
        self.assertTrue(mickey.birthdate == sickey.birthdate)
        self.assertTrue(mickey.permissions == sickey.permissions)
        self.assertTrue(mickey.bio == sickey.bio)
        self.assertTrue(mickey.gender == sickey.gender)

    def test_06_updating_name(self):
        session = Session()
        mickey = session.query(User).filter_by(name='Mickey Mouse').first()
        q = session.query(User).filter_by(id=mickey.id)
        q = q.update({"name":"Wood Joey"})
        mickey = session.query(User).filter_by(id=mickey.id).first()
        self.assertTrue(mickey.name == 'Wood Joey')
        session.close()

    def test_07_updating_email(self):
        session = Session()
        mickey = session.query(User).filter_by(name='Mickey Mouse').first()
        q = session.query(User).filter_by(id=mickey.id)
        q = q.update({"email":"jos.wood1@husky.neu.edu"})
        mickey = session.query(User).filter_by(id=mickey.id).first()
        self.assertTrue(mickey.email == 'jos.wood1@husky.neu.edu')
        session.close()

    def test_08_phone_long(self):
        N=10
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        self.assertRaises(ValueError, Admin, 'Mickey Mouse', email, 'mouse', '07654345677', True,
                       birthdate=date(2006, 6, 6), bio='Peace Walt', gender='Male')

    def test_09_phone_short(self):
        N=10
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        self.assertRaises(ValueError, Admin, 'Mickey Mouse', email, 'mouse', '076543456', True,
                       birthdate=date(2006, 6, 6), bio='Peace Walt', gender='Male')

    def test_10_phone_letters(self):
        N=10
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        self.assertRaises(ValueError, Admin, 'Mickey Mouse', email, 'mouse', 'abcdefghij', True,
                       birthdate=date(2006, 6, 6), bio='Peace Walt', gender='Male')

    #unit test for password hashing
    def test_11_password_hash(self):
        session = Session()
        N=10
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        mickey = Admin('Mickey Mouse', email, 'mouse', '0765434567', True,
                       birthdate=date(2006, 6, 6), bio='Peace Walt', gender='Male')
        try:
            session.add(mickey)
            session.commit()
            rickey = session.query(Admin).filter_by(phone='0765434567').first()
            self.assertTrue(mickey.passwordhash != 'mouse')
            self.assertTrue(rickey.passwordhash != 'mouse')
            self.assertTrue(mickey.check_password('mouse'))
            self.assertFalse(mickey.check_password('mouse2'))
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)
                        
    


    # # Email is valid
    # def test_phone_number_symbol(self):
    #    joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'Email must be vald')



    # # Phone is a string of 10 ints
    # def test_phone_number_symbol(self):
    #    joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'Phone numbers must be a string of 10 integers')

     # # Phone is a string of 10 ints
    # def test_phone_number<10(self):
    #    joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'Phone numbers must be a string of 10 integers')

   # Phone is a string of 10 ints
    # def test_phone_number>10(self):
    #    joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'Phone numbers must be a string of 10 integers')

    # # joey.last_active_is a string - should be in the form mm/dd/yyyy, hh:mm
    # def test_last_active_format0(self):
    #    joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'last active must be in the form mm/dd/yyyy hh:mm')

    # # joey.last_active_is a string - should be in the form mm/dd/yyyy, hh:mm
    # def test_last_active_format1(self):
    #     joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'last active must be in the form mm/dd/yyyy hh:mm')

    # # joey.last_active_must be in the past
    # def test_last_active_past(self):
    #     joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990'
    #                    bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'last active must be in the form mm/dd/yyyy hh:mm')

    # # joey.birthday is a string - should be in form mm/dd/yyyy
    # def test_birthday_format0(self):
    #     joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'birthday must be in the form mm/dd/yyyy')

    # # joey.birthday is a string - should be in the form mm/dd/yyyy
    # def test_birthday_format1(self):
    #     joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'birthday must be in the form mm/dd/yyyy')

    # # joey.birthday is a string of letters - should be in the past
    # def test_birthday_past(self):
    #     joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'birthday must be in the past')


    # These tests require the Interest and Skills Enumerations to be created

    # # joey.interests should exist in the interests table
    # def test_interests_exists(self):
    #     session = Session()
    #     self.assertEqual(self.joey.interests, session.query(Interests).filter_by(name=self.joey.interests).first())
    #     session.close()
    #
    # # joey.skills should exist in the skills table
    # def test_skills_exists(self):
    #     session = Session()
    #     self.assertEqual(self.joey.skills, session.query(Skills).filter_by(name=self.joey.skills).first())
    #     session.close()

        




if __name__ == '__main__':
    unittest.main()





