import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from sqlalchemy import desc

from models import setup_db, Book

BOOKS_PER_SHELF = 8



def paginated_books(books,page):
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF
    formatted_books = [ book.format() for book in books ]
    return formatted_books[start:end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

  
    @app.route('/books')
    def get_books():
        books = Book.query.order_by(desc(Book.id)).all()
        page = request.args.get('page', 1, type=int)

        formatted_books = paginated_books(books,page)

        if len(formatted_books) == 0:
                    abort(404)


        return jsonify({
            "success": True,
            "books" : formatted_books,
            "total_books" : len(books)
        })

   
    @app.route("/books/<int:book_id>", methods=["PATCH"])
    def update_ratings(book_id):
        body = request.get_json()

        try:
            book = Book.query.get(book_id)

            if book is not None:
                book.rating = int(body.get("rating"))
                book.update()

                return jsonify({ "success": True})
            else:
                abort(404)
        except:
            abort(400)


    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id):
        try:
            book = Book.query.get(book_id)           

            if book is not None:
                book.delete()
                books = Book.query.all()
                page = request.args.get('page', 1, type=int)

                formatted_books = paginated_books(books,page)

                if len(formatted_books) == 0:
                    abort(404)

                return jsonify(
                    { 
                    "success": True,
                    "deleted": book_id,
                    "books": formatted_books,
                    "total_books": len(books)
                    })
            else:
                abort(404)
        except:
            abort(422)

    @app.route('/books', methods=['POST'])
    def create_book():
        body = request.get_json()

        title = body.get('title', None)
        author = body.get('author', None)
        rating = body.get('rating', None)

        books = Book.query.order_by(desc(Book.id)).all()
        page = request.args.get('page', 1, type=int)
        formatted_books = paginated_books(books,page)

        try:
            book = Book(author=author, title=title, rating=rating)
            book.insert()

            return jsonify({
                "success": True,
                "created": book.id,
                "books": formatted_books,
                "total_books": len(books)
            })
        except:
            abort(422)
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad request"
            }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "Method not allowed"
            }), 405

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Cannot process request"
            }), 422
    
    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Server Error"
            }), 500

    return app


