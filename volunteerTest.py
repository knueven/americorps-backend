from volunteer import Volunteer
from db import Session
from user import User
import unittest
from datetime import *
from sqlalchemy import exc
from volunteerNeighborhoods import VolunteerNeighborhoods
from volunteerInterests import VolunteerInterests
from volunteerSkills import VolunteerSkills
from volunteerAvailability import VolunteerAvailability
from attendee import Attendee
import volunteerTest
import string
import random
# volunteer contains: name, email, passwordhash, phone, last_active,
#			birthdate, permissions, bio, gender,
#			uhours, vhours, education

class VolunteerTests(unittest.TestCase):

    #checks if the volunteer's fields are initialized correctly
    def test_init(self):
        N=10
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        joey = Volunteer('Joey Wood', email, 'lit', '3015559721',
                         birthdate=date(1990, 5, 26), bio='Snell rhymes with hell', gender='Male',
                         uhours=0, vhours=0, education="Some college, no degree")
        self.assertTrue(joey.name == 'Joey Wood')
        self.assertTrue(joey.email == email)
        self.assertTrue(joey.passwordhash != 'lit')
        self.assertTrue(joey.phone == '3015559721')
        #self.assertTrue(joey.birthdate == '05/26/1990')
        self.assertTrue(joey.permissions == 'volunteer')
        self.assertTrue(joey.bio == 'Snell rhymes with hell')
        self.assertTrue(joey.gender == 'Male')
        self.assertTrue(joey.uhours == 0)
        self.assertTrue(joey.vhours == 0)
        self.assertTrue(joey.education == "Some college, no degree")



    #test object write to the database.    
    def test_db_write(self):
        N=20
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        joey = Volunteer('Joey Wood', email, 'lit', '3015559721',
                         birthdate=date(1990, 5, 26), bio='Snell rhymes with hell', gender='Male',
                         uhours=0, vhours=0, education="Some college, no degree")
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
                         birthdate=date(1990, 5, 26), bio='Snell rhymes with hell', gender='Male',
                         uhours=0, vhours=0, education="Some college, no degree")        
        poey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        self.assertTrue(joey.name == poey.name)
        self.assertTrue(joey.email == poey.email)
        self.assertTrue(joey.passwordhash != poey.passwordhash)
        self.assertTrue(joey.phone == poey.phone)
        self.assertTrue(joey.birthdate == poey.birthdate)
        self.assertTrue(joey.permissions == poey.permissions)
        self.assertTrue(joey.bio == poey.bio)
        self.assertTrue(joey.gender == poey.gender)
        self.assertTrue(joey.uhours == poey.uhours)
        self.assertTrue(joey.vhours == poey.vhours)
        self.assertTrue(joey.education == poey.education)

#<<<<<<< HEAD
#=======


#>>>>>>> develop
                        

    # checks if the volunteer can be queried by email
    def test_queryEmail(self):

        session = Session()
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721',
                         birthdate=date(1990, 5, 26), bio='Snell rhymes with hell', gender='Male',
                         uhours=0, vhours=0, education="Some college, no degree")
        poey = session.query(Volunteer).filter_by(email='wood.jos@husky.neu.edu').first()
        self.assertTrue(joey.name == poey.name)
        self.assertTrue(joey.email == poey.email)
        self.assertTrue(joey.passwordhash != poey.passwordhash)
        self.assertTrue(joey.phone == poey.phone)
        self.assertTrue(joey.birthdate == poey.birthdate)
        self.assertTrue(joey.permissions == poey.permissions)
        self.assertTrue(joey.bio == poey.bio)
        self.assertTrue(joey.gender == poey.gender)
        self.assertTrue(joey.uhours == poey.uhours)
        self.assertTrue(joey.vhours == poey.vhours)
        self.assertTrue(joey.education == poey.education)

                        

    # checks if the volunteer can be queried by phone
    def test_queryPhone(self):
        session = Session()
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721',
                         birthdate=date(1990, 5, 26), bio='Snell rhymes with hell', gender='Male',
                         uhours=0, vhours=0, education="Some college, no degree")         
        poey = session.query(Volunteer).filter_by(phone='3015559721').first()
        self.assertTrue(joey.name == poey.name)
        self.assertTrue(joey.email == poey.email)
        self.assertTrue(joey.phone == poey.phone)
        self.assertTrue(joey.birthdate == poey.birthdate)
        self.assertTrue(joey.permissions == poey.permissions)
        self.assertTrue(joey.bio == poey.bio)
        self.assertTrue(joey.gender == poey.gender)
        self.assertTrue(joey.uhours == poey.uhours)
        self.assertTrue(joey.vhours == poey.vhours)
        self.assertTrue(joey.education == poey.education)

    #unit test for password hashing
    def test_password_hash(self):
        N = 15
        session = Session()
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        vol = Volunteer('Test', email, 'lit', '3015559725',
                         birthdate=date(1990, 5, 26), bio='Snell rhymes with hell', gender='Male',
                         uhours=0, vhours=0, education="Some college, no degree")  
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
        joey = session.query(VolunteerInterests).filter_by(volunteer_id=doey.id).first()
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
        joey = session.query(VolunteerNeighborhoods).filter_by(volunteer_id=doey.id).first()
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
        joey = session.query(VolunteerSkills).filter_by(volunteer_id=doey.id).first()
        self.assertTrue(moey.skill == joey.skill)

    def test_availability_write(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        if joey:
            moey = VolunteerAvailability("Monday", joey.id)
            self.assertTrue(moey.day == "Monday")
            try:
                session.add(moey)
                session.commit()
                session.close()
                self.assertTrue(True)
            except exc.SQLAlchemyError:
                self.assertTrue(False)
        else:
            self.assertTrue(False)

    def test_availability(self):
        session = Session()
        doey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerAvailability("Monday", doey.id)
        joey = session.query(VolunteerAvailability).filter_by(volunteer_id=doey.id).first()
        self.assertTrue(moey.day == joey.day)

    def test_sign_up(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        joey.addEvent(1)
        event = session.query(Attendee).filter_by(userID=joey.id).first()
        self.assertTrue(event.userID == joey.id)
        session.close()
       

        




if __name__ == '__main__':
    unittest.main()






