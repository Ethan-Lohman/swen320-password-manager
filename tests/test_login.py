import os
import unittest

from flask_testing import TestCase
from flask import url_for

from web import app, db
from web.accounts.models import User
from web.accounts.forms import LoginForm, RegisterForm, ChangePasswordForm

class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object("config.TestingConfig")
        return app

    def setUp(self):
        db.create_all()
        user = User(username="testUser", password="password", token="verygoodtokentohave")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        testdb_path = os.path.join("web", "testdb.sqlite")
        if os.path.exists(testdb_path):
            os.remove(testdb_path)

# Test the login form to see if it returns an error and if it logins correctly.
class TestLogin(BaseTestCase):
    def test_invalidUsernameLogin(self):
        # Create an instance of the LoginForm with invalid credentials
        form1 = LoginForm(username="testUse", password="password")
        
        # Call validate() to trigger form validation
        form1.validate()

        # Send a GET request to the login route to get the form
        response = self.client.get("/login")

        # Send a POST request to the login route with the form data
        response = self.client.post("/login", data=dict(
            username=form1.username.data,
            password=form1.password.data
        ), follow_redirects=True)

        # Assert that the expected flash message appears in the response
        self.assertIn(b'Invalid username and/or password.', response.data)

    def test_invalidPasswordLogin(self):
        # Create an instance of the LoginForm with invalid credentials
        form1 = LoginForm(username="testUser", password="passwor")
        
        # Call validate() to trigger form validation
        form1.validate()

        # Send a GET request to the login route to get the form
        response = self.client.get("/login")

        # Send a POST request to the login route with the form data
        response = self.client.post("/login", data=dict(
            username=form1.username.data,
            password=form1.password.data
        ), follow_redirects=True)

        # Assert that the expected flash message appears in the response
        self.assertIn(b'Invalid username and/or password.', response.data)

    def test_validLogin(self):
        # Create an instance of the LoginForm with invalid credentials
        form1 = LoginForm(username="testUser", password="password")
        
        # Call validate() to trigger form validation
        form1.validate()

        # Send a GET request to the login route to get the form
        response = self.client.get("/login")

        # Send a POST request to the login route with the form data
        response = self.client.post("/login", data=dict(
            username=form1.username.data,
            password=form1.password.data
        ), follow_redirects=True)

        response = self.client.get("/decrypt") # Sees if it can get the decrypt page.
        self.assertIn(b'Decryption-page', response.data) # Asserts whether the page it is on is the decryption page.

if __name__ == "__main__":
    unittest.main()