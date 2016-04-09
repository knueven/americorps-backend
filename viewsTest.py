import unittest
import tempfile
from db import Base, Session
import app

class ViewsTest(unittest.TestCase):

	def setUp(self):
		self.app = app.app.test_client()


	def testIndex(self):
		rv = self.app.get('/')
		assert b'not found' in rv.data

	def testUserCreate(self):
		rv = self.app.post('/user', data=dict(name='<hi>'))
		assert b'Error in' in rv.error


	#def tearDown(self):
		#tear it down


if __name__ == '__main__':
	unittest.main()
