CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE books (
    isbn VARCHAR(20) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users,
    book_isbn VARCHAR(20) NOT NULL REFERENCES books,
    rating INTEGER,
    review TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE reviews ALTER COLUMN rating DROP NOT NULL;


