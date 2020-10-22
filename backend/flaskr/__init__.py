import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Define paginate external to create_app
def paginate(request, data_pull):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_data_pull = [data.format() for data in data_pull[start:end]]

    return formatted_data_pull


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    # Tyler - 0 - From 3.4
    cors = CORS(app, resources={r"/api/*":{"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    # Tyler - 1 - From 3.4

    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response


    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    # Tyler - 2 - From 3.5
    @app.route('/api/categories')
    def get_categories():
      try:
        categories = Category.query.all()
        formatted_categories = {category.id:category.type for category in categories}

        return jsonify({
          'success':True,
          'categories': formatted_categories
        })

      except:
        abort(500)

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    # Tyler - 3 - From 3.5

    @app.route('/api/questions')
    def get_questions():
      try:
        questions = Question.query.all()
        formatted_questions = paginate(request, questions)

        if len(formatted_questions) == 0:
          abort(404)

        categories = Category.query.all()
        formatted_categories = {category.id:category.type for category in categories}

        return jsonify({
          'success':True,
          'questions':formatted_questions,
          'total_questions':len(questions),
          'categories':formatted_categories,
          'current_category':None,
        })

      except:
        abort(500)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    # Tyler - 4 - From 3.6

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
      try:
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
          abort(404)

        question.delete()
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate(request, questions)

        return jsonify({
          'success': True,
          'deleted': question_id,
          'questions': current_questions,
          'total_questions': len(questions)
        })
      
      except:
        abort(422)

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    # Tyler - 5 - From 3.6

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    # Tyler - 6

    @app.route('/api/questions', methods=['POST'])
    def create_question():
      body = request.get_json()

      if 'searchTerm' in body:
        search_term = body['searchTerm'].strip()

        questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
          'success': True,
          'questions': formatted_questions
        })

      else:
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
          question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
          question.insert()

          questions = Question.query.order_by(Question.id).all()
          current_questions = paginate(request, questions)

          return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_questions,
            'total_questions': len(questions)
          })

        except:
          abort(422)

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    # Tyler - 7 - From 3.5

    @app.route('/api/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
      try:
        questions = Question.query.filter_by(category=str(category_id)).all()
        formatted_questions = paginate(request, questions)

        categories = Category.query.all()
        formatted_categories = {category.id:category.type for category in categories}

        return jsonify({
          'success':True,
          'questions':formatted_questions,
          'total_questions':len(questions),
          'categories':formatted_categories,
          'current_category':category_id,
        })

      except:
        abort(500)


    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    # Tyler - 8 - From 3.5

    @app.route('/api/quizzes', methods=['POST'])
    def play_quiz():
      # Go to ViewQuiz.js to see request contents

      request_contents = request.json

      try:
          request_category = request_contents['quiz_category']['id']
      except:
          abort(400)
      
      # If no category is selected, get all of them
      # Otherwise, query by selected category
      if request_category == 0:
          questions = Question.query.all()
      else:
          questions = Question.query.filter_by(category=str(request_category)).all()

      formatted_questions = [question.format() for question in questions]
      
      # Retrieve previous questions
      try:
          prior_questions = request_contents['previous_questions']
      except:
          abort(400)
      
      # Only allow questions the quiz-taker hasn't seen before
      remaining_questions = []
      for question in formatted_questions:
          if question['id'] not in prior_questions:
              remaining_questions.append(question)

      # If there are no more questions remaining, end the quiz.
      if len(remaining_questions) == 0:
          return jsonify({
              'success': True
          })

      question = random.choice(remaining_questions)

      return jsonify({
          'success': True,
          'question': question
      })


    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    # Tyler - 9 - From 3.6

    # HTTP Status Response Codes:
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        })

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        })

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        })




    return app