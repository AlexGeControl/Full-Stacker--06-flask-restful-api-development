import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.models import Category, CategoryFactory, Question, QuestionFactory


class GetQuestionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        # activate app context:
        self.app_context = self.app.app_context()
        self.app_context.push()
        # create tables:
        db.create_all()
        # create client:
        self.client = self.app.test_client(use_cookies=True)

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

    def test_get_question_with_invalid_id(self):
        """ response should be success = False for getting non-existing question
        """
        # send request:
        response = self.client.get(
            url_for('api.get_question', id = 999), 
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 404)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check response:
        self.assertEqual(json_response["success"], False)
        self.assertEqual(json_response["error"], 404)
        self.assertEqual(json_response["message"], "404 Not Found: Question with id=999 not found")

    def test_get_question_with_valid_id(self):
        """ response should be question with given id
        """
        # create data:
        category = CategoryFactory()            
        db.session.add(category)
        db.session.commit()
        question = QuestionFactory()
        db.session.add(question)
        db.session.commit()

        # send request:
        response = self.client.get(
            url_for('api.get_question', id = question.id), 
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )

        # check response:
        self.assertEqual(json_response["id"], question.id)