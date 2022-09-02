# API Development and Documentation Final Project

## Trivia App

The goal of this project is to use APIs to control and manage a web application using existing data models. A REST API is developed using Test Driven Development (TDD) with the following functionality:

1. Displays questions: 
    - All questions and by category. 
    - Show the question, category, and difficulty.
    - Show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

### Applied concepts

- The code adheres to the `PEP 8` style guide and follows common best practices.
- RESTful principles are followed throughout the project, including appropriate naming of endpoints, use of HTTP methods GET, POST, and DELETE.
- Project handles common errors using the `@app.errorhandler` decorator function to format an API friendly JSON error response.
- `Unittest`  was used to test each endpoint for expected success and error behavior. 

### About the Stack

Tech stack includes:
- `React.js` for the website's frontend (provided by Udacity Team).
- `Python3` and `Flask` as server-side language and server-side framework.~
- `PostgreSQL` as database of choice.
- `SQLAlchemy ORM` as ORM library of choice.

### Getting Started

#### Backend

##### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PostgreSQL** - Make sure to have PostgreSQL installed, if it is not installed, follow instructions to download PostgreSQL in [PostgreSQL Downloads](https://www.postgresql.org/download/)

4. **PIP Dependencies** - Install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
##### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql`. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

##### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically. By default, the Flask server runs on http://localhost:5000.

##### API Reference and Test

Project includes tests to ensure CRUD operations are successful and persist accurately in the database for GET, POST, PUT and DELETE HTTP requests.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
Omit the `dropdb` command the first time you run tests.

View the [API README](./backend/README.md) for detailed documentation of API endpoints which includes URL, request parameters and the response body.

#### Frontend

> _tip_: this frontend is designed to work with Flask-based Backend. so it will not load successfully if the backend is not working or not connected. Stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.
##### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: `npm i`is shorthand for `npm install`
##### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```
