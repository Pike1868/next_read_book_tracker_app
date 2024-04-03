from flask import render_template, request, flash
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from ..models import Book, UserBooks, db
import requests
import os

books_bp = Blueprint('books_bp', __name__)


@books_bp.route('/search', methods=['POST'])
def search_google_books():
    startIndex = int(request.form.get('startIndex', 0))
    query = request.form.get('query')
    books = []
    if request.method == 'POST':
        query = request.form.get('query')
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q={query}&key={os.environ.get('API_KEY')}&startIndex={startIndex}&printType=books&maxResults=40")
        data = response.json()

        if "items" in data:
            for item in data["items"]:
                book_info = item["volumeInfo"]
                books.append({
                    "google_books_id": item["id"],
                    "title": book_info.get("title", "Unknown Title"),
                    "authors": book_info.get("authors", ["Unknown Author"]),
                    "thumbnail_url": book_info.get("imageLinks", {}).get("thumbnail", ""),

                })

    return render_template('/users/index.html', books=books, query=query, startIndex=startIndex)


@books_bp.route('/search_genre/<genre>', methods=["GET", "POST"])
def search_genre(genre):
    startIndex = request.form.get('startIndex', 0, type=int)
    genre_books = []
    response = requests.get(
        f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&startIndex={startIndex}&printType=books&maxResults=40"
    )
    data = response.json()
    # print(data)

    if "items" in data:
        for item in data["items"]:
            book_info = item["volumeInfo"]
            genre_books.append({
                "google_books_id": item["id"],
                "title": book_info.get("title", "Unknown Title"),
                "authors": book_info.get("authors", ["Unknown Author"]),
                "thumbnail_url": book_info.get("imageLinks", {}).get("thumbnail", ""),
            })

    return render_template('/users/index.html', books=genre_books, query=genre, startIndex=startIndex)


@books_bp.route('/detail/<volume_id>')
def detail(volume_id):
    response = requests.get(
        f"https://www.googleapis.com/books/v1/volumes/{volume_id}?key={os.environ.get('API_KEY')}")
    data = response.json()

    book_detail = data["volumeInfo"]

    return render_template('books/detail.html', book=book_detail, google_books_id=volume_id)


@books_bp.route('/save-book', methods=['POST'])
@login_required
def save_book():
    user_id = current_user.id
    google_books_id = request.form.get('google_books_id')
    status = request.form.get('status')

    book = Book.query.filter_by(google_books_id=google_books_id).first()

    if not book:
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes/{google_books_id}?key={os.environ.get('API_KEY')}")

        data = response.json()["volumeInfo"]

        new_book = Book(
            google_books_id=google_books_id,
            title=data.get("title", "Unknown Title"),
            authors=", ".join(data.get("authors", ["Unknown Author"])),
            thumbnail_url=data.get("imageLinks", {}).get("thumbnail", ""),
            description=data.get("description", "No description available."),
            published_date=data.get("publishedDate", "Date not available"),
            average_rating=data.get("averageRating", None),
            ratings_count=data.get("ratingsCount", 0),
            page_count=data.get("pageCount")
        )

        db.session.add(new_book)
        db.session.flush()

        user_book_link = UserBooks(
            user_id=user_id, book_id=new_book.id, status=status)
        db.session.add(user_book_link)

    else:
        user_book_link = UserBooks.query.filter_by(
            user_id=user_id, book_id=book.id).first()

        if user_book_link:
            user_book_link.status = status

        else:
            user_book_link = UserBooks(
                user_id=user_id, book_id=book.id, status=status)
        db.session.add(user_book_link)

    db.session.commit()

    return redirect(url_for('main_bp.home'))


@books_bp.route('/<volume_id>/remove', methods=["POST"])
def remove_user_book(volume_id):

    book_to_remove = Book.query.filter_by(google_books_id=volume_id).first()

    user_book = UserBooks.query.filter_by(
        user_id=current_user.id, book_id=book_to_remove.id).first()

    if user_book:
        db.session.delete(user_book)
        db.session.commit()
        flash("Book removed successfully", "success")
    else:
        flash("Book not found in your lists", "warning")

    return redirect(url_for("main_bp.home"))


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask


@books_bp.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
