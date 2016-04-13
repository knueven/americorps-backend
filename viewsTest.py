import unittest
import tempfile
from db import Base, Session
from app import app
import string
import random
import json
from views import *

class ViewsTest(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()


	def testIndex(self):
		rv = self.app.get('/')
		assert b'disregard' in rv.data

	def testUserCreateError(self):
		rv = self.app.post('/user/', 
			data=json.dumps(dict(name='<hi>')), 
			content_type='application/json')
		assert b'500' in rv.data

	#leaving out until org is rewritten
	# def testOrgCreateSuccess(self):
	# 	rv = self.app.post('/organization/', data=json.dumps({"name": "Organization Test", 
	# 		"address": "10 Leon Street", "city": "Boston", "state": "MA", 
	# 		"zip": "02115", "mission": "Testing stuff"}), content_type='application/json') 
	# 	assert b"organization created, yay!" in rv.data

	def testVolunteerCreateSuccess(self):
		email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10)) + '@gmail.com'
		rv = self.app.post('/user/', data=json.dumps(
			{"name":"Volunteer Example","email":email,"passwordhash":"2930hmX","phone":"4017753433","permissions":"volunteer", "bio": "I like to volunteer",
    "gender": "Female",
    "birthdate":"1990-6-06",
    "education": "Less than High School",
    "neighborhoods": ["Charlestown", "East Boston"],
    "skills": ["Legal", "Handiwork"],
    "interests": ["Youth", "Education"],
    "availability": ["Monday", "Tuesday"]}),
			content_type='application/json')
		#print(rv.data)
		assert b'account created' in rv.data

	def testAdminCreateSuccess(self):
		email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10)) + '@gmail.com'
		rv = self.app.post('/user/', data=json.dumps({"name":"John Doe","email":email, "passwordhash":"asdfhjas", "phone":"6176472232","permissions":"admin","master":False}), content_type='application/json') 
		#print(rv.data)
		assert b'account created' in rv.data

	def testEventCreateSuccess(self):
		rv = self.app.post('/event', data=json.dumps({"name": "Test Event","address": "1 Mass Ave","city": "Boston","state": "MA","zip": "02115", "about": "Volunteering Stuff", "start_at": "2016-02-04 13:00:00","end_at": "2016-02-04 15:00:00","org": 1,"skills": ["Legal", "Handiwork"],"interests": ["Youth", "Education"], "capacity": 50}), content_type='application/json')
		assert b'event created' in rv.data

	#todo
	#def testEventSignupSuccess(self):
	#def testLoginSuccess(self):
	#def testOrganization
	#def 



	#def tearDown(self):
		#tear it down


if __name__ == '__main__':
	unittest.main()
