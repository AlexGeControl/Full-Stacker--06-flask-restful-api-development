import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db

class BlueprintMainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        # activate app context:
        self.app_context = self.app.app_context()
        self.app_context.push()
        # create tables:
        db.create_all()
        # create client:
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        # flush transaction:
        db.session.remove()
        # remove all tables:
        db.drop_all()
        # deactivate app context:
        self.app_context.pop()

    def test_get_root(self):
        """ response code of GET / should be 200
        """
        response = self.client.get(
            url_for('main.index'), 
            content_type='application/json'
        )        
        
        self.assertEqual(response.status_code, 200)

    def test_get_root_response_body(self):
        """ response body of GET / should be the greeting in JSON
        """
        response = self.client.get(
            url_for('main.index'), 
            content_type='application/json'
        )        
        
        self.assertEqual(response.status_code, 200)
        # parse response body as JSON:
        json_response = json.loads(response.get_data(as_text=True))

        self.assertEqual(json_response['message'], 'Hello, RESTful API development!')
