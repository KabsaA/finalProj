from unittest import TestCase, main as unittest_main, mock
from flask import Flask
from app import app
from bson.objectid import ObjectId

test_id = ObjectId('5df556455d9d5e71a23e3e61')
test_post = {
    'name': 'Testname',
    'date': "Test post",

}
sample_form_data = {
    'name': test_post['name'],
    'date': test_post['date'],
}

class PostTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    '''Testing page'''
    def test_about(self):
        result = self.client.get('/about')
        self.assertEqual(result.status, '200 OK')

    '''Testing new post'''
    def test_new(self):
        result = self.client.get('/create_post')
        self.assertEqual(result.status, '200 OK')

if __name__ == '__main__':
    unittest_main()
