import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from sqlalchemy import desc

from models import setup_db, Book

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.

def paginated_books(books,page):
    if len(books) == 0:
        abort(404)
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

    # @TODO: Write a route that retrivies all books, paginated.
    #         You can use the constant above to paginate by eight books.
    #         If you decide to change the number of books per page,
    #         update the frontend to handle additional books in the styling and pagination
    #         Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars
    @app.route('/books')
    def get_books():
        books = Book.query.order_by(desc(Book.id)).all()
        page = request.args.get('page', 1, type=int)

        formatted_books = paginated_books(books,page)

        return jsonify({
            "success": True,
            "books" : formatted_books,
            "total_books" : len(books)
        })

    # @TODO: Write a route that will update a single book's rating.
    #         It should only be able to update the rating, not the entire representation
    #         and should follow API design principles regarding method and route.
    #         Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh
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

    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'

    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.
    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id):
        try:
            book = Book.query.get(book_id)           

            if book is not None:
                book.delete()
                books = Book.query.all()
                page = request.args.get('page', 1, type=int)

                formatted_books = paginated_books(books,page)

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
    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at the end of the page.
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


