from event import Event
import event
from db import Session
import unittest
from organization import Organization
from datetime import datetime
from sqlalchemy import exc
import random
import string
from eventSkills import EventSkills
from eventInterests import EventInterests
from eventNeighborhoods import EventNeighborhoods


# event contains: id, name, address, city, state, zip, about, start_at, posted_at, duration, interests, skills, org
class EventTests(unittest.TestCase):



    # checks if the events fields are initialized correctly
    def test_01_init(self):
        s = Session()
        org = s.query(Organization).filter_by(name='Test Org').first()
        race = Event('Race for the Cure', '20 Newbury St.', 'Boston', 'MA', '02115',
                     'Running a marathon to raise money for cancer research',
                     datetime(2016, 4, 2, 13, 0, 0), datetime(2016, 4, 2, 14, 0, 0), org.id, org_name=org.name,
                     capacity=25, featured=False)
        
        self.assertEqual(race.name, 'Race for the Cure')
        self.assertEqual(race.address, '20 Newbury St.')
        self.assertEqual(race.city, 'Boston')
        self.assertEqual(race.state, 'MA')
        self.assertEqual(race.zip, '02115')
        self.assertEqual(race.about, 'Running a marathon to raise money for cancer research')
        self.assertEqual(str(race.start_at), '2016-04-02 13:00:00')
        self.assertEqual(str(race.end_at), '2016-04-02 14:00:00')
        self.assertEqual(race.org, org.id)
        self.assertEqual(race.org_name, org.name)
        self.assertEqual(race.capacity, 25)
        self.assertFalse(race.featured)
        s.close()

    # test object write to the database.
    def test_02_db_write(self):
        s = Session()
        org = s.query(Organization).filter_by(name='Test Org').first()
        race = Event('Race for the Cure', 'Mass Ave', 'Boston', 'MA', '02115',
                     'Running a marathon to raise money for cancer research', datetime(2016, 4, 2, 13, 0, 0),
                     datetime(2016, 4, 2, 14, 0, 0), org.id, org_name=org.name,
                     capacity=30, featured=False)

        s.add(race)
        s.commit()
        s.close()
        if s.query(Event).filter_by(name='Race for the Cure').first():
            self.assertTrue(True)
        else:
            self.assertTrue(False)  # checks if the event was added to the database after initialization

    #def test_db_delete(self):
#        s = Session()
#        try:
#            event1 = s.query(Event).filter_by(name='Race for the Cure').first()
#            s.delete(event1)
#            s.commit
#        except exc.SQLAlchemyError:
#            self.assertTrue(False)



    def test_03_create_event(self):
        json = {"name": "Event1","address": "1 something street", "city": "Boston", "state": "MA", "zip": "02115", "about": "ok", "start_at": "04/02/2016 13:00","posted_at": "03/27/2016 24:00:00","end_at": "04/02/2016 15:00", "org": 1, "capacity": 25}
        try: 
            event.createEvent(json)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_04_query(self):
        session = Session()
        race = Event('Race for the Cure', 'Mass Ave', 'Boston', 'MA', '02115',
                     'Running a marathon to raise money for cancer research',
                     datetime(2016, 4, 2, 13, 0, 0), datetime(2016, 4, 2, 14, 0, 0), 1, 20, False)
        qrace = session.query(Event).filter_by(name='Race for the Cure').first()
        self.assertTrue(race.name == qrace.name)
        self.assertTrue(race.address == qrace.address)
        self.assertTrue(race.city == qrace.city)
        self.assertTrue(race.state == qrace.state)
        self.assertTrue(race.zip == qrace.zip)
        self.assertTrue(race.about == qrace.about)
        self.assertTrue(race.start_at == qrace.start_at)
        self.assertTrue(race.end_at == qrace.end_at)
        self.assertTrue(qrace.org_name != None)
        self.assertFalse(race.featured)

    def test_05_updating_name(self):
        session = Session()
        race = session.query(Event).filter_by(name='Race for the Cure').first()
        q = session.query(Event).filter_by(id=race.id)
        q = q.update({"name":"Wood Joey"})
        race = session.query(Event).filter_by(id=race.id).first()
        self.assertTrue(race.name == 'Wood Joey')
        session.close()

    def test_06_updating_zip(self):
        session = Session()
        race = session.query(Event).filter_by(name='Race for the Cure').first()
        q = session.query(Event).filter_by(id=race.id)
        q = q.update({"zip":"02120"})
        race = session.query(Event).filter_by(id=race.id).first()
        self.assertTrue(race.zip == '02120')
        session.close()

    # # race.zip is a string of letters - should be 5 ints
    def test_07_zip_letters(self):
        
        self.assertRaises(ValueError, Event, 'Race for the Cure', 'Mass Ave', 'Boston', 'MA', 'abcde',
                     'Running a marathon to raise money for cancer research',
                     datetime(2016, 4, 2, 13, 0, 0), datetime(2016, 4, 2, 14, 0, 0), 1, capacity=20)

# # race.zip is too long - should be 5 ints
    def test_08_zip_length(self):
        self.assertRaises(ValueError, Event, 'Race for the Cure', 'Mass Ave', 'Boston', 'MA', '021155',
                     'Running a marathon to raise money for cancer research',
                     datetime(2016, 4, 2, 13, 0, 0), datetime(2016, 4, 2, 14, 0, 0), 1, capacity=20)


# # race.zip is too short - should be 5 ints
    def test_09_zip_length(self):
        self.assertRaises(ValueError, Event, 'Race for the Cure', 'Mass Ave', 'Boston', 'MA', '0211',
                     'Running a marathon to raise money for cancer research',
                     datetime(2016, 4, 2, 13, 0, 0), datetime(2016, 4, 2, 14, 0, 0), 1, capacity=20)


# # race.capacity cant be less than 0
    def test_10_zip_length(self):
        self.assertRaises(ValueError, Event, 'Race for the Cure', 'Mass Ave', 'Boston', 'MA', '02115',
                     'Running a marathon to raise money for cancer research',
                     datetime(2016, 4, 2, 13, 0, 0), datetime(2016, 4, 2, 14, 0, 0), 1, capacity=-1)

    def test_11_interests_write(self):
        session = Session()
        race = session.query(Event).filter_by(name='Race for the Cure').first()
        dace = EventInterests("Youth", race.id)
        self.assertTrue(dace.interest == "Youth")
        try:
            session.add(dace)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_12_interests(self):
        session = Session()
        race = session.query(Event).filter_by(name='Race for the Cure').first()
        dace = EventInterests("Youth", race.id)
        lace = session.query(EventInterests).filter_by(event_id=race.id).first()
        self.assertTrue(dace.interest == lace.interest)
        session.close()

    def test_13_neighborhood_write(self):
        session = Session()
        race = session.query(Event).filter_by(name='Race for the Cure').first()
        dace = EventNeighborhoods("Back Bay", race.id)
        self.assertTrue(dace.neighborhood == "Back Bay")
        try:
            session.add(dace)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_14_neighborhoods(self):
        session = Session()
        race = session.query(Event).filter_by(name='Race for the Cure').first()
        dace = EventNeighborhoods("Back Bay", race.id)
        lace = session.query(EventNeighborhoods).filter_by(event_id=race.id).first()
        self.assertTrue(dace.neighborhood == lace.neighborhood)
        session.close()


    def test_15_skill_write(self):
        session = Session()
        race = session.query(Event).filter_by(name='Race for the Cure').first()
        dace = EventSkills("Teaching/Tutoring", race.id)
        self.assertTrue(dace.skill == "Teaching/Tutoring")
        try:
            session.add(dace)
            session.commit()
            session.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)

    def test_16_skills(self):
        session = Session()
        race = session.query(Event).filter_by(name='Race for the Cure').first()
        dace = EventSkills("Teaching/Tutoring", race.id)
        lace = session.query(EventSkills).filter_by(event_id=race.id).first()
        self.assertTrue(dace.skill == lace.skill)
        session.close()

        


# not sure if we still need this
#    def test_org_exists(self):
 #       session = Session()
#        race = Event('Race for the Cure', 'Mass Ave', 'Boston', 'MA', '02115',
#                     'Running a marathon to raise money for cancer research',
#                     '04/02/2016 13:00', '03/27/2016 24:00:00','04/02/2016 15:00', 1, 35)
#        org = Organization('Cancer Research Center', '350 Mass Ave', 'Boston', 'MA', '02115', 'Looking for a Cure!')
#        query = session.query(Organization).filter_by(name=org.name).first()
#        if query:
#            self.assertTrue(org.name == query.name and
#                            org.address == query.address and
#                            org.city == query.city)
#        else:
#            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
