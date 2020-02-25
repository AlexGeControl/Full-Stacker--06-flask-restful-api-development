import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.models import Category, CategoryFactory, Question, QuestionFactory


class GetQuestionsByCategoryTestCase(unittest.TestCase):
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

    def test_get_questions_with_invalid_category_id(self):
        """ response should be success = False for getting non-existing category
        """
        # send request:
        response = self.client.get(
            url_for('api.get_questions_by_category', id = 999), 
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
        self.assertEqual(json_response["message"], "404 Not Found: Category with id=999 not found")

    def test_get_questions_by_category(self):
        """ response should be questions which belongs to the given category
        """
        # create category one:
        category_one = CategoryFactory()            
        db.session.add(category_one)
        db.session.commit()
        # add questions:
        for _ in range(3):
            question = QuestionFactory()
            question.category_id = category_one.id
            db.session.add(question)
            db.session.commit()
        # create category another:
        category_another = CategoryFactory()            
        db.session.add(category_another)
        db.session.commit()
        for _ in range(4):
            question = QuestionFactory()
            question.category_id = category_another.id
            db.session.add(question)
            db.session.commit()

        # send request:
        response = self.client.get(
            url_for('api.get_questions_by_category', id = category_one.id), 
            content_type='application/json'
        )        
        
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check total question count:
        self.assertEqual(json_response["total_questions"], 3)
        # check current category:
        self.assertEqual(json_response["current_category"], category_one.id)

        # send request:
        response = self.client.get(
            url_for('api.get_questions_by_category', id = category_another.id), 
            content_type='application/json'
        )        
        
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check total question count:
        self.assertEqual(json_response["total_questions"], 4)
        # check current category:
        self.assertEqual(json_response["current_category"], category_another.id)
