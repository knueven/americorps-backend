from volunteer import Volunteer
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
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '03/26/16 1:00', '05/26/1990',
                         bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
                         availability="Mondays @ 3pm - 6pm", events="")
        self.assertTrue(joey.name == 'Joey Wood' and
                        joey.email == 'wood.jos@husky.neu.edu' and
                        joey.passwordhash == 'lit' and
                        joey.phone == '3015559721' and
			joey.birthdate == '05/26/1990' and
                        joey.permissions == "volunteer" and
                        joey.bio == 'Snell rhymes with hell' and
                        joey.gender == 'Male' and
			joey.vhours == 0 and
                        joey.neighborhood == "Back Bay" and
                        joey.interests == "Teaching" and 
			joey.skills == "Teaching" and
                        joey.education == "College" and
                        joey.availability == "Mondays @ 3pm - 6pm" and
                        joey.events == "")

    #test object write to the database.    
    def test_db_write(self):
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '03/26/16 1:00', '05/26/1990',
                         bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
                         availability="Mondays @ 3pm - 6pm", events="")
        s = Session()
        try:
            s.add(joey)
            s.commit()
            s.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)


    # checks if the volunteer was added to the database after initialization
    def test_queryName(self):
        session = Session()
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990',
                         bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
                         availability="Mondays @ 3pm - 6pm", events="")         
        poey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        self.assertTrue(joey.name == poey.name and
                        joey.email == poey.email and
                        joey.passwordhash == poey.passwordhash and
                        joey.phone == poey.phone and
                        joey.last_active == poey.last_active and
			joey.birthdate == poey.birthdate and
                        joey.permissions == poey.permissions and
                        joey.bio == poey.bio and
                        joey.gender == poey.gender and
			joey.vhours == poey.vhours and
                        joey.neighborhood == poey.neighborhood and
                        joey.interests == poey.interests and 
			joey.skills == poey.skills and
                        joey.education == poey.education and
                        joey.availability == poey.availability and
                        joey.events == poey.events)

    # checks if the volunteer can be queried by email
    def test_queryEmail(self):
        session = Session()
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990',
                         bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
                         availability="Mondays @ 3pm - 6pm", events="")         
        poey = session.query(Volunteer).filter_by(email='wood.jos@husky.neu.edu').first()
        self.assertTrue(joey.name == poey.name and
                        joey.email == poey.email and
                        joey.passwordhash == poey.passwordhash and
                        joey.phone == poey.phone and
                        joey.last_active == poey.last_active and
			joey.birthdate == poey.birthdate and
                        joey.permissions == poey.permissions and
                        joey.bio == poey.bio and
                        joey.gender == poey.gender and
			joey.vhours == poey.vhours and
                        joey.neighborhood == poey.neighborhood and
                        joey.interests == poey.interests and 
			joey.skills == poey.skills and
                        joey.education == poey.education and
                        joey.availability == poey.availability and
                        joey.events == poey.events)

    # checks if the volunteer can be queried by phone
    def test_queryPhone(self):
        session = Session()
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '05/26/1990',
                         bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
                         availability="Mondays @ 3pm - 6pm", events="")         
        poey = session.query(Volunteer).filter_by(phone='3015559721').first()
        self.assertTrue(joey.name == poey.name and
                        joey.email == poey.email and
                        joey.passwordhash == poey.passwordhash and
                        joey.phone == poey.phone and
                        joey.last_active == poey.last_active and
			joey.birthdate == poey.birthdate and
                        joey.permissions == poey.permissions and
                        joey.bio == poey.bio and
                        joey.gender == poey.gender and
			joey.vhours == poey.vhours and
                        joey.neighborhood == poey.neighborhood and
                        joey.interests == poey.interests and 
			joey.skills == poey.skills and
                        joey.education == poey.education and
                        joey.availability == poey.availability and
                        joey.events == poey.events)


    # # Email is valid
    # def test_phone_number_symbol(self):
    #    joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '03/26/16 1:00', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'Email must be vald')



    # # Phone is a string of 10 ints
    # def test_phone_number_symbol(self):
    #    joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '03/26/16 1:00', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'Phone numbers must be a string of 10 integers')

     # # Phone is a string of 10 ints
    # def test_phone_number<10(self):
    #    joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '03/26/16 1:00', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'Phone numbers must be a string of 10 integers')

   # Phone is a string of 10 ints
    # def test_phone_number>10(self):
    #    joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '03/26/16 1:00', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'Phone numbers must be a string of 10 integers')

    # # joey.last_active_is a string - should be in the form mm/dd/yyyy, hh:mm
    # def test_last_active_format0(self):
    #    joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '03/26/16 1:00', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'last active must be in the form mm/dd/yyyy hh:mm')

    # # joey.last_active_is a string - should be in the form mm/dd/yyyy, hh:mm
    # def test_last_active_format1(self):
    #     joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '03/26/16 1:00', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'last active must be in the form mm/dd/yyyy hh:mm')

    # # joey.last_active_must be in the past
    # def test_last_active_past(self):
    #     joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '03/26/16 1:00', '05/26/1990',
                         bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
                         availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'last active must be in the form mm/dd/yyyy hh:mm')

    # # joey.birthday is a string - should be in form mm/dd/yyyy
    # def test_birthday_format0(self):
    #     joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '03/26/16 1:00', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'birthday must be in the form mm/dd/yyyy')

    # # joey.birthday is a string - should be in the form mm/dd/yyyy
    # def test_birthday_format1(self):
    #     joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '03/26/16 1:00', '05/26/1990',
    #                     bio='Snell rhymes with hell', gender='Male', vhours=0, neighborhood="Back Bay", interests="Teaching", skills="Teaching", education="College",
    #                     availability="Mondays @ 3pm - 6pm", events="")
    #     self.assertRaises(ValueError, 'birthday must be in the form mm/dd/yyyy')

    # # joey.birthday is a string of letters - should be in the past
    # def test_birthday_past(self):
    #     joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', '03/26/16 1:00', '05/26/1990',
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





