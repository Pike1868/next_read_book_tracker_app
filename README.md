# README

## Capstone 1: Next Read Book Tracker App

# Project Overview

**Next Read** is a web application developed using Flask. It provides a platform for users to search, save, and categorize books they're reading, have read, or want to read. This app uses the Google Books API for a vast library of book data retrieval. Currently, the app requires enhancements for optimal responsiveness on smaller screens and mobile devices.

## Why I Chose This Project

### Problem Statement and Goal

The main objective is to create a platform for both avid readers and beginners who aspire to read more. I wanted to build an app that allowed users to track their books and see the progress on their reading habits, and eventually allow users to create and track their reading goals. Making book discovery both easy and personalized by offering book recommendations based on a user's favorite genres, authors, and previously read books.

### Target Demographics

The primary users of this platform are:
- Individuals passionate about reading and on the lookout for their next book to read.
- People who want to keep tabs on their reading habits.
- Anyone aspiring to cultivate a reading habit to enjoy the many benefits that reading provides, as highlighted [here](https://www.healthline.com/health/benefits-of-reading-books).

### Demographics by Stats

- **Reading Patterns:** 19% of US adults are responsible for 79% of books read annually, as indicated in this article [research](https://journals.sagepub.com/doi/full/10.1177/1367549419886026).
  
- **Gender Distribution:** Another interesting bit of information I found: According to data gathered by Zippia, 64.3% of readers are women, while 35.7% are men. More details can be found [here](https://myclasstracks.com/us-book-reading-statistics/).

## Project Directory Structure:

next_read_book_tracker/
│
├── app/
│ ├── init.py # Sets up the Flask application and adds extensions
│ ├── config.py # Application configuration settings
│ ├── forms.py # Contains form classes
│ ├── models.py # Defines database models
│ │
│ ├── routes/
│ │ ├── users.py 
│ │ └── books.py 
│ │
│ ├── static/
│ │ ├── images/ 
│ │ └── css/ 
│ │
│ ├── templates/
│ │ ├── books/
│ │ │ ├── detail.html
│ │ │ └── user_tracked_books.html
│ │ │
│ │ ├── users/
│ │ │ ├── base.html
│ │ │ ├── edit.html
│ │ │ ├── index.html
│ │ │ ├── profile.html
│ │ │ ├── sign_in.html
│ │ │ └── sign_up.html
│ │
│ └── tests/
│ ├── test_books.py # Tests for book-related functionalities
│ └── test_users.py # Tests for user-related functionalities
│
└── README.md
## Features and Routes

### User Authentication:

- **Sign Up:** `@users_bp.route('/sign_up', methods=["GET", "POST"])`
- **Sign In:** `@users_bp.route('/sign_in', methods=["GET", "POST"])`
- **Edit Profile:** `@users_bp.route("/profile/edit", methods=["GET", "POST"])`
- **Sign Out:** `@users_bp.route("/sign_out", methods=["POST"])`
- **Delete User:** `@users_bp.route("/delete", methods=["POST"])`

### Book Management:

- **Search Books (Google API):** `@books_bp.route('/search', methods=['POST'])`
- **Genre-based Search:** `@books_bp.route('/search_genre/<genre>', methods=["GET", "POST"])`
- **Book Details:** `@books_bp.route('/detail/<volume_id>')`
- **Save Book:** `@books_bp.route('/save-book', methods=['POST'])`
- **Remove Book:** `@books_bp.route('/<volume_id>/remove', methods=["POST"])`

## Insights from the Development

Creating an application from scratch was challenging. While I had many ideas and I though they would be rather simple to conceptualize, integrating all of them into a functional application was easier said than done. This project, in particular helped me understand the importance of planning and has increased my awareness of what goes into development while also providing me with experience to make more accurate estimations of projects going forward. Also  the unpredictability's of development, allowed me to dive deeper into Python, Flask, server-side rendering, database design, css frameworks and testing.

## Future Goals and Improvements:

- **Responsiveness Enhancements:** As a priority, refining the user experience on smaller screens and mobile devices.
- **Social Integration:** Allow users to follow other readers, to create a community feel.
- **Recommendation System:** Provide book suggestions based on a user's reading history.
- **Reading Goal Setting:** Plans to integrate a system allowing users to set and track reading milestones and suggestions on reading plans.
- **Reading Clubs:** Like Meetup, but for books. Users can start or join clubs centered around certain genres, authors, or titles.
- **Community Challenges:** Set up challenges like reading a set number of books in a set time period or a set number of pages per day.
- **Integration with More APIs:** Adding other book apis like the New York Times Best Sellers API,to help with the recommendations for users to read.
- **Security Enhancements:** As the user base grows, prioritize the security of user data, including encrypted passwords and two-factor authentication.


- Initial Project Proposal: https://docs.google.com/document/d/1HtxSaqOavbiUVMYkoIC5m8_OQVsrk3ADwcKqpKc-AJg/edit

- Database Schema: https://docs.google.com/document/d/1QJm9H24GYfQvAfwihd47M6fNrUKKpRvfEfBLsxm5TrQ/edit?usp=sharing