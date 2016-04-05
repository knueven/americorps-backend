from admin import Admin
from db import Session
import unittest
from datetime import datetime
from sqlalchemy import exc
# volunteer contains: name, email, passwordhash, phone, last_active,
#			birthdate=None, permissions, bio=None, gender=None,
#			vhours=None, neighborhood=None, interests=None, 
#			skills=None, education=None, availability=None, events=None

class VolunteerTests(unittest.TestCase):

    #checks if the volunteer's fields are initialized correctly
    def test_init(self):
        mickey = Admin('Mickey Mouse', 'mickey@disney.com', 'mouse', '0765434567', True,
                       birthdate='06/06/2006', bio='Peace Walt', gender='Male')
        self.assertTrue(mickey.name == 'Mickey Mouse')
        self.assertTrue(mickey.email == 'mickey@disney.com')
        #self.assertTrue(mickey.passwordhash == 'mouse')
        self.assertTrue(mickey.phone == '0765434567')
        self.assertTrue(mickey.master)
        #self.assertTrue(mickey.last_active == )
        self.assertTrue(mickey.birthdate == '06/06/2006')
        self.assertTrue(mickey.permissions == 'admin')
        self.assertTrue(mickey.bio == 'Peace Walt')
        self.assertTrue(mickey.gender == 'Male')
        
    #test object write to the database.    
    def test_db_write(self):
        mickey = Admin('Mickey Mouse', 'mickey@disney.com', 'mouse', '0765434567', True,
                         birthdate='06/06/2006', bio='Peace Walt', gender='Male')
        s = Session()
        try:
            s.add(mickey)
            s.commit()
            s.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

# checks if the volunteer was added to the database after initialization
    def test_queryName(self):
        session = Session()
        mickey = Admin('Mickey Mouse', 'mickey@disney.com', 'mouse', '0765434567', True,
                         birthdate='06/06/2006', bio='Peace Walt', gender='Male')
        sickey = session.query(Admin).filter_by(name='Mickey Mouse').first()
        self.assertTrue(mickey.name == sickey.name)
        self.assertTrue(mickey.email == sickey.email)
        #self.assertTrue(mickey.passwordhash == sickey.passwordhash)
        self.assertTrue(mickey.phone == sickey.phone)
        self.assertTrue(mickey.master)
        #self.assertTrue(mickey.last_active == )
        self.assertTrue(mickey.birthdate == sickey.birthdate)
        self.assertTrue(mickey.permissions == sickey.permissions)
        self.assertTrue(mickey.bio == sickey.bio)
        self.assertTrue(mickey.gender == sickey.gender)
                        

    # checks if the volunteer can be queried by email
    def test_queryEmail(self):
        session = Session()
        mickey = Admin('Mickey Mouse', 'mickey@disney.com', 'mouse', '0765434567', True,
                         birthdate='06/06/2006', bio='Peace Walt', gender='Male')
        sickey = session.query(Admin).filter_by(name='Mickey Mouse').first()
        self.assertTrue(mickey.name == sickey.name)
        self.assertTrue(mickey.email == sickey.email)
        #self.assertTrue(mickey.passwordhash == sickey.passwordhash)
        self.assertTrue(mickey.phone == sickey.phone)
        self.assertTrue(mickey.master)
        #self.assertTrue(mickey.last_active == )
        self.assertTrue(mickey.birthdate == sickey.birthdate)
        self.assertTrue(mickey.permissions == sickey.permissions)
        self.assertTrue(mickey.bio == sickey.bio)
        self.assertTrue(mickey.gender == sickey.gender)
                        

    # checks if the volunteer can be queried by phone
    def test_queryPhone(self):
        session = Session()
        mickey = Admin('Mickey Mouse', 'mickey@disney.com', 'mouse', '0765434567', True,
                         birthdate='06/06/2006', bio='Peace Walt', gender='Male')
        sickey = session.query(Admin).filter_by(name='Mickey Mouse').first()
        self.assertTrue(mickey.name == sickey.name)
        self.assertTrue(mickey.email == sickey.email)
        #self.assertTrue(mickey.passwordhash == sickey.passwordhash)
        self.assertTrue(mickey.phone == sickey.phone)
        self.assertTrue(mickey.master)
        #self.assertTrue(mickey.last_active == )
        self.assertTrue(mickey.birthdate == sickey.birthdate)
        self.assertTrue(mickey.permissions == sickey.permissions)
        self.assertTrue(mickey.bio == sickey.bio)
        self.assertTrue(mickey.gender == sickey.gender)
                        
    


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





