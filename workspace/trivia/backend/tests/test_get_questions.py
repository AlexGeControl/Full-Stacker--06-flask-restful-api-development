import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.models import Category, CategoryFactory, Question, QuestionFactory


class GetQuestionsTestCase(unittest.TestCase):
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
        GetQuestionsTestCase.generate_data(20)

    @staticmethod
    def generate_data(num):
        # generate test data:
        for id in range(num):
            # generate:
            category = CategoryFactory()
            question = QuestionFactory()
            # insert:
            db.session.add_all(
                [category, question]
            )
            db.session.commit()

    def tearDown(self):
        # flush transaction:
        db.session.remove()
        # remove all tables:
        db.drop_all()
        # deactivate app context:
        self.app_context.pop()

    def test_get_questions_with_no_query_param(self):
        """ response should be generated using default page 1
        """
        # send request:
        response = self.client.get(
            url_for('api.get_questions'), 
            content_type='application/json'
        )        
        
        self.assertEqual(response.status_code, 200)
        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check response:
        self.assertEqual(json_response["total_questions"], 20)
        # check pagination:
        questions = sorted(json_response["questions"], key = lambda x: x["id"])
        self.assertEqual(questions[-1]["id"] - questions[0]["id"], 9)
        # check categories:
        categories = json_response["categories"]
        category_ids = [
            int(x) for x in categories.keys()
        ]
        self.assertEqual(max(category_ids) - min(category_ids), 19)

    def test_get_questions_with_query_param_page(self):
        """ response should be generated using given page 2
        """
        # send request:
        response = self.client.get(
            url_for('api.get_questions', page = 2), 
            content_type='application/json'
        )        
        
        self.assertEqual(response.status_code, 200)
        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check response:
        self.assertEqual(json_response["total_questions"], 20)
        # check pagination:
        questions = sorted(json_response["questions"], key = lambda x: x["id"])
        self.assertEqual(questions[-1]["id"] - questions[0]["id"], 9)
        # check categories:
        categories = json_response["categories"]
        category_ids = [
            int(x) for x in categories.keys()
        ]
        self.assertEqual(max(category_ids) - min(category_ids), 19)
