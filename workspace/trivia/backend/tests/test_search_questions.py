import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.models import Category, CategoryFactory, Question, QuestionFactory


class SearchQuestionsTestCase(unittest.TestCase):
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

    def test_search_questions(self):
        """ response should be questions with search term in question body
        """
        # create new category:
        category = CategoryFactory()
        db.session.add(category)
        db.session.commit()
        # create new questions:
        for _ in range(3):
            question = QuestionFactory()
            question.category_id = category.id
            question.question = 'KeyWordA'
            db.session.add(question)
            db.session.commit()
        for _ in range(4):
            question = QuestionFactory()
            question.category_id = category.id
            question.question = 'KeyWordB'
            db.session.add(question)
            db.session.commit()

        # send request:
        response = self.client.post(
            url_for('api.search_questions'),
            content_type='application/json',
            data = json.dumps(
                {
                    "searchTerm": "KeyWordA"
                }
            )
        )      
        
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check response:
        self.assertEqual(json_response["total_questions"], 3)
        # check current category:
        self.assertEqual(json_response["current_category"], None)

        # send request:
        response = self.client.post(
            url_for('api.search_questions'),
            content_type='application/json',
            data = json.dumps(
                {
                    "searchTerm": "KeyWordB"
                }
            )
        )      
        
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check response:
        self.assertEqual(json_response["total_questions"], 4)
        # check current category:
        self.assertEqual(json_response["current_category"], None)
