import os
from flask import Flask, session, render_template, redirect, url_for, request
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from sampleAPI import getAPIRatings


app = Flask(__name__)

os.environ["DATABASE_URL"]
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return redirect(url_for('login'))


# Webpage to register an Account
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get username and password from form
        username = request.form.get("username")
        password = request.form.get("password")
        # Add new user to database
        db.execute(text("INSERT INTO users (username, password) VALUES (:username, :password)"),
                   {"username": username, "password": password})
        db.commit()
        #Go to page to login
        return redirect(url_for('login'))
    #Otherwise stay on register page, e.g. for invalid registration
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #Get typed username and password from login page
        username = request.form.get("username")
        password = request.form.get("password")
        # Search DB for user/pass combination
        user = db.execute(text("SELECT * FROM users WHERE username = :username AND password = :password"),
                           {"username": username, "password": password}).fetchone()

        # Could not find user/pass combination in DB
        if user is None:
            return render_template("login.html", message="Invalid username or password")

        # Store userid in session
        session["user_id"] = user.id
        # Go to home page
        return redirect(url_for('home'))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for('login'))


# Performs the search based on if there are anymatches wrt Title, ISBN, or authors
def search(input):
    cursor = db.execute(text('SELECT * FROM books WHERE title LIKE :input OR ISBN LIKE :input OR author LIKE :input'),
                   {"input": '%' + input + '%'})
    return cursor.fetchall()


#Home Page where user can search for books.
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        # Performs search on the input from textbox.
        result = search(request.form.get('input'))
        if result:
            # Reloads the home page with all the results, passes the results to home.html
            return render_template('home.html', result=result)
        else:
            # Search returned no matches
            return render_template('home.html', message='No results matched your search')

    # If session expires, return to login
    if "user_id" not in session:
        return redirect(url_for('login'))
    # Passes current user row to home.html
    user = db.execute(text("SELECT * FROM users WHERE id = :id"), {"id": session["user_id"]}).fetchone()
    return render_template("home.html", username=user.id)



@app.route("/book", methods=["GET", "POST"])
def book():
    ISBN = request.args.get("ISBN")     #Gets the ISBN from book.html, which was passed from home.html
    userID = session.get("user_id")     #Gets the current user's id from session

    if request.method == "POST":
        # Get the rating/review from the input on the page
        rating = request.form.get('rating')
        review = request.form.get('review')

        # Checks to if the user has already posted a review
        inDB = db.execute(text('SELECT id FROM reviews WHERE book_isbn=:ISBN AND user_id=:userID'),
                          {'ISBN': ISBN, 'userID': userID}).fetchone()

        # If it's not in the DB, create a new review/rating in the DB
        if not inDB:
            if review is None and rating is not None:
                db.execute(text('INSERT INTO reviews (user_id, book_isbn, rating, review) '
                                'VALUES (:userID, :ISBN, :rating, :review)'),
                           {"userID": userID, "ISBN": ISBN, "rating": rating, "review": review})

            elif rating is None and review is not None:
                db.execute(text('INSERT INTO reviews (user_id, book_isbn, rating, review) '
                                'VALUES (:userID, :ISBN, :rating, :review)'),
                           {"userID": userID, "ISBN": ISBN, "rating": rating, "review": review})

        # If it's already in the DB, update the review/rating in the DB
        else:
            if review is None and rating is not None:
                db.execute(text('UPDATE reviews SET rating = :rating WHERE user_id = :userID AND book_isbn = :ISBN'),
                           {'rating': rating, 'userID': userID, 'ISBN': ISBN})

            elif rating is None and review is not None:
                db.execute(text('UPDATE reviews SET review = :review WHERE user_id = :userID AND book_isbn = :ISBN'),
                           {'review': review, 'userID': userID, 'ISBN': ISBN})

    #Fetch the book data
    book = db.execute(text('SELECT * FROM books WHERE ISBN = :isbn'), {'isbn': ISBN}).fetchone()
    #Fetch all the reviews from the db for the given book
    reviews = db.execute(text('SELECT rating, review, created_at FROM reviews WHERE book_isbn = :ISBN'),
                             {'ISBN': ISBN}).fetchall()

    # Get the ratings and count from Google Books API
    API_data = getAPIRatings(ISBN)
    db.commit()
    return render_template('book.html', book=book, reviews=reviews, API_data=API_data)


if __name__ == '__main__':
    app.run(debug=True)