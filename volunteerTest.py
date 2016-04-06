from volunteer import Volunteer
from db import Session
import unittest
from datetime import datetime
from sqlalchemy import exc
from volunteerNeighborhoods import VolunteerNeighborhoods
from volunteerInterests import VolunteerInterests
from volunteerSkills import VolunteerSkills
from volunteerAvailability import VolunteerAvailability
# volunteer contains: name, email, passwordhash, phone, last_active,
#			birthdate=None, permissions, bio=None, gender=None,
#			vhours=None, neighborhood=None, interests=None, 
#			skills=None, education=None, availability=None, events=None

class VolunteerTests(unittest.TestCase):

    #checks if the volunteer's fields are initialized correctly
    def test_init(self):
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721',
                         birthdate= '05/26/1990', bio='Snell rhymes with hell', gender='Male',
                         vhours=0, education="Some college, no degree")
        self.assertTrue(joey.name == 'Joey Wood')
        self.assertTrue(joey.email == 'wood.jos@husky.neu.edu')
        self.assertTrue(joey.passwordhash != 'lit')
        self.assertTrue(joey.phone == '3015559721')
        #self.assertTrue(joey.last_active == )
        self.assertTrue(joey.birthdate == '05/26/1990')
        self.assertTrue(joey.permissions == 'volunteer')
        self.assertTrue(joey.bio == 'Snell rhymes with hell')
        self.assertTrue(joey.gender == 'Male')
        self.assertTrue(joey.vhours == 0)
        #self.assertTrue(joey.neighborhoods.neighborhood == "Back Bay")
        #self.assertTrue(joey.interests == "Teaching") 
        #self.assertTrue(joey.skills == "Teaching")
        self.assertTrue(joey.education == "Some college, no degree")
        #self.assertTrue(joey.availability == 'Mondays @ 3pm - 6pm')


    #test object write to the database.    
    def test_db_write(self):
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721',
                         birthdate='05/26/1990', bio='Snell rhymes with hell', gender='Male',
                         vhours=0, education="Some college, no degree")
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
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721',
                         birthdate= '05/26/1990', bio='Snell rhymes with hell', gender='Male',
                         vhours=0, education="Some college, no degree")        
        poey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        self.assertTrue(joey.name == poey.name)
        self.assertTrue(joey.email == poey.email)
        self.assertTrue(joey.passwordhash != poey.passwordhash)
        self.assertTrue(joey.phone == poey.phone)
        #self.assertTrue(joey.last_active == poey.last_active)
        self.assertTrue(joey.birthdate == poey.birthdate)
        self.assertTrue(joey.permissions == poey.permissions)
        self.assertTrue(joey.bio == poey.bio)
        self.assertTrue(joey.gender == poey.gender)
        self.assertTrue(joey.vhours == poey.vhours)
        #self.assertTrue(joey.neighborhoods == poey.neighborhoods)
        #self.assertTrue(joey.interests == poey.interests) 
        #self.assertTrue(joey.skills == poey.skills)
        self.assertTrue(joey.education == poey.education)
        #self.assertTrue(joey.availability == poey.availability)
        #self.assertTrue(joey.events == poey.events)


                        

    # checks if the volunteer can be queried by email
    def test_queryEmail(self):

        session = Session()
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721',
                         birthdate= '05/26/1990', bio='Snell rhymes with hell', gender='Male',
                         vhours=0, education="Some college, no degree")
        poey = session.query(Volunteer).filter_by(email='wood.jos@husky.neu.edu').first()
        self.assertTrue(joey.name == poey.name)
        self.assertTrue(joey.email == poey.email)
        self.assertTrue(joey.passwordhash != poey.passwordhash)
        self.assertTrue(joey.phone == poey.phone)
        #self.assertTrue(joey.last_active == poey.last_active)
        self.assertTrue(joey.birthdate == poey.birthdate)
        self.assertTrue(joey.permissions == poey.permissions)
        self.assertTrue(joey.bio == poey.bio)
        self.assertTrue(joey.gender == poey.gender)
        self.assertTrue(joey.vhours == poey.vhours)
        #self.assertTrue(joey.neighborhoods == poey.neighborhoods)
        #self.assertTrue(joey.interests == poey.interests) 
        #self.assertTrue(joey.skills == poey.skills)
        self.assertTrue(joey.education == poey.education)
        #self.assertTrue(joey.availability == poey.availability)
        #self.assertTrue(joey.events == poey.events)
                        

    # checks if the volunteer can be queried by phone
    def test_queryPhone(self):
        session = Session()
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721',
                         birthdate= '05/26/1990', bio='Snell rhymes with hell', gender='Male',
                         vhours=0, education="Some college, no degree")         
        poey = session.query(Volunteer).filter_by(phone='3015559721').first()
        self.assertTrue(joey.name == poey.name)
        self.assertTrue(joey.email == poey.email)
      #  self.assertTrue(joey.passwordhash == poey.passwordhash)
        self.assertTrue(joey.phone == poey.phone)
        #self.assertTrue(joey.last_active == poey.last_active)
        self.assertTrue(joey.birthdate == poey.birthdate)
        self.assertTrue(joey.permissions == poey.permissions)
        self.assertTrue(joey.bio == poey.bio)
        self.assertTrue(joey.gender == poey.gender)
        self.assertTrue(joey.vhours == poey.vhours)
        #self.assertTrue(joey.neighborhoods == poey.neighborhoods)
        #self.assertTrue(joey.interests == poey.interests) 
        #self.assertTrue(joey.skills == poey.skills)
        self.assertTrue(joey.education == poey.education)
        #self.assertTrue(joey.availability == poey.availability)
        #self.assertTrue(joey.events == poey.events)

    #unit test for password hashing
    def test_password_hash(self):
        session = Session()
        vol = Volunteer('Test', '2234@gmail.com', 'lit', '3015559725',
                         birthdate= '05/26/1990', bio='Snell rhymes with hell', gender='Male',
                         vhours=0, education="Some college, no degree")  
        try:
            session.add(vol)
            session.commit()
            poey = session.query(Volunteer).filter_by(phone='3015559725').first()
            self.assertTrue(vol.passwordhash != 'lit')
            self.assertTrue(poey.passwordhash != 'lit')
            self.assertTrue(vol.check_password('lit'))
            self.assertFalse(vol.check_password('lit2'))
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)


    def test_interests_write(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerInterests("Youth", joey.id)
        self.assertTrue(moey.interest == "Youth")
        try:
            session.add(moey)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_interests(self):
        session = Session()
        doey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerInterests("Youth", doey.id)
        joey = session.query(VolunteerInterests).filter_by(volunteer_id=25).first()
        self.assertTrue(moey.interest == joey.interest)

    def test_neighborhood_write(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerNeighborhoods("Back Bay", joey.id)
        self.assertTrue(moey.neighborhood == "Back Bay")
        try:
            session.add(moey)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_neighborhoods(self):
        session = Session()
        doey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerNeighborhoods("Back Bay", doey.id)
        joey = session.query(VolunteerNeighborhoods).filter_by(volunteer_id=25).first()
        self.assertTrue(moey.neighborhood == joey.neighborhood)

    def test_skill_write(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerSkills("Teaching/Tutoring", joey.id)
        self.assertTrue(moey.skill == "Teaching/Tutoring")
        try:
            session.add(moey)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_skills(self):
        session = Session()
        doey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerSkills("Teaching/Tutoring", doey.id)
        joey = session.query(VolunteerSkills).filter_by(volunteer_id=25).first()
        self.assertTrue(moey.skill == joey.skill)

    def test_availability_write(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerAvailability("Monday", joey.id)
        self.assertTrue(moey.day == "Monday")
        try:
            session.add(moey)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_availability(self):
        session = Session()
        doey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerAvailability("Monday", doey.id)
        joey = session.query(VolunteerAvailability).filter_by(volunteer_id=doey.id).first()
        self.assertTrue(moey.day == joey.day)

        # vol = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559725',
        #                  birthdate= '05/26/1990', bio='Snell rhymes with hell', gender='Male',
        #                  vhours=0, education="Some college, no degree")  

        
     #   print(vol.passwordhash)
       
                        
    


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






