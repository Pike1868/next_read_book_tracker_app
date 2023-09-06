from unittest import TestCase
from app import create_app, db
from app.models import User


class UserModelTestCase(TestCase):
    """Test user model"""

    def setUp(self):
        """Create test client, add sample data."""
        self.app = create_app('Testing')
        self.client = self.app.test_client()

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        existing_user = User(username="existingUser",
                             password="somepassword",
                             email="existingUser@test.com")
        db.session.add(existing_user)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        db.drop_all()
        self.ctx.pop()

# =======================  Test get signup form ================================

    def test_get_sign_up_form(self):
        """Test that sign up form is displayed"""
        resp = self.client.get("/users/sign_up")
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Sign Up Below", html)
        self.assertIn('href="/users/sign_in"', html)
        self.assertIn('action="/users/sign_up"', html)
        self.assertIn('method="POST"', html)
        self.assertIn("Username", html)
        self.assertIn("Email", html)
        self.assertIn("Password", html)
        self.assertIn("Confirm password", html)

# ======================= Test successful signup ================================

    def test_successful_signup(self):
        """Test if a user can successfully sign up."""

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm': 'testpassword'
        }

        resp = self.client.post("/users/sign_up", data=data, follow_redirects=True)

        self.assertEqual(resp.status_code, 200)

        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

# ======================= Test unsuccessful signup if existing username ================================

    def test_existing_username_signup(self):
        """Test if a user can't sign up with an existing username."""

        data = {
            'username': 'existingUser',
            'email': 'testnew@example.com',
            'password': 'testpassword',
            'confirm': 'testpassword'
        }

        resp = self.client.post("/users/sign_up", data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Username taken, please pick another.", html)

        user_count = User.query.count()
        self.assertEqual(user_count, 1)

# ======================= Test unsuccessful signup if existing email ================================

    def test_existing_email_signup(self):
        """Test if a user can't sign up with an existing email."""

        data = {
            'username': 'SomeNewUser',
            'email': 'existingUser@test.com',
            'password': 'testpassword',
            'confirm': 'testpassword'
        }

        resp = self.client.post("/users/sign_up", data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Email is already is registered, please try logging in.", html)

        user_count = User.query.count()
        self.assertEqual(user_count, 1)


# ======================= Test get sign in form ================================

    def test_get_sign_in_form(self):
        """Test that sign in form is displayed"""
        resp = self.client.get("/users/sign_in")
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Sign In Below", html)
        self.assertIn('href="/users/sign_up"', html)
        self.assertIn('action="/users/sign_in"', html)
        self.assertIn('method="POST"', html)
        self.assertIn("Username", html)
        self.assertIn("Password", html)

# ======================= Test successful user sign in ================================

    def test_successful_sign_in(self):
        """Test if a user can successfully sign in."""

        data = {
            'username': 'existingUser',
            'password': 'somepassword',
        }

        resp = self.client.post(
            "/users/sign_in", data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)

        user = User.query.filter_by(username="existingUser").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "existingUser@test.com")
        self.assertIn('src="/static/images/default-pic.png"', html)


# ======================= Test unsuccessful user sign in ================================

    def test_unsuccessful_sign_in(self):
        """Test if sign in for non existent user will fail, and user is given feedback"""

        data = {
            'username': 'anotheruser',
            'password': 'testpassword',
        }

        resp = self.client.post("/users/sign_in", data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)

        user = User.query.filter_by(username='anotheruser').first()

        self.assertIsNone(user)
        self.assertIn('Incorrect username or password', html)

# ======================= Test user profile page ================================

    def test_display_user_profile(self):
        """Test if the user profile page is displayed correctly after login."""

        signed_in_user = {
            'username': 'existingUser',
            'password': 'somepassword'
        }

        login_resp = self.client.post(
            "/users/sign_in", data=signed_in_user, follow_redirects=True)
        login_html = login_resp.get_data(as_text=True)

        self.assertEqual(login_resp.status_code, 200)
        self.assertIn("Welcome Back, existingUser!", login_html)

        profile_resp = self.client.get("/users/profile", follow_redirects=True)
        profile_html = profile_resp.get_data(as_text=True)

        curr_user = User.query.filter_by(username='existingUser').first()
        print(curr_user)

        self.assertEqual(profile_resp.status_code, 200)
        self.assertIn("existingUser", profile_html)
        self.assertIn(f"{curr_user.email}", profile_html)
        self.assertIn('href="/users/profile/edit"', profile_html)
        self.assertIn('action="/users/delete"', profile_html)

# ======================= Test user edit form is displayed ================================

    def test_display_edit_user_form(self):
        """Test if the user edit form is displayed correctly"""

        signed_in_user = {
            'username': 'existingUser',
            'password': 'somepassword'
        }

        login_resp = self.client.post(
            "/users/sign_in", data=signed_in_user, follow_redirects=True)

        self.assertEqual(login_resp.status_code, 200)

        edit_form_resp = self.client.get(
            "/users/profile/edit", follow_redirects=True)
        edit_form_html = edit_form_resp.get_data(as_text=True)

        self.assertEqual(login_resp.status_code, 200)
        self.assertIn("Username", edit_form_html)
        self.assertIn("E-mail", edit_form_html)
        self.assertIn("Bio", edit_form_html)
        self.assertIn("Location", edit_form_html)
        self.assertIn("(Optional) Image URL", edit_form_html)
        self.assertIn("To confirm changes, enter your password:",
                      edit_form_html)

# ======================= Test user edit form is processed correctly ================================

    def test_successful_user_edit(self):
        """Test if a user can successfully edit their profile."""

        signed_in_user = {
            'username': 'existingUser',
            'password': 'somepassword'
        }

        login_resp = self.client.post(
            "/users/sign_in", data=signed_in_user, follow_redirects=True)

        self.assertEqual(login_resp.status_code, 200)
        new_data = {
            'username': 'updatedUser',
            'email': 'updatedUser@test.com',
            'bio': 'Updated bio',
            'location': 'Updated location',
            'image_url': 'http://example.com/updated.jpg',
            'password': 'somepassword'
        }

        resp = self.client.post(
            "/users/profile/edit", data=new_data, follow_redirects=True)
        print(resp)
        html = resp.get_data(as_text=True)

        updated_user = User.query.filter_by(username='updatedUser').first()

        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.email, 'updatedUser@test.com')
        self.assertEqual(updated_user.bio, 'Updated bio')
        self.assertEqual(updated_user.location, 'Updated location')
        self.assertEqual(updated_user.image_url,
                         'http://example.com/updated.jpg')
        self.assertIn("Profile updated successfully", html)


# ======================= Test unsuccessful user edit form submission ================================

    def test_unsuccessful_user_edit(self):
        """Test user is not updated and that edit form displays feedback if password is incorrect"""

        signed_in_user = {
            'username': 'existingUser',
            'password': 'somepassword'
        }

        login_resp = self.client.post(
            "/users/sign_in", data=signed_in_user, follow_redirects=True)

        self.assertEqual(login_resp.status_code, 200)
        new_data = {
            'username': 'updatedUser',
            'email': 'updatedUser@test.com',
            'bio': 'Updated bio',
            'location': 'Updated location',
            'image_url': 'http://example.com/updated.jpg',
            'password': 'wrongpassword'
        }

        resp = self.client.post(
            "/users/profile/edit", data=new_data, follow_redirects=True)
        print(resp)
        html = resp.get_data(as_text=True)

        updated_user = User.query.filter_by(username='updatedUser').first()
        curr_user = User.query.filter_by(username='existingUser').first()

        self.assertIsNone(updated_user)
        self.assertIsNotNone(curr_user)
        self.assertEqual(curr_user.username, "existingUser")
        self.assertIsNone(curr_user.bio)
        self.assertIn("Username", html)
        self.assertIn("E-mail", html)
        self.assertIn("Bio", html)
        self.assertIn("Location", html)
        self.assertIn("(Optional) Image URL", html)
        self.assertIn("To confirm changes, enter your password:", html)
        self.assertIn(
            "Incorrect password. Please enter your correct password to confirm changes.", html)


# ======================= Test user can successfully sign out ================================

    def test_successful_sign_out(self):
        """Test if a user can successfully sign out."""

        signed_in_user = {
            'username': 'existingUser',
            'password': 'somepassword'
        }

        sign_in_resp = self.client.post("/users/sign_in", data=signed_in_user)
        self.assertEqual(sign_in_resp.status_code, 302)

        sign_out_resp = self.client.post(
            "/users/sign_out", follow_redirects=True)
        sign_out_html = sign_out_resp.get_data(as_text=True)
        print(sign_out_html)

        self.assertEqual(sign_out_resp.status_code, 200)
        self.assertIn("Goodbye!", sign_out_html)
        self.assertIn('href="/users/sign_in"', sign_out_html)
        self.assertIn('href="/users/sign_up"', sign_out_html)

# ======================= Test unsuccessful user edit form submission ================================

    def test_successful_user_delete(self):
        """Test user is successfully deleted"""

        signed_in_user = {
            'username': 'existingUser',
            'password': 'somepassword'
        }

        login_resp = self.client.post(
            "/users/sign_in", data=signed_in_user, follow_redirects=True)
        
        curr_user = User.query.filter_by(username="existingUser").first()

        self.assertEqual(login_resp.status_code, 200)
        self.assertIsNotNone(curr_user)

        del_resp = self.client.post("/users/delete", follow_redirects=True)
        html = del_resp.get_data(as_text=True)

        curr_user = User.query.filter_by(username="existingUser").first()
        
        self.assertEqual(del_resp.status_code, 200)
        self.assertIsNone(curr_user)
        self.assertIn("Your account has been deleted.", html)
        self.assertIn("Find Your Next Read", html)
        self.assertIn('href="/users/sign_in"', html)
        self.assertIn('href="/users/sign_up"', html)
