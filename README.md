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





## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
