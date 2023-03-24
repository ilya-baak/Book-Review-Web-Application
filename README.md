Flask Book Review Web Application
This is a Flask-based web application that allows users to search and review books. The application uses SQLAlchemy and a PostgreSQL database to store book information and user reviews.

This web application allows users to:
Register for an account
Log in to their account
Log out of their account
Search for books by title, ISBN, or author
See search results for books
View book details
Submit a rating and review for a book

Using import.py, we populate the books table in the database, with 5000 books that users can will be able to interact with
In sampleAPI.py, we have a function that pulls data about books with respect to ratings using the Google Books API
In templates, you can find the html pages of the web application
Additionally, requirements.txt includes additional python packages needed to run the application.
