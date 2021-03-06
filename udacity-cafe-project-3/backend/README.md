# Coffee Shop Backend

## Getting Started

Introduction video: https://www.youtube.com/watch?v=Xz5nULulr7s


### Installing Dependencies

#### Python 3.7 or newer

Follow instructions to install the latest version of python for your platform in the 
[python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

Instructions for setting up a virtual environment for your platform can be found in the 
[python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` 
directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.
- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.


## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
# build and seed the database
DATABASE_URL=postgres://localhost/cafe_dev python manage.py db_seed

# run Flask
export FLASK_APP=api
export FLASK_DEBUG=true
flask run --reload
```

## Running tests

```bash
export FLASK_APP=api
export FLASK_DEBUG=true
export DATABASE_URL=postgres://localhost:5432/cafe_test

rm -rf .coverage coverage_html_report/ .pytest_cache/
coverage erase
coverage run -m pytest && coverage html && open coverage_html_report/index.html
```

## API Endpoints

To view all API Routes
```bash
python3 manage.py routes
```

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions

(completed up to here so far)

7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./auth/auth.py`
2. `./api.py`
