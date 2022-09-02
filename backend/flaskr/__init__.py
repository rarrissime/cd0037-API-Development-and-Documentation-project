import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) *    QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def dictionary_categories(selection):
    categories = [category.format() for category in selection]
    data = {}
    for category in categories:
        data.update(category)

    return data

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*" : {"origins": "*"}})
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PUT, DELETE')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")   
    def retrieve_categories():
        selection = Category.query.order_by(Category.id).all()
        categories = dictionary_categories(selection)

        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": categories,
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        question_selection =Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, question_selection)
        category_selection = Category.query.order_by(Category.id).all()
        categories = dictionary_categories(category_selection)
        
        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": categories,
                "current_category": "Placeholder"
            }
        )
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """ 
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify(
                {
                    "success": True,
                }
            )

        except BaseException:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions", methods=["POST"])
    def search_or_create_question():

        try:
            body = request.get_json()

            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_difficulty = body.get("difficulty", None)
            new_category = body.get("category", None)
            search = body.get("searchTerm", None)
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                )
                questions = [question.format() for question in selection]

                return jsonify(
                    {
                        "success": True,
                        "questions": questions,
                        "total_questions": len(selection.all()),
                        "current_category": "Placeholder"
                    }
                )
            elif new_question:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category)
                question.insert()

                return jsonify(
                    {
                        "success": True,
                    }
                )

        except BaseException:
            abort(400)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def retrieve_questions_byCategory(category_id):
        selection = Question.query.order_by(Question.id).filter(
            Question.category == category_id
        )
        questions = [question.format() for question in selection]

        if len(questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": questions,
                "total_questions": len(selection.all()),
                "current_category": "Placeholder"
            }
        )

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def retrieve_random_question():
        try:
            body = request.get_json()

            past_questions = body.get("previous_questions", None)
            quiz_category = body.get("quiz_category", None)
            category_id = quiz_category["id"]

            if category_id == 0:
                rand_selection = Question.query.order_by(func.random())
                selection = rand_selection.filter(
                    Question.id.not_in(past_questions)).first()

                if selection is not None:
                    question = selection.format()
                    return jsonify(
                        {
                            "success": True,
                            "question": question,
                        }
                    )
                return jsonify(
                    {
                        "question": None,
                    }
                )
            else:
                rand_selection = Question.query.order_by(func.random())
                selection = rand_selection.filter(
                    Question.category == category_id,
                    Question.id.not_in(past_questions)).first()

                if selection is not None:
                    question = selection.format()
                    return jsonify(
                        {
                            "success": True,
                            "question": question,
                        }
                    )
                return jsonify(
                    {
                        "question": None,
                    }
                )
        except BaseException:
            abort(404)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                     "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400,
                    "message": "bad request"}),
            400,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({"success": False, "error": 500,
                    "message": "internal server error"}),
            500,
        )
    return app

