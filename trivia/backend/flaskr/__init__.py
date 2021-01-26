import os
import random

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from models import Category, Question, setup_db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, origins={'*'})

    # CORS(app )

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET , POST , PATCH , DELETE , OPTIONS')
        return response

    @app.route('/')
    def hello():
        return jsonify({
            'message': "Helllllllllllo",
        })

    @app.route('/categories')
    def get_categories():
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type
        return jsonify({
            'categories': categories,
            "success": True
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        # start = (page-1) * 10
        # end = start +10
        questions = Question.query.paginate(page, 10)

        # total = Question.total
        total = len(Question.query.all())
        questions = questions.items

        current_category = Question.category

        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type

        questions = [i.format() for i in questions]
        return jsonify({
            'success': True,
            'questions': questions,
            'total': total,
            'categories': categories,
        })

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def del_question(question_id):
        deleted_questions = Question.query.filter(
            Question.id == question_id).one_or_none()

        if deleted_questions is None:
            abort(404)

        else:
            deleted_questions.delete()
            return jsonify({
                'success': True,
                'deleted_questions': deleted_questions.format()
            })

    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')

        q = Question(question=question, answer=answer,
                     category=category, difficulty=difficulty)

        q.insert()

        return jsonify({
            'success': True,
            'question': q.format()
        })

    @app.route('/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        search_term = body.get('searchTerm')
        questions = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()
        questions = [i.format() for i in questions]
        return jsonify({
            'success': True,
            'questions': questions
        })

    @app.route('/categories/<int:id>/questions', methods=['POST'])
    def get_question_by_category(id):
        category = Category.query.filter_by(id=id).one_or_none()
        questions = Question.query.filter(Question.category == str(id)).all()
        questions = [i.format() for i in questions]
        return jsonify({
            'success': True,
            'questions': questions,
            'current_category': category.type
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous = body.get('previous_questions')
        category = body.get('quiz_category')

        if (category['id'] == "0"):
            questions = Question.query.filter(
                Question.id.notin_((previous))).all()
        else:
            questions = Question.query.filter_by(category=category['id']).filter(
                Question.id.notin_((previous))).all()

        new_questions = questions[random.randint(0, len(questions)-1)]

        return jsonify({
            'success': True,
            'question': new_questions.format()
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "page not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app
