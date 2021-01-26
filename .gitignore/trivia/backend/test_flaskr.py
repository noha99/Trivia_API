import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgresql://postgres:postgres@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_questions_size(self):
        response = self.client().get('/questions')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["questions"]),10)

    def test_wrong_method(self):
        response = self.client().get('/questions')

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(data['success'], True)

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['questions']),10)

    def test_delete_question(self):
        response = self.client().delete('/questions/1')
        data = json.loads(response.data)

        if response.status_code == 404:
            self.assertEqual(data['success'], False)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], True)

    def test_add_question(self):
        response = self.client().post('/questions', data=json.dumps({}),
                                 content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_question(self):
        response = self.client().post('/questions', json={'searchTerm': 'what is your name'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_question_by_category(self):
        response = self.client().post('categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_play_quiz(self):
        response = self.client().post('/quizzes',json={
                                                    'previous_questions': [1, 2],
                                                    'quiz_category': {
                                                        'type': 'Science', 
                                                        'id': '1'
                                                        }
                                                    })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 1)

        self.assertNotEqual(data['question']['id'], 1)
        self.assertNotEqual(data['question']['id'], 2)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()