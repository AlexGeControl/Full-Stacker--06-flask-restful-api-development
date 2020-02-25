import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.models import Category, CategoryFactory


class GetCategoriesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        # activate app context:
        self.app_context = self.app.app_context()
        self.app_context.push()
        # create tables:
        db.create_all()
        # create client:
        self.client = self.app.test_client(use_cookies=True)
        # generate data:
        GetCategoriesTestCase.generate_data(20)

    @staticmethod
    def generate_data(num):
        # generate test data:
        for id in range(num):
            # generate:
            category = CategoryFactory()
            # insert:
            db.session.add(category)
            db.session.commit()

    def tearDown(self):
        # flush transaction:
        db.session.remove()
        # remove all tables:
        db.drop_all()
        # deactivate app context:
        self.app_context.pop()

    def test_get_categories(self):
        """ response should be all available categories as dict with id as key and type as value
        """
        # send request:
        response = self.client.get(
            url_for('api.get_categories'), 
            content_type='application/json'
        )        
        
        self.assertEqual(response.status_code, 200)
        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        categories = json_response["categories"]
        # check total number of categories:
        self.assertEqual(len(categories), 20)
        # check category ids:
        category_ids = [
            int(x) for x in categories.keys()
        ]
        self.assertEqual(max(category_ids) - min(category_ids), 19)
