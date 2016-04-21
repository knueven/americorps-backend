from volunteer import *
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
from event import Event
from enums import *
# volunteer contains: name, email, passwordhash, phone, last_active,
#			birthdate, permissions, bio, gender,
#			uhours, vhours, education

class VolunteerTests(unittest.TestCase):

    #checks if the volunteer's fields are initialized correctly
    def test_01_init(self):
        N=10
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        joey = Volunteer('Joey Wood', email, 'lit', '3015559721', True,
                         birthdate=date(1990, 5, 26), bio='CS Major', gender='Male',
                         uhours=0, vhours=0, education="somecoll",
                         pic="https://www.google.com/imgres?imgurl=http%3A%2F%2Fwww.peopleplace.eu%2Fimage%2Fnew%2Fslide1.jpg&imgrefurl=http%3A%2F%2Fwww.peopleplace.eu%2F&docid=lyjdXkOPdJV8bM&tbnid=u7uxEKYTPiGTmM%3A&w=2000&h=1333&bih=673&biw=1020&ved=0ahUKEwiJ3vq2yJzMAhUMdD4KHTtfDV0QMwhvKAYwBg&iact=mrc&uact=8")
        self.assertTrue(joey.name == 'Joey Wood')
        self.assertTrue(joey.email == email)
        self.assertTrue(joey.passwordhash != 'lit')
        self.assertTrue(joey.phone == '3015559721')
        self.assertTrue(joey.contact)
        #self.assertTrue(joey.birthdate == '05/26/1990')
        self.assertTrue(joey.permissions == 'volunteer')
        self.assertTrue(joey.bio == 'CS Major')
        self.assertTrue(joey.gender == 'Male')
        self.assertTrue(joey.uhours == 0)
        self.assertTrue(joey.vhours == 0)
        self.assertTrue(joey.education == "somecoll")
        self.assertTrue(joey.pic == 'https://www.google.com/imgres?imgurl=http%3A%2F%2Fwww.peopleplace.eu%2Fimage%2Fnew%2Fslide1.jpg&imgrefurl=http%3A%2F%2Fwww.peopleplace.eu%2F&docid=lyjdXkOPdJV8bM&tbnid=u7uxEKYTPiGTmM%3A&w=2000&h=1333&bih=673&biw=1020&ved=0ahUKEwiJ3vq2yJzMAhUMdD4KHTtfDV0QMwhvKAYwBg&iact=mrc&uact=8')



    #test object write to the database.    
    def test_02_db_write(self):
        N=20
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        joey = Volunteer('Joey Wood', email, 'lit', '3015259721', True,
                         birthdate=date(1990, 5, 26), bio='CS Major', gender='Male',
                         uhours=0, vhours=0, education="somecoll",
                         pic='http://www.wired.com/wp-content/uploads/2014/09/parks-recreation-binge-ft.jpg')
        s = Session()
        try:
            s.add(joey)
            s.commit()
            s.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

# checks if the volunteer was added to the database after initialization
    def test_03_queryName(self):
        session = Session()
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015259721', True,
                         birthdate=date(1990, 5, 26), bio='CS Major', gender='Male',
                         uhours=0, vhours=0, education="somecoll")        
        poey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        self.assertTrue(joey.name == poey.name)
        #self.assertTrue(joey.email == poey.email)
        self.assertTrue(joey.passwordhash != poey.passwordhash)
        self.assertTrue(joey.phone == poey.phone)
        self.assertTrue(joey.contact and poey.contact)
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
#    def test_04_queryEmail(self):
#
#        session = Session()
#        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721',
#                         birthdate=date(1990, 5, 26), bio='Snell rhymes with hell', gender='Male',
#                         uhours=0, vhours=0, education="Some college, no degree")
#        poey = session.query(Volunteer).filter_by(email='wood.jos@husky.neu.edu').first()
#        self.assertTrue(joey.name == poey.name)
#        self.assertTrue(joey.email == poey.email)
#        self.assertTrue(joey.passwordhash != poey.passwordhash)
#        self.assertTrue(joey.phone == poey.phone)
#        self.assertTrue(joey.birthdate == poey.birthdate)
#        self.assertTrue(joey.permissions == poey.permissions)
#        self.assertTrue(joey.bio == poey.bio)
#        self.assertTrue(joey.gender == poey.gender)
#        self.assertTrue(joey.uhours == poey.uhours)
#        self.assertTrue(joey.vhours == poey.vhours)
#        self.assertTrue(joey.education == poey.education)

                        

    # checks if the volunteer can be queried by phone
    def test_05_queryPhone(self):
        session = Session()
        joey = Volunteer('Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '3015259721', True,
                         birthdate=date(1990, 5, 26), bio='CS Major', gender='Male',
                         uhours=0, vhours=0, education="somecoll")         
        poey = session.query(Volunteer).filter_by(phone='3015259721').first()
        self.assertTrue(joey.name == poey.name)
        #self.assertTrue(joey.email == poey.email)
        self.assertTrue(joey.phone == poey.phone)
        self.assertTrue(joey.birthdate == poey.birthdate)
        self.assertTrue(joey.permissions == poey.permissions)
        self.assertTrue(joey.bio == poey.bio)
        self.assertTrue(joey.gender == poey.gender)
        self.assertTrue(joey.uhours == poey.uhours)
        self.assertTrue(joey.vhours == poey.vhours)
        self.assertTrue(joey.education == poey.education)

    #unit test for password hashing
    def test_06_password_hash(self):
        N = 15
        session = Session()
        email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)) + '@gmail.com'
        vol = Volunteer('Test', email, 'lit', '3015259725', True,
                         birthdate=date(1990, 5, 26), bio='CS Major', gender='Male',
                         uhours=0, vhours=0, education="somecoll")  
        try:
            session.add(vol)
            session.commit()
            poey = session.query(Volunteer).filter_by(phone='3015259725').first()
            self.assertTrue(vol.passwordhash != 'lit')
            self.assertTrue(poey.passwordhash != 'lit')
            self.assertTrue(vol.check_password('lit'))
            self.assertFalse(vol.check_password('lit2'))
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)


    def test_07_interests_write(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerInterests("youth", joey.id)
        self.assertTrue(moey.interest == "youth")
        try:
            session.add(moey)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_08_interests(self):
        session = Session()
        doey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerInterests("youth", doey.id)
        joey = session.query(VolunteerInterests).filter_by(volunteer_id=doey.id).first()
        #self.assertTrue(moey.interest == joey.interest)
        session.close()

    def test_09_neighborhood_write(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerNeighborhoods("backbay", joey.id)
        self.assertTrue(moey.neighborhood == "backbay")
        try:
            session.add(moey)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_10_neighborhoods(self):
        session = Session()
        doey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerNeighborhoods("backbay", doey.id)
        joey = session.query(VolunteerNeighborhoods).filter_by(volunteer_id=doey.id).first()
        #self.assertTrue(moey.neighborhood == joey.neighborhood)
        session.close()


    def test_11_skill_write(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerSkills(SkillsEnum.teaching, joey.id)
        self.assertTrue(moey.skill == "teaching")
        try:
            session.add(moey)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_12_skills(self):
        session = Session()
        doey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerSkills("teaching", doey.id)
        joey = session.query(VolunteerSkills).filter_by(volunteer_id=doey.id).first()
        #self.assertTrue(moey.skill == joey.skill)
        session.close()

    def test_13_availability_write(self):
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

    def test_14_availability(self):
        session = Session()
        doey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        moey = VolunteerAvailability("Monday", doey.id)
        joey = session.query(VolunteerAvailability).filter_by(volunteer_id=doey.id).first()
        #self.assertTrue(moey.day == joey.day)
        session.close()

    def test_15_sign_up(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        event = session.query(Event).filter_by(state='MA').first()
        addEvent(event.id, joey.id)
        attendee = session.query(Attendee).filter_by(userID=joey.id).first()
        print(attendee.userID)
        print(joey.id)
        self.assertTrue(attendee.userID == joey.id)
        session.close()

    def test_16_hour_logging(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joey Wood').first()
        event = session.query(Event).filter_by(state='MA').first()
        if joey and event:
            try:
                joey.log_hours(event.id, 4)
            except exc.SQLAlchemyError:
                self.assertTrue(False)
        else:
            return false
        attendee = session.query(Attendee).filter_by(eventID=event.id, userID=joey.id).first()
        self.assertTrue(attendee.hours == 4)
        session.close()

    def test_17_updating_name(self):
        session = Session()
        joey = session.query(User).filter_by(name='Joey Wood').first()
        q = session.query(User).filter_by(id=joey.id)
        q = q.update({"name":"Wood Joey"})
        joey = session.query(User).filter_by(id=joey.id).first()
        self.assertTrue(joey.name == 'Wood Joey')
        session.close()

    def test_18_updating_email(self):
        session = Session()
        joey = session.query(User).filter_by(name='Joey Wood').first()
        q = session.query(User).filter_by(id=joey.id)
        q = q.update({"email":"wood5@husky.neu.edu"})
        joey = session.query(User).filter_by(id=joey.id).first()
        self.assertTrue(joey.email == 'wood5@husky.neu.edu')
        session.close()

    def test_19_create_volunteer(self):
        json = {'name': 'Joey Wood', 'email': 'wood.jos@husky.neu.edu', 'passwordhash': 'lit',
                'phone': '3015559721', 'contact': true, 'birthdate':'03/27/2016', 'bio': 'Snell rhymes with hell',
                'gender': 'Male', 'uhours': 0, 'vhours': 0, 'education': "somecoll"}
        try:
            createVolunteer(json)
        except exc.SQLAlchemyError:
            self.assertTrue(False)
        



    def test_21_phone_long(self):
        self.assertRaises(ValueError, Volunteer, 'Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '30155597211', True,
                         birthdate=date(1990, 5, 26), bio='Snell rhymes with hell', gender='Male',
                         uhours=0, vhours=0, education="somecoll")

    def test_22_phone_short(self):
        self.assertRaises(ValueError, Volunteer, 'Joey Wood', 'wood.jos@husky.neu.edu', 'lit', '301555972', True,
                         birthdate=date(1990, 5, 26), bio='Snell rhymes with hell', gender='Male',
                         uhours=0, vhours=0, education="somecoll")

    def test_23_phone_letters(self):
        self.assertRaises(ValueError, Volunteer, 'Joey Wood', 'wood.jos@husky.neu.edu', 'lit', 'abcdefghij', True,
                         birthdate=date(1990, 5, 26), bio='Snell rhymes with hell', gender='Male',
                         uhours=0, vhours=0, education="somecoll")
        
        
        
       


if __name__ == '__main__':
    unittest.main()






