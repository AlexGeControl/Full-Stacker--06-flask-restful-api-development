import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.models import Category, CategoryFactory, Question, QuestionFactory


class DeleteQuestionTestCase(unittest.TestCase):
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
        DeleteQuestionTestCase.generate_data(1)

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

    def test_delete_existing_question(self):
        """ response should be success = True for deletion of existing question
        """
        # send request:
        response = self.client.delete(
            url_for('api.delete_question', id = 0)
        )      
        
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check response:
        self.assertEqual(json_response["success"], True)

    def test_delete_existing_question(self):
        """ response should be success = False for deletion of non-existing question
        """
        # send request:
        response = self.client.delete(
            url_for('api.delete_question', id = 999)
        )      
        
        self.assertEqual(response.status_code, 500)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check response:
        self.assertEqual(json_response["success"], False)
        self.assertEqual(json_response["error"], 500)
        self.assertEqual(json_response["message"], "500 Internal Server Error: Failed to delete Question with id=999")
