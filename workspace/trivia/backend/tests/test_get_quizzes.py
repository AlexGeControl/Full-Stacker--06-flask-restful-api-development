import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app, db
from application.models import Category, CategoryFactory, Question, QuestionFactory


class GetQuizzesByCategoryTestCase(unittest.TestCase):
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

    def test_get_quizzes_without_previous_questions(self):
        """ response should be success = False for POST invalid JSON
        """
        response = self.client.post(
            url_for('api.get_quizzes'),
            content_type='application/json',
            data = json.dumps(
                {}
            )
        )
        
        # check status code:
        self.assertEqual(response.status_code, 400)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        self.assertEqual(json_response["success"], False)
        self.assertEqual(json_response["error"], 400)
        self.assertEqual(json_response["message"], "400 Bad Request: 'previous_questions' not found")

    def test_get_quizzes_with_quiz_category(self):
        """ response should be contain new question from given category if there are still remaining ones, None otherwise
        """
        # create category one:
        category_one = CategoryFactory()            
        db.session.add(category_one)
        db.session.commit()
        # add questions:
        category_one_question_ids = []
        for _ in range(3):
            question = QuestionFactory()
            question.category_id = category_one.id
            db.session.add(question)
            db.session.commit()
            # save ids as quiz state:
            category_one_question_ids.append(question.id)
        # create category another:
        category_another = CategoryFactory()            
        db.session.add(category_another)
        db.session.commit()
        category_another_question_ids = []
        for _ in range(4):
            question = QuestionFactory()
            question.category_id = category_another.id
            db.session.add(question)
            db.session.commit()
            # save ids as quiz state:
            category_another_question_ids.append(question.id)

        # test category one:
        category_one_question_ids = set(category_one_question_ids)
        category_one_previous_question_ids = []
        for _ in range(len(category_one_question_ids)):
            # request one new question:
            response = self.client.post(
                url_for('api.get_quizzes'),
                content_type='application/json',
                data = json.dumps(
                    {
                        "previous_questions": category_one_previous_question_ids,
                        "quiz_category": {
                            "id": category_one.id,
                            "type": category_one.type
                        }
                    }
                )
            )      
            # check status code:
            self.assertEqual(response.status_code, 200)

            # parse json response:
            json_response = json.loads(
                response.get_data(as_text=True)
            )
            next_question = json_response["question"]

            # check total question count:
            self.assertTrue(next_question["id"] in category_one_question_ids)

            # update state:
            category_one_previous_question_ids.append(next_question["id"])
            category_one_question_ids.remove(next_question["id"])

        # request one new question :
        response = self.client.post(
            url_for('api.get_quizzes'),
            content_type='application/json',
            data = json.dumps(
                {
                    "previous_questions": category_one_previous_question_ids,
                    "quiz_category": {
                        "id": category_one.id,
                        "type": category_one.type
                    }
                }
            )
        )      
        # check status code:
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        next_question = json_response["question"]

        self.assertTrue(next_question is None)

    def test_get_quizzes_without_quiz_category(self):
        """ response should be contain new question from all categories if there are still remaining ones, None otherwise
        """
        # create category one:
        category_one = CategoryFactory()            
        db.session.add(category_one)
        db.session.commit()
        # add questions:
        question_ids = []
        for _ in range(3):
            question = QuestionFactory()
            question.category_id = category_one.id
            db.session.add(question)
            db.session.commit()
            # save ids as quiz state:
            question_ids.append(question.id)
        # create category another:
        category_another = CategoryFactory()            
        db.session.add(category_another)
        db.session.commit()
        for _ in range(4):
            question = QuestionFactory()
            question.category_id = category_another.id
            db.session.add(question)
            db.session.commit()
            # save ids as quiz state:
            question_ids.append(question.id)

        # test category one:
        question_ids = set(question_ids)
        previous_question_ids = []
        for _ in range(len(question_ids)):
            # request one new question:
            response = self.client.post(
                url_for('api.get_quizzes'),
                content_type='application/json',
                data = json.dumps(
                    {
                        "previous_questions": previous_question_ids
                    }
                )
            )      
            # check status code:
            self.assertEqual(response.status_code, 200)

            # parse json response:
            json_response = json.loads(
                response.get_data(as_text=True)
            )
            next_question = json_response["question"]

            # check total question count:
            self.assertTrue(next_question["id"] in question_ids)

            # update state:
            previous_question_ids.append(next_question["id"])
            question_ids.remove(next_question["id"])

        # request one new question :
        response = self.client.post(
            url_for('api.get_quizzes'),
            content_type='application/json',
            data = json.dumps(
                {
                    "previous_questions": previous_question_ids
                }
            )
        )      
        # check status code:
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        next_question = json_response["question"]

        self.assertTrue(next_question is None)