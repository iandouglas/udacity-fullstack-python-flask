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

## API Routes

```bash
python3 manage.py routes
```

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
