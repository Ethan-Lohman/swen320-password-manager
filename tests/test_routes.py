import os
import unittest

# from base_test import BaseTestCase
from flask_testing import TestCase
from web.accounts.models import User
from flask import url_for

from web import app, db
from web.accounts.models import User

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

# Control Flow Testing to cover the paths users can take
class TestRoutes(BaseTestCase):
    def testDecryptionRoute(self):
        self.client.post("/login", data=dict(username="testUser", password="password")) # Logins.
        response = self.client.get("/decrypt") # Sees if it can get the decrypt page.
        self.assertIn(b'Decryption-page', response.data) # Asserts whether the page it is on is the decryption page.

    def testEncryptionRoute(self):
        self.client.post("/login", data=dict(username="testUser", password="password")) # Logins.
        response = self.client.get("/encrypt") # Sees if it can get the decrypt page.
        self.assertIn(b'Encryption-page', response.data) # Asserts whether the page it is on is the encryption page.

    def testListRoute(self):
        self.client.post("/login", data=dict(username="testUser", password="password")) # Logins.
        response = self.client.get("/list") # Sees if it can get the list page.
        self.assertIn(b'List-page', response.data) # Asserts whether the page it is on is the list page.

    def testUpdatePassRoute(self):
        self.client.post("/login", data=dict(username="testUser", password="password")) # Logins.
        response = self.client.get("/updatepass") # Sees if it can get the update password page.
        self.assertIn(b'Updatepass-page', response.data) # Asserts whether the page it is on is the update password page.

    def testLoginToRegisterRoute(self):
        self.client.post("/login", data=dict(username="testUser", password="password")) # Logins.
        response = self.client.get("/encrypt") # Sees if it can get the list page.
        self.assertIn(b'Encryption-page', response.data) # Asserts whether the page it is on is the encryption page.
        response = self.client.get("/logout", follow_redirects=True) # Logsout
        self.assertIn(b'Login-page', response.data) # Asserts whether the page it is on is the login page.
        response = self.client.get("/register", follow_redirects=True) # Logsout
        self.assertIn(b'Register-page', response.data) # Asserts whether the page it is on is the register page.


if __name__ == "__main__":
    unittest.main()