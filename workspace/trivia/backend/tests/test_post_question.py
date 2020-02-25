import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.models import Category, CategoryFactory, Question, QuestionFactory


class PostQuestionTestCase(unittest.TestCase):
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

    def test_post_new_question(self):
        """ response should be success = True for posting of new question
        """
        # create new category:
        category = CategoryFactory()
        db.session.add(category)
        db.session.commit()
        # create new question:
        question = QuestionFactory().to_json()
        question["category_id"] = category.id

        # send request:
        response = self.client.post(
            url_for('api.create_question'),
            content_type='application/json',
            data = json.dumps(
                {
                    "answer": question["answer"],
                    "question": question["question"],
                    "difficulty": question["difficulty"],
                    "category_id": question["category_id"]
                }
            )
        )      
        
        self.assertEqual(response.status_code, 201)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check response:
        self.assertEqual(json_response["success"], True)

    def test_post_existing_question(self):
        """ response should be success = False for posting of existing question
        """
        # create new category & question:
        category = CategoryFactory()
        db.session.add(category)
        db.session.commit()
        question = QuestionFactory()
        question.category_id = category.id
        db.session.add(question)
        db.session.commit()
        # create new question with existing id:
        another_question = QuestionFactory().to_json()
        another_question["id"] = question.id
        another_question["category_id"] = category.id

        # send request:
        response = self.client.post(
            url_for('api.create_question'),
            content_type='application/json',
            data = json.dumps(
                another_question
            )
        )      
        
        self.assertEqual(response.status_code, 500)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check response:
        self.assertEqual(json_response["success"], False)
        self.assertEqual(json_response["error"], 500)
        self.assertEqual(json_response["message"], "500 Internal Server Error: Failed to create new Question")
