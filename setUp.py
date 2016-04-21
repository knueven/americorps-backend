from event import Event
from db import Session
from organization import Organization
from datetime import *
from sqlalchemy import exc
import string
from volunteer import Volunteer
from admin import Admin
from volunteerInterests import VolunteerInterests
from volunteerSkills import VolunteerSkills
from volunteerAvailability import VolunteerAvailability
from volunteerNeighborhoods import VolunteerNeighborhoods
import unittest

class SetUp(unittest.TestCase):

    def test_01_org_setup(cls):
        org0 = Organization('Cancer Research Center', 'crc@gmail.com', 'password101', '3198023836', '350 Mass Ave',
                           'Boston', 'MA', '02115', 'Looking for a Cure!', 'jane@gmail.com',
                            pics="http://www.imbcr.org/wp-content/uploads/2013/09/slider-5.jpg,http://www.worldwidecancerresearch.org/media/1131/Streaking-Bacteria2109.jpg,https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQEsnGcKjN0soZy1XqtG5MPluFD-MZ2nHtmE8nAh6LlLDXzQZt6lA,http://smhs.gwu.edu/sites/default/files/styles/875-x-variable/public/field/image/Research_website_460x220.png?itok=0rdPVS_m")

        org1 = Organization('Homeless Shelter', 'hs@hotmail.com', 'p@ssword', '3456789870', '174 Hillside St',
                            'Boston', 'MA', '02120', 'Help feed the homeless!', 'joey@gmail.com',
                            pics="http://cdn.citylab.com/media/img/citylab/2012/01/16/homelesssheltermain/lead_large.jpg,http://www.panhandlepost.com/wp-content/uploads/2013/02/Homeless-Shelter.jpg,https://upload.wikimedia.org/wikipedia/commons/a/a2/Meals_on_Wheels_food_prep.jpg,http://www.cvrm.org/wp-content/uploads/2011/06/givefoodsupplies_web.jpg")

        org2 = Organization('Dog Watchers', 'dw@gmail.com', 'puppies', '0987654321', '720 Columbus Ave',
                            'Boston', 'MA', '02120', 'Walk puppies!', 'shivi@icloud.com',
                            pics="http://f.tqn.com/y/dogs/1/W/3/K/0/-/pet-sitter-124465293-resized.jpg,http://cdn.bleacherreport.net/images_root/slides/photos/001/278/794/diaz5_display_image.jpg?1315512623,http://celebritydogwatcher.com/wp-content/uploads/2008/02/cesarmillan.jpg,http://cdn01.cdn.justjaredjr.com/wp-content/uploads/pictures/2011/04/shake-dog/davis-cleveland-dog-tv-watcher-10.jpg")
        
        s = Session()
        s.add(org0)
        s.add(org1)
        s.add(org2)
        
        try:
            s.commit()
        except exc.SQLAlchemyError:
            s.rollback()
        s.close()
    
    def test_02_event_setup(cls):
        s = Session()
        org = s.query(Organization).filter_by(name='Homeless Shelter').first()
        race1 = Event('Feed the Homeless', '20 Mass Ave', 'Boston', 'MA', '02115',
                     'Come hand out bread and soup',
                     datetime(2016, 2, 4, 16, 0, 0), datetime(2016, 2, 4, 14, 0, 0), org.id, org_name=org.name,
                      capacity=2, featured=True)
        org = s.query(Organization).filter_by(name='Dog Watchers').first()
        race3 = Event('Walk dogs', '170 Boylston St.', 'Boston', 'MA', '02115',
                     "Come walk people's dogs",
                     datetime(2015, 12, 12, 10, 0, 0), datetime(2015, 12, 12, 14, 0, 0), org.id, org_name=org.name,
                      capacity=25, featured=True)

        s.add(race1)
        s.add(race3)
        try:
            s.commit()
        except exc.SQLAlchemuError:
            s.rollback()
        s.close()

    def test_03_vol_setup(self):
        joey = Volunteer('Joseph Wood', 'wood.jos@husky.neu.edu', 'lit', '3015559721', True,
                         birthdate=date(1990, 5, 26), bio='CS Major', gender='Male',
                         uhours=0, vhours=0, education="somecoll",
                         pic='http://www.wired.com/wp-content/uploads/2014/09/parks-recreation-binge-ft.jpg')
        olivia = Volunteer('Olivia', 'olivia@husky.neu.edu', 'sratlyfe', '4029834098', True,
                           birthdate=date(1720, 10, 30), bio='Vote for Pedro', gender='Female',
                           uhours=0, vhours=0, education='lesshigh',
                           pic='https://upload.wikimedia.org/wikipedia/en/a/a3/Parks_recreation_canvassing.jpg')
        andrew= Volunteer('Andrew', 'andrew@husky.neu.edu', 'sqlalchemy', '9852039385', True,
                          birthdate=date(1993, 12, 22), bio='Yahoo4ever', gender='Male',
                          uhours=0, vhours=0, education='doctoral',
                          pic='http://cdn.fansided.com/wp-content/blogs.dir/340/files/2014/12/ben-wyatt-parks-and-rec.png')
        s = Session()
        try:
            s.add(joey)
            s.add(olivia)
            s.add(andrew)
            s.commit()
            s.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_04_vol_ints(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joseph Wood').first()
        olivia = session.query(Volunteer).filter_by(name='Olivia').first()
        andrew = session.query(Volunteer).filter_by(name='Andrew').first()
        doey = VolunteerInterests("animals", joey.id)
        livia = VolunteerInterests("health", olivia.id)
        drew = VolunteerInterests("education", andrew.id)
        try:
            session.add(doey)
            session.add(livia)
            session.add(drew)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_05_vol_skills(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joseph Wood').first()
        olivia = session.query(Volunteer).filter_by(name='Olivia').first()
        andrew = session.query(Volunteer).filter_by(name='Andrew').first()
        doey = VolunteerSkills("arts", joey.id)
        livia = VolunteerSkills("legal", olivia.id)
        drew = VolunteerSkills("writing", andrew.id)
        try:
            session.add(doey)
            session.add(livia)
            session.add(drew)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_06_vol_neighs(self):
        session = Session()
        olivia = session.query(Volunteer).filter_by(name='Olivia').first()
        andrew = session.query(Volunteer).filter_by(name='andrew').first()
        dolivia = VolunteerNeighborhoods("allston", olivia.id)
        solivia = VolunteerNeighborhoods("brighton", olivia.id)
        andrew = VolunteerNeighborhoods("westend", andrew.id)
        try:
            session.add(dolivia)
            session.add(solivia)
            session.add(andrew)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_07_vol_avail(self):
        session = Session()
        joey = session.query(Volunteer).filter_by(name='Joseph Wood').first()
        olivia = session.query(Volunteer).filter_by(name='Olivia').first()
        andrew = session.query(Volunteer).filter_by(name='Andrew').first()
        if joey:
            livia = VolunteerAvailability("Tuesday", olivia.id)
            drew = VolunteerAvailability("Saturday", andrew.id)
            mew = VolunteerAvailability("Sunday", andrew.id)
            try:
                session.add(livia)
                session.add(drew)
                session.add(mew)
                session.commit()
                session.close()
                self.assertTrue(True)
            except exc.SQLAlchemyError:
                self.assertTrue(False)
        else:
            self.assertTrue(False)

    def test_08_admin_setup(self):
        s = Session()
        shivi = Admin('Shivi', 'shivi@husky.neu.edu', 'ra', '4923840941', False,
                      birthdate=date(1990, 7, 4), bio='Team mom', gender='Female')
        michael = Admin('Michael', 'michael@husky.neu.edu', 'uml', '4928103491', False,
                        birthdate=date(1993, 4, 9), bio='Soft Dev Prof', gender='Male')
        kt = Admin('Katie', 'katie@husky.neu.edu', 'kt', '9898279812', False,
                   birthdate=date(1995, 3, 21), bio='Winning', gender='Female')

        s.add(shivi)
        s.add(michael)
        s.add(kt)
        try:
            s.commit()
        except exc.SQLAlchemuError:
            s.rollback()
        s.close()
        
