from event import Event
import event
from db import Session
import unittest
from organization import Organization
from datetime import datetime
from sqlalchemy import exc


# event contains: id, name, address, city, state, zip, about, start_at, posted_at, duration, interests, skills, org
class EventTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        org = Organization('Cancer Research Center', '350 Mass Ave', 'Boston', 'MA', '02115', 'Looking for a Cure!')
        org.id = 1
        s = Session()
        s.add(org)
        try:
            s.commit()
        except exc.SQLAlchemyError:
            s.rollback()
        s.close()

    # checks if the events fields are initialized correctly
    def test_01_init(self):
        race = Event('Race for the Cure', 'Mass Ave', 'Boston', 'MA', '02115',
                     'Running a marathon to raise money for cancer research',
                     datetime(2016, 4, 2, 13, 0, 0), datetime(2016, 4, 2, 14, 0, 0), 1, 25)
        self.assertEqual(race.name, 'Race for the Cure')
        self.assertEqual(race.address, 'Mass Ave')
        self.assertEqual(race.city, 'Boston')
        self.assertEqual(race.state, 'MA')
        self.assertEqual(race.zip, '02115')
        self.assertEqual(race.about, 'Running a marathon to raise money for cancer research')
        self.assertEqual(str(race.start_at), '2016-04-02 13:00:00')
        self.assertEqual(str(race.end_at), '2016-04-02 14:00:00')
        self.assertEqual(race.org, 1)
        self.assertEqual(race.capacity, 25)

    # test object write to the database.
    def test_02_db_write(self):
        race = Event('Race for the Cure', 'Mass Ave', 'Boston', 'MA', '02115',
                     'Running a marathon to raise money for cancer research', datetime(2016, 4, 2, 13, 0, 0),
                     datetime(2016, 4, 2, 14, 0, 0), 1, 30)
        s = Session()

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

    def test_query(self):
        session = Session()
        race = Event('Race for the Cure', 'Mass Ave', 'Boston', 'MA', '02115',
                     'Running a marathon to raise money for cancer research',
                     datetime(2016, 4, 2, 13, 0, 0), datetime(2016, 4, 2, 14, 0, 0), 1, 20)
        qrace = session.query(Event).filter_by(name='Race for the Cure').first()
        self.assertTrue(race.name == qrace.name)
        self.assertTrue(race.address == qrace.address)
        self.assertTrue(race.city == qrace.city)
        self.assertTrue(race.state == qrace.state)
        self.assertTrue(race.zip == qrace.zip)
        self.assertTrue(race.about == qrace.about)
        self.assertTrue(race.start_at == qrace.start_at)
        self.assertTrue(race.end_at == qrace.end_at)

# # race.zip is a string of letters - should be 5 ints
# def test_zip_letters(self):
#     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', 'abcdef',
#                'Running a marathon to raise money for cancer research', '04/02/2016 13:00', '03/27/2016 24:00:00',
#                2, 'cancer', 'running', 'Race for the Cure')
#     self.assertRaises(ValueError, 'zip-codes must be a string of 5 integers')

# # race.zip is too long - should be 5 ints
# def test_zip_length(self):
#     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', '123456789',
#                'Running a marathon to raise money for cancer research', '04/02/2016 13:00', '03/27/2016 24:00:00',
#                2, 'cancer', 'running', 'Race for the Cure')
#     self.assertRaises(ValueError, 'zip-codes must be a string of 5 integers')

# # race.start_at is a string of letters - should be in the form mm/dd/yyyy, hh:mm
# def test_startAt_letters(self):
#     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', '02115',
#                'Running a marathon to raise money for cancer research', 'oops', '03/27/2016 24:00:00',
#                2, 'cancer', 'running', 'Race for the Cure')
#     self.assertRaises(ValueError, 'start time must be in the form mm/dd/yyyy hh:mm')

# # race.start_at is improperly formatted - should be in the form mm/dd/yyyy, hh:mm
# def test_startAt_format(self):
#     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', '02115',
#                'Running a marathon to raise money for cancer research', 'April 12, 2016 1pm', '03/27/2016 24:00:00',
#                2, 'cancer', 'running', 'Race for the Cure')
#     self.assertRaises(ValueError, 'start time must be in the form mm/dd/yyyy hh:mm')

# # race.start_at cannot be in the past
# def test_startAt_past(self):
#     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', '02115',
#                'Running a marathon to raise money for cancer research', 'April 12, 2014 1pm', '03/27/2016 24:00:00',
#                2, 'cancer', 'running', 'Race for the Cure')
#     self.assertRaises(ValueError, 'start time must be in the form mm/dd/yyyy hh:mm')

# # race.posted_at is a string of letters - should be in the form mm/dd/yyyy, hh:mm:ss
# def test_postedAt_letters(self):
#     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', '02115',
#                'Running a marathon to raise money for cancer research', '04/02/2016 13:00', 'oops',
#                2, 'cancer', 'running', 'Race for the Cure')
#     self.assertRaises(ValueError, 'post time must be in the form mm/dd/yyyy hh:mm:ss')

# # race.posted_at is improperly formatted - should be in the form mm/dd/yyyy, hh:mm:ss
# def test_postedAt_format(self):
#     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', '02115',
#                'Running a marathon to raise money for cancer research', '04/02/2016 13:00', 'March 27, 2016 12am',
#                2, 'cancer', 'running', 'Race for the Cure')
#     self.assertRaises(ValueError, 'post time must be in the form mm/dd/yyyy hh:mm:ss')

# These tests require the Interest and Skills Enumerations to be created

# # race.interests should exist in the interests table
# def test_interests_exists(self):
#     session = Session()
#     self.assertEqual(self.race.interests, session.query(Interests).filter_by(name=self.race.interests).first())
#     session.close()
#
# # race.skills should exist in the skills table
# def test_skills_exists(self):
#     session = Session()
#     self.assertEqual(self.race.skills, session.query(Skills).filter_by(name=self.race.skills).first())
#     session.close()

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
