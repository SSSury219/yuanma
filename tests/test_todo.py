import unittest
from app import app
class TodoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        print 'success'

    def test_index(self):
        rv = self.app.get('/')
        assert "this is a index page" in rv.data

    def test_analysis(self):
        rv = self.app.post('/analysis?=862286091759611905')
        assert 'id' in rv.data

