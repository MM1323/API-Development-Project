import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
ALL_CATEGORY = None

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """ Review CORs section to see if correect
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """ DONE
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        return response
      
    # Paginate the questions  
    def paginate_ques(request, selection):
      page = request.args.get("page", 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE

      ques = [que.format() for que in selection]
      current_questions = ques[start:end]

      return current_questions
    
    # Gets all categories and returns as an dict
    def get_all_categories():
      categories = Category.query.order_by(Category.id).all()
      return {cat.id: cat.type for cat in categories}
    
    """
    @TODO: Need to test on Curl if works
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=["GET"])
    def get_categories():
      categories = get_all_categories()
      
      if len(categories) == 0:
        abort(404)
      
      return jsonify({
        'success': True,
        "categories": categories
      })

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
    @app.route("/questions", methods=["GET"])
    def get_questions():
      categories = get_all_categories()
      global ALL_CATEGORY
      
      if ALL_CATEGORY == None:
        current_category = 0
        
        questions = Question.query.order_by(Question.difficulty).all()
        current_questions = paginate_ques(request, questions)

        if len(current_questions) < 1:
          abort(404)
        
      else:
        questions = Question.query.filter(Question.category == ALL_CATEGORY).order_by(Question.difficulty).all()
        current_questions = paginate_ques(request, questions)
        
        categories_select = Category.query.all()
        current_category = [cat.type for cat in categories_select if cat.id == ALL_CATEGORY][0]
        
        #questions = Question.query.filter(Question.category == categories[ALL_CATEGORY]).order_by(Question.difficulty).all()
        #current_questions = paginate_ques(request, questions)

        if len(current_questions) < 1:
          abort(404)

      return jsonify({
        "success": True,
        "questions": current_questions,
        "totalQuestions": len(questions),
        "currentCategory": current_category,
        "categories": categories,
      })
    
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
      question = Question.query.get(question_id)

      try:
        question.delete()
        global ALL_CATEGORY
        ALL_CATEGORY = question.category
        print(ALL_CATEGORY)
        return jsonify({
          "success":True,
          "deleted": question.id,
          "totalQuestions": len(Question.query.all()),
          })
      except:
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
    @app.route("/questions", methods=["POST"])
    def add_question():
      body = request.get_json()
      
      new_que = body.get("question")
      new_ans = body.get("answer")      
      new_diff = body.get("difficulty")   
      new_cat = body.get("category")
      search = body.get("searchTerm", None)
      
      try:
        if search:
          selection = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
          search_questions = paginate_ques(request, selection)
          
          return jsonify({
            "success": True,
            "questions": list(search_questions),
            "total_questions": len(selection),
          })          
        else:
          if (new_que, new_ans, new_diff, new_cat) == None:
           abort(422)

          question = Question(
            question=new_que,
            answer=new_ans,
            difficulty=new_diff,
            category=new_cat
          )

          question.insert()
          total_questions = Question.query.all()
          current_questions = paginate_ques(request, total_questions)

          return jsonify({
            "success": True,
            "created": question.id,
            "totalQuestions": len(total_questions),
          })
      
      except:
        abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    # DONE ABOVE

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def category_questions(category_id):
      try:
        selection = Question.query.filter(Question.category == category_id).order_by(Question.difficulty).all()
        current_questions = paginate_ques(request, selection)
        categories = Category.query.all()
        current_category = [cat.type for cat in categories if cat.id == category_id ][0]
        
        if category_id > len(categories):
          abort(404)
          
        return jsonify({
          "success": True,
          "questions": list(current_questions),
          "totalQuestions": len(selection),
          "currentCategory": current_category,
          "categories": get_all_categories(),
        })
      except:
        abort(404)
        

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
    @app.route('/quizzes', methods=['POST'])
    def start_trivia():
      global ALL_CATEGORY
      try:
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        category_id = body['quiz_category']['id']        
        questions = None
        
        if int(category_id) > 0:
          questions = Question.query.filter(Question.category == category_id).order_by(Question.difficulty).all()
        else:
          questions = Question.query.order_by(Question.difficulty).all()
        
        if len(questions) < 1:
          abort(404)

        question = None
        no_question = len(previous_questions)
        
        if no_question < 1:
          question = random.choice(questions).format()
        elif no_question < len(questions):
          question = questions[no_question].format()
        else:
          question = None

        return jsonify({
          'success': True,
          'question': question
        })
      
      except:
        abort(404)
      
      

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )
      
    return app
