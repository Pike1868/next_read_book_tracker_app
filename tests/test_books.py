import unittest
from unittest.mock import patch, Mock
from app import create_app, db
from app.models import Book, User, UserBooks


class TestBooks(unittest.TestCase):

    def setUp(self):
        self.app = create_app('Testing')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            existing_user = User(username="existingUser",
                             password="somepassword",
                             email="existingUser@test.com")
            db.session.add(existing_user)
            db.session.commit()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()



# ====================== Testing search_google_books function and that the data for a search is displayed correctly =============================
    @patch('app.routes.books.requests.get')
    def test_search_google_books(self, mock_get):

        mock_response_data = {
            'kind': 'books#volumes',
            'totalItems': 1,
            'items': [{
                'kind': 'books#volume',
                'id': 'aJQILlLxRmAC',
                'selfLink': 'https://www.googleapis.com/books/v1/volumes/aJQILlLxRmAC',
                'volumeInfo': {
                    'title': 'Python Programming',
                    'authors': ['John M. Zelle'],

                },

            }]
        }
        mock_get.return_value.json.return_value = mock_response_data

        response = self.client.post('/search', data={'query': 'Python', 'startIndex': 0})

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Python Programming', data)
        self.assertIn('John M. Zelle', data)
        self.assertIn('aJQILlLxRmAC', data)

# ====================== Testing that the data for a search by genre is displayed correctly =============================
    @patch('app.routes.books.requests.get')
    def test_search_genre(self, mock_get):

        mock_response_data = {
            'kind': 'books#volumes',
            'totalItems': 73,
            'items': [{
                'kind': 'books#volume',
                'id': 'CQlnKQbwnEcC',
                'volumeInfo': {
                    'title': 'The Testing',
                    'authors': ['Joelle Charbonneau'],
                    'imageLinks': {
                        'thumbnail': 'http://books.google.com/books/content?id=CQlnKQbwnEcC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'
                    }
                }
            }]
        }
        mock_get.return_value.json.return_value = mock_response_data

        response = self.client.post('/search_genre/Sci-fi', data={'startIndex': 0})

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('The Testing', data)
        self.assertIn('Joelle Charbonneau', data)
    #     self.assertIn('href="/detail/CQlnKQbwnEcC"', data)


# ====================== Testing that the data for the detailed page for a book is displayed correctly =============================

    @patch('app.routes.books.requests.get')
    def test_detail(self, mock_get):

        mock_response_data = {
            'kind': 'books#volume',
            'id': 'aJQILlLxRmAC',
            'volumeInfo': {
                'title': 'The Testing',
                'authors': ['Joelle Charbonneau'],
                'publisher': 'Houghton Mifflin Harcourt',
                'publishedDate': '2013',
                'description': (
                    "<p>The opening volume in the New York Times bestselling Testing trilogy. In Cia's dystopian society, it's an honor to be chosen for The Testing. But it's not enough to pass the Test. Cia will have to survive it.</p>"
                    "<p>It's graduation day for sixteen-year-old Malencia Vale, and the entire Five Lakes Colony (the former Great Lakes) is celebrating. All Cia can think about--hope for--is whether she'll be chosen for The Testing, a United Commonwealth program that selects the best and brightest new graduates to become possible leaders of the slowly revitalizing post-war civilization.</p>"
                    "<p>When Cia is chosen, her father finally tells her about his own nightmarish half-memories of The Testing. Armed with his dire warnings (\"Cia, trust no one\"), she bravely heads off to Tosu City, far away from friends and family, perhaps forever. Danger, romance--and sheer terror--await.</p>"
                    "<p>\"The Testing is a chilling and devious dystopian thriller that all fans of The Hunger Games will simply devour. Joelle Charbonneau writes with guts and nerve but also great compassion and heart. Highly recommended.\"--Jonathan Maberry, New York Times bestselling author of Rot & Ruin and Flesh & Bone</p>"
                    "<p>The Testing trilogy is: </p>"
                    "<ul>"
                    "<li>The Testing</li>"
                    "<li>Independent Study</li>"
                    "<li>Graduation Day</li>"
                    "</ul>"
                ),
                'industryIdentifiers': [
                    {'type': 'ISBN_13', 'identifier': '9780547959108'},
                    {'type': 'ISBN_10', 'identifier': '0547959109'}
                ],
                'readingModes': {'text': False, 'image': True},
                'pageCount': 344,
                'printedPageCount': 355,
                'dimensions': {
                    'height': '22.00 cm',
                    'width': '14.00 cm',
                    'thickness': '2.90 cm'
                },
                'printType': 'BOOK',
                'averageRating': 4,
                'ratingsCount': 79,
                'maturityRating': 'NOT_MATURE',
                'allowAnonLogging': False,
                'contentVersion': '0.2.0.0.preview.1',
                'panelizationSummary': {
                    'containsEpubBubbles': False,
                    'containsImageBubbles': False
                },
                'imageLinks': {
                    'smallThumbnail': 'http://books.google.com/books/content?id=CQlnKQbwnEcC&printsec=frontcover&img=1&zoom=5&edge=curl&imgtk=AFLRE72GgqmYupqd5A8az9DaxQGRyh19POLTA6krky60XFkdAVBfQHlmLo-nxnpSrlnDC7zPBwFlCn0jDwWqDsxxyW2rcRWT2vVpoC2KfXLVrX1kOV0pnKYnzNmMRbEaFSp1FI7oCEEp&source=gbs_api',
                    'thumbnail': '...',
                    'small': '...',
                    'medium': '...',
                    'large': '...',
                    'extraLarge': '...'
                },
                'language': 'en',
                'previewLink': 'http://books.google.com/books?id=CQlnKQbwnEcC&hl=&source=gbs_api',
                'infoLink': 'https://play.google.com/store/books/details?id=CQlnKQbwnEcC&source=gbs_api',
                'canonicalVolumeLink': 'https://play.google.com/store/books/details?id=CQlnKQbwnEcC'
            }

        }
        mock_get.return_value.json.return_value = mock_response_data
        

        response = self.client.get('/detail/aJQILlLxRmAC')
        data = response.get_data(as_text=True)
        
        mock_get.assert_called_once()

        self.assertEqual(response.status_code, 200)
        self.assertIn('The Testing', data)
        self.assertIn('Joelle Charbonneau', data)
        self.assertIn('0547959109', data)
        self.assertIn("The opening volume in the New York Times", data)

# ======================= Test that a book is saved to the database, and a relationship to the user is created ===========================  
    
    @patch('requests.get')
    def test_save_new_book(self, mock_get):

        mock_response_data = {
            'kind': 'books#volume',
            'id': 'aJQILlLxRmAC',
            'volumeInfo': {
                'title': 'The Testing',
                'authors': ['Joelle Charbonneau'],
                'publisher': 'Houghton Mifflin Harcourt',
                'publishedDate': '2013',
                'description': (
                    "<p>The opening volume in the New York Times bestselling Testing trilogy. In Cia's dystopian society, it's an honor to be chosen for The Testing. But it's not enough to pass the Test. Cia will have to survive it.</p>"
                    "<p>It's graduation day for sixteen-year-old Malencia Vale, and the entire Five Lakes Colony (the former Great Lakes) is celebrating. All Cia can think about--hope for--is whether she'll be chosen for The Testing, a United Commonwealth program that selects the best and brightest new graduates to become possible leaders of the slowly revitalizing post-war civilization.</p>"
                    "<p>When Cia is chosen, her father finally tells her about his own nightmarish half-memories of The Testing. Armed with his dire warnings (\"Cia, trust no one\"), she bravely heads off to Tosu City, far away from friends and family, perhaps forever. Danger, romance--and sheer terror--await.</p>"
                    "<p>\"The Testing is a chilling and devious dystopian thriller that all fans of The Hunger Games will simply devour. Joelle Charbonneau writes with guts and nerve but also great compassion and heart. Highly recommended.\"--Jonathan Maberry, New York Times bestselling author of Rot & Ruin and Flesh & Bone</p>"
                    "<p>The Testing trilogy is: </p>"
                    "<ul>"
                    "<li>The Testing</li>"
                    "<li>Independent Study</li>"
                    "<li>Graduation Day</li>"
                    "</ul>"
                ),
                'industryIdentifiers': [
                    {'type': 'ISBN_13', 'identifier': '9780547959108'},
                    {'type': 'ISBN_10', 'identifier': '0547959109'}
                ],
                'readingModes': {'text': False, 'image': True},
                'pageCount': 344,
                'printedPageCount': 355,
                'dimensions': {
                    'height': '22.00 cm',
                    'width': '14.00 cm',
                    'thickness': '2.90 cm'
                },
                'printType': 'BOOK',
                'averageRating': 4,
                'ratingsCount': 79,
                'maturityRating': 'NOT_MATURE',
                'allowAnonLogging': False,
                'contentVersion': '0.2.0.0.preview.1',
                'panelizationSummary': {
                    'containsEpubBubbles': False,
                    'containsImageBubbles': False
                },
                'imageLinks': {
                    'smallThumbnail': 'http://books.google.com/books/content?id=CQlnKQbwnEcC&printsec=frontcover&img=1&zoom=5&edge=curl&imgtk=AFLRE72GgqmYupqd5A8az9DaxQGRyh19POLTA6krky60XFkdAVBfQHlmLo-nxnpSrlnDC7zPBwFlCn0jDwWqDsxxyW2rcRWT2vVpoC2KfXLVrX1kOV0pnKYnzNmMRbEaFSp1FI7oCEEp&source=gbs_api',
                    'thumbnail': '...',
                    'small': '...',
                    'medium': '...',
                    'large': '...',
                    'extraLarge': '...'
                },
                'language': 'en',
                'previewLink': 'http://books.google.com/books?id=CQlnKQbwnEcC&hl=&source=gbs_api',
                'infoLink': 'https://play.google.com/store/books/details?id=CQlnKQbwnEcC&source=gbs_api',
                'canonicalVolumeLink': 'https://play.google.com/store/books/details?id=CQlnKQbwnEcC'
            }

        }
        
        signed_in_user = {
            'username': 'existingUser',
            'password': 'somepassword',
        }

        resp = self.client.post(
            "/users/sign_in", data=signed_in_user, follow_redirects=True)

        self.assertEqual(resp.status_code, 200)

        mock_get.return_value.json.return_value = mock_response_data
        with self.app.app_context():
            curr_user = User.query.filter_by(username='existingUser').first()

            response = self.client.post('/save-book', data={
                'google_books_id': 'aJQILlLxRmAC',
                'status': 'previously_read'
            }, follow_redirects=True)
            data = response.get_data(as_text=True)

            book = Book.query.filter_by(google_books_id='aJQILlLxRmAC').first()
            self.assertIsNotNone(book)

            link = UserBooks.query.filter_by(user_id=curr_user.id, book_id=book.id).first()
            self.assertIsNotNone(link)
            self.assertEqual(link.status, 'previously_read')

        self.assertEqual(response.status_code, 200)
        self.assertIn('Currently Reading', data)
        self.assertIn('Previously Read', data)
        self.assertIn('Want To Read', data)
        self.assertIn("Find Your Next Read", data)
        self.assertIn('alt="The Testing"', data)
        self.assertIn('href="/detail/aJQILlLxRmAC"', data)

    
