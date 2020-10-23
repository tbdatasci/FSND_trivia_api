# Full Stack API Final Project

## Full Stack Trivia

### The Premise

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

### The Project

The app does the following:

1) Display questions - both all questions and by category. Questions should show the question, category, and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

# Getting Started

## How to Start Up the Frontend

### Full Instructions at [`./frontend/`](./frontend/README.md)

### TL;DR

```
npm install
npm start
```

## How to Fire Up the Backend

### Full Instructions at [`./backend/`](./backend/README.md)

### TL;DR

```bash
# Install requirements
pip install -r requirements.txt
# Create the trivia database
psql -U <username> trivia < trivia.psql
# Run flask with given conditions.  (Mac users should substitute "export" for "set" below)
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```
To run unit tests to ensure expected functionality:
```bash
dropdb trivia_test (for Windows: drop database trivia_test)
createdb trivia_test (for Windows: create database trivia_test)
psql trivia_test < trivia.psql
python test_flaskr.py
```

# API Reference
## Notes
1. At present, this app can only be run locally.  The back-end runs at http://127.0.0.1:5000/, and the front-end runs at http://localhost:3000/.
2. At present, this app does not require authentication or API keys.
3. CORS is enabled.

## Error Handling
Errors are returned as JSON objects in the following format:
```bash
{
  "success": False,
  "error": 400,
  "message": "Bad Request"
}
```
The API will return four error types when requests fail:
1.  400: Bad Request
2.  404: Not Found
3.  422: Unprocessable Entity:
4.  500: Internal Server Error

## Endpoints
### GET /api/categories
* General
  * Returns a dictionary of trivia categories where each has an ID and category text.
  * Returns success status.
* Sample: `curl http://localhost:5000/api/categories`
```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### GET /api/questions
* General
  * Returns a dictionary of trivia categories where each has an ID and category text.
  * Returns current category (if any).
  * Returns a list of questions, each containing answer, category, difficulty, id, and question.
  * Paginates to only 10 results per page.
  * Returns success status.
  * Returns total number of questions in database.
* Sample: `curl http://localhost:5000/api/questions`
```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    ... I removed the other eight questions to make this more readable ...
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```

### DELETE /api/questions/<int:question_id>
* General
  * Given a question_id, it will delete the question from our database.
  * Returns question_id of deleted question, a paginated list of the questions still in the database, success status, and the total number of questions still in the database.
* Sample: `curl -X DELETE http://localhost:5000/api/questions/26`
```bash
{
  "deleted": 26,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    ... I removed the other eight questions to make this more readable ...
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

### POST /api/questions
* General
  #### Create Question ####
  * Creates a new question from user input.
  * Returns id of created question, success status, and the first 10 questions in the dataset.
  #### Search Questions ####
  * Can also search questions based on keyword(s) from user input.
  * Returns questions that meet search criteria and success status.
  
* Sample of Create: `curl -X POST http://localhost:5000/api/questions -H "Content-Type: application/json" -d '{"question": "What is the meaning of the universe?", "answer": "12", "category": "1", "difficulty": 5}'`
```bash
{
  "created": 27,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    ... I removed the other eight questions to make this more readable ...
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```

* Sample of Search: `curl -X POST http://localhost:5000/api/questions -H "Content-Type: application/json" -d '{"searchTerm": "Giaconda"}`
```bash
{
  "questions": [
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }
  ],
  "success": true
}
```

### GET /api/categories/<int:category_id>/questions
* General
  * Given a category_id, it will get all of the questions within that category.
  * Returns dictionary of the available categories, selected category, all the questions within that category, success status, and total questions within the category.
* Sample: `curl http://localhost:5000/api/categories/6/questions`
```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": 6,
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

### POST /api/quizzes **********************************************
* General
  * This is where the quiz is played.
  * A random question will be given to the player.
  * This random question will be filtered by category if the player chooses to.
  * The request must include a list of previous questions and the selected category.
  * The response contains a dictionary about the given question as well as a success status.
* Sample when on the first question and filtering by the History category: `curl -X POST http://localhost:5000/api/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"History","id":4}}'`
```bash
{
  "question": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  "success": true
}
```
