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
        self.database_path = "postgres://{}/{}".format('postgres:password@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # Tyler - 0 - From 4.3

    def test_homepage(self):
        """Test that the homepage loads """
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

    # Tyler - 2 - From 4.3

    def test_get_categories(self):
        """ Checks for valid GET request results from /categories """
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)

    # Tyler - 3 - From 4.3

    def test_get_questions(self):
        """ Checks for valid GET request results from /questions """
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['questions'][0]['answer'], 'Maya Angelou')
        self.assertEqual(len(data['categories']), 6)

    # Tyler - 4 - From 4.3
    def test_create_delete_questions(self):
        """ Checks to make sure that creating and deleting a
        question goes according to plan """

        new_question = 'What is the meaning of the universe?'
        new_answer = '12'
        new_category = 1 # Science
        new_difficulty = '5'

        new_question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        new_question.insert()

        new_question_id = new_question.id

        question_pull = Question.query.filter(Question.id == new_question_id).one_or_none()

        self.assertEqual(question_pull.answer, '12')

        res = self.client().delete(f'/api/questions/{new_question_id}')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], new_question_id)

    # Tyler - 5 - From 4.3

    def test_post_new_question(self):
        """ POST a question and check that it's in the database """

        self.new_question = {
            'question':'How much wood would a woodchuck chuck if a woodchuck could chuck wood?',
            'answer':'About 700 pounds',
            'category': 1,  # Science
            'difficulty': '4'
        }
        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)
        new_question_id = data['created']

        self.assertEqual(data['success'], True)

        question_pull = Question.query.filter(Question.id == new_question_id).one_or_none()

        self.assertEqual(question_pull.answer, 'About 700 pounds')

        # Delete question to revert back to original database

        res = self.client().delete(f'/api/questions/{new_question_id}')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], new_question_id)


    # Tyler - 6 - From 4.3

    def test_question_search(self):
        """ Find question based on search term """
        res = self.client().post('/api/questions', json={'searchTerm':'Giaconda'})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'][0]['id'], 17)

    
    # Tyler - 7 - From 4.3

    def test_get_questions_by_category(self):
        """ GET questions filtered by category """
        # Pull in the 4 Art category questions
        res = self.client().get('/api/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 2)
        self.assertEqual(data['total_questions'], 4)

    
    # Tyler - 8 - From 4.3

    def test_play_quiz_1(self):
        """ Test the opening of the quiz when Sports is selected.
        There are only two Sports questions, 10 and 11. """
        res = self.client().post('/api/quizzes', json={'previous_questions':[], 'quiz_category': {'type':'Sports', 'id':'6'}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], 6)


    def test_play_quiz_2(self):
        """ Test the second question of the quiz when Sports is selected """
        res = self.client().post('/api/quizzes', json={'previous_questions':[10], 'quiz_category': {'type':'Sports', 'id':'6'}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['id'], 11)


    def test_play_quiz_3(self):
        """ Test what happens once all questions are answered """
        res = self.client().post('/api/quizzes', json={'previous_questions':[10, 11], 'quiz_category': {'type':'Sports', 'id':'6'}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual('question' not in data, True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()