# Udacity Python Full-Stack NanoDegree Project 2: Udicitrivia

## Getting Started

### Installing Dependencies

#### Python 3.7 or newer (I developed on 3.8)

Follow instructions to install the latest version of python for your platform in the 
[python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for
each project separate and organized. Instructions for setting up a virtual environment for your platform can be found 
in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` 
directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. 
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 
- [Flask-RESTful]() I decided to emulate Miguel Grinberg's "flasky" app for layout since it's a much more robust method of building a Flask-based API

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
createdb trivia
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export DATABASE_URL="postgres://localhost:5432/trivia"
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Notes:
- Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.
- Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing

To run the tests, run
```
createdb trivia_test
# DO NOT RUN `psql trivia_test < trivia.psql`
# the tests will set up everything they need (as they should!)

export DATABASE_URL="postgres://localhost:5432/trivia_test"
export FLASK_APP=flaskr
export FLASK_ENV=testing

rm -rf .coverage coverage_html_report/ .pytest_cache/
coverage erase
coverage run -m pytest && coverage html && open coverage_html_report/index.html
```


## API Endpoints

To view all API Routes
```bash
python3 manage.py routes
```

### Retrieve categories for Trivia Game

Request:
- GET /categories
- Query Parameters:
  - none
- URI Parameters:
  - none
- Required body in JSON format:
  - none

Response:
- 200 status code
- Data payload:
```json
{
    "categories": {
        "2": "Art",
        "5": "Entertainment",
        "3": "Geography",
        "4": "History",
        "1": "Science",
        "6": "Sports"
    }
}
```
  - categories: an object of all category names in alphabetical order and their respective ID values


### Retrieve questions for Trivia Game

Request:
- GET /questions
- Query Parameters:
  - page - optional, will request paginated results, hard-limited to 10 per page
- URI Parameters:
  - none
- Required body in JSON format:
  - none

Response:
- 200 status code
- Data payload:
```json
{
    "total_questions": 22,
    "categories": {
        "2": "Art",
        "5": "Entertainment",
        "3": "Geography",
        "4": "History",
        "1": "Science",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4
        },
        {...}
    ]
}
```
  - questions: an array of questions (if any) for the requested page; if an invalid page number is given, this array will be empty
  - total_questions: total count (integer) of questions in the database
  - current_category: always null
  - categories: an object of all category names in alphabetical order and their respective ID values


### Retrieve all questions for a given category

Request:
- GET /categories/<integer id>/questions
- Query Parameters:
  - none
- URI Parameters:
  - the category ID is given in integer form
- Required body in JSON format:
  - none

Response:
- 200 status code
- Data payload:
```json
{
    "current_category": null,
    "total_questions": 6,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {...}
    ]
}
```
  - questions: an array of questions for the requested category, if any; if category has no questions, returns an empty array
  - total_questions: total count (integer) of questions in the database for this category
  - current_category: always null



### Create a trivia question for a category

Request:
- POST /questions
- Query Parameters:
  - none
- URI Parameters:
  - none
- Required body in JSON format:
```json
{
    "question": "my_question",
    "answer": "my_answer",
    "difficulty": "4",
    "category": "5"
}
```
  - question: string, question presented to user
  - answer: string, the answer to the given question
  - difficulty: string, a numeric value of 1 to 5
  - category: string, a numeric value of which category ID with which to associate this question

Response:
- 201 status code on success
- Data payload:
```json
{
    "message": "New question successfully added",
    "question": {
        "id": 27,
        "question": "my_question",
        "answer": "my_answer",
        "category": 5,
        "difficulty": 4
    }
}
```
  - question: an object showing the data of the question including its new ID value
  - message: string, indicating success

Error Conditions:
- a 400 error will be returned with an error payload:
```json
{
    "message": "New question was not added, check errors for reasons",
    "errors": [
        "Question text cannot be blank, or was not a string",
        "Answer text cannot be blank, or was not a string",
        "Difficulty integer cannot be blank, and must be an integer between 1 and 5",
        "Category integer cannot be blank, or is set to an invalid category"
    ]
}
```
  - message: string, indicating an error has occurred
  - errors: array, contains one or more strings indicating why the question was not successfully added to the database

Diagnostics for Error Conditions:
- "Question text cannot be blank, or was not a string"
  - ensure the question you are sending is in a valid string format, is not blank (trailing/leading whitespace is removed upon submission)
- "Answer text cannot be blank, or was not a string"
  - ensure the answer you are sending is in a valid string format, is not blank (trailing/leading whitespace is removed upon submission)
- "Difficulty integer cannot be blank, and must be an integer between 1 and 5"
  - the difficulty value was not numeric, not a whole number (integer), or was outside of the 1 to 5 range
- "Category integer cannot be blank, or is set to an invalid category"
  - the category value was not numeric, not a whole number (integer), or did not match the ID of an existing category


### Delete a trivia question

Request:
- DELETE /questions/<integer id>
- Query Parameters:
  - none
- URI Parameters:
  - none
- Required body in JSON format:
  - none

Response:
- 204 status code on success
- Data payload:
  - none

Error Conditions:
- a 404 status code will be returned if question ID is invalid or not found with the following JSON:
```json
{
    "message": "Resource not found"
}
```
  - message: string, indicating the ID you gave was not found in the database


### Play a game of Trivia

Request:
- GET /quizzes
- Query Parameters:
  - none
- URI Parameters:
  - none
- Required body in JSON format:
```json
{
    "previous_questions": [array of integers],
    "quiz_category": {category object, described below}
}
```
  - previous_questions: array of integers of question IDs which have been previously asked to the user
  - quiz_category: object of category `{"type": "Art", "id": "2"}`
    - if you wish to randomly select any category, send the following category object: `{"type": "all", "id": "0"}`

Response:
- 200 status code on success
- Data payload:
```json
{
    "question": {
        "id": 17,
        "question": "La Giaconda is better known as what?",
        "answer": "Mona Lisa",
        "category": 2,
        "difficulty": 3
    }
}
```
  - question: object of question data, if any questions are found
    - if all questions for a category have been exhausted, an empty object `{}` is returned in the response body

Error Conditions:
- if the category ID you send in the request body does not match something in the database, a 200 status code is returned, but the response body will be an empty object, `{}`
