from flask import Flask, render_template, jsonify, request, redirect, url_for
import csv
from pathlib import Path
from db import db
from sqlalchemy import select
from models import Book
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///i_copy_pasted_this.db"
app.instance_path = Path("./data").resolve()

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv('NYT_API_KEY')

# Initialize the database with the Flask app
db.init_app(app)

# Route for the home page
@app.route("/")
def home():
    url = 'https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json'
    response = requests.get(url, params={'api-key': api_key})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()  # Convert response to JSON

        # Check if 'results' exist in the response data
        if 'results' in data:
            books = data['results']
            
            # Prepare a list of books with relevant data
            book_list = []
            for book in books:
                # Extract book details from the 'book_details' list
                if 'book_details' in book and isinstance(book['book_details'], list):
                    book_details = book['book_details'][0]  # Assuming the first item in the list is the desired one
                    
                    book_list.append({
                        'title': book_details.get('title', 'No title'),
                        'author': book_details.get('author', 'Unknown'),
                        'description': book_details.get('description', 'No description available'),
                        'thumbnail': book_details.get('cover_image', ''),  # Assuming cover_image is the image URL field
                    })
                else:
                    print("No book_details found or wrong format")
            
            # Render the books in the template
            return render_template('home.html', books=book_list)
        else:
            return "No books found in the response data", 404
    else:
        # If the API request failed, return an error message
        return f"Failed to fetch data from the NYT API. Status Code: {response.status_code}", 500
    
# Route for the books listing page
@app.route("/books")
def book():
    book_stmt = select(Book)
    book_list = db.session.execute(book_stmt).scalars()
    return render_template("books.html", books=book_list)

# Route for displaying details of a specific book
@app.route("/books/<int:book_id>")
def book_detail(book_id):

    book_info_stmt = select(Book).where(Book.id == book_id)
    book_info = db.session.execute(book_info_stmt).scalar() 
    return render_template("books_page.html", book=book_info)

@app.route("/api/books/<int:book_id>")
def api_book_detail(book_id):
    # Query the database for the book with the given ID
    book = db.session.get(Book, book_id)
    
    # If the book does not exist, return a 404 error
    if not book:
        return {"error": "Book not found"}, 404

    return jsonify(book)

@app.route('/add_book', methods=['POST'])
def add_book():
    data = request.get_json()  # Get JSON data from the request
    user_title = data.get('title', '').strip().lower()  # Ensure title is provided and normalized
    url = f"https://openlibrary.org/search.json?title={user_title}"

    # Fetch data from Open Library API
    response = requests.get(url)

    if response.status_code == 200:
        book_data = response.json()

        if book_data.get('docs'):
            # Look for an exact match in the search results
            exact_match = None
            for book in book_data['docs']:
                book_title = book.get('title', '').strip().lower()
                if book_title == user_title:
                    exact_match = book
                    break

            if exact_match:
                # Extract data from the exact match
                title = exact_match.get('title', 'Unknown')
                author = exact_match.get('author_name', ['Unknown'])[0]
                cover_i = exact_match.get('cover_i', None)
            else:
                # Handle no exact match found
                return jsonify({'error': 'No exact match found for the provided title'}), 404
        else:
            return jsonify({'error': 'No books found in the search results'}), 404
    else:
        return jsonify({'error': 'Failed to fetch data from Open Library API'}), 500

    # Additional data from the request
    rating = data.get('rating', 0)
    status = data.get('status', 'Plan To Read')
    progress = data.get('progress', 0)
    total_pages = data.get('total_pages', 0)

    # Create a new Book instance
    new_book = Book(
        title=title,
        author=author,
        rating=rating,
        status=status,
        progress=progress,
        total_pages=total_pages,
        thumbnail=cover_i,
    )

    # Add the new book to the session and commit to the database
    db.session.add(new_book)
    db.session.commit()

    # Return a success response
    return jsonify({'message': 'Book successfully added!'}), 200



if __name__ == "__main__":
    app.run(debug=True, port=8888)