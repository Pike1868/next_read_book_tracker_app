-- Drop existing tables if they exist
DROP TABLE IF EXISTS user_books;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;
-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    bio TEXT,
    location TEXT,
    image_url TEXT DEFAULT '/static/images/default-pic.png',
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hashed_password TEXT NOT NULL
);
-- Create the books table
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    google_books_id TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    authors TEXT NOT NULL,
    thumbnail_url TEXT NOT NULL,
    description TEXT,
    published_date TEXT,
    average_rating FLOAT,
    ratings_count INTEGER,
    page_count INTEGER
);
-- Create the user_books table
CREATE TABLE user_books (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL
);