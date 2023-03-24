from sqlalchemy import create_engine, text
import csv

url = ""

# Set up database
engine = create_engine(url)

#Read csv, automatically closes when done
with open('books.csv', 'r') as books:
    reader = csv.reader(books)
    next(reader)

    connection = engine.connect()

    for row in reader:
        print(row[0], row[1], row[2], row[3])
        connection.execute(text('INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)'),
                           {"isbn": row[0], "title": row[1], "author": row[2], "year": row[3]})
    connection.commit()
    connection.close()