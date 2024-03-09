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

class TestRoutes(BaseTestCase):
    def testDecryptionRoute(self):
        self.client.post("/login", data=dict(username="testUser", password="password")) # Logins.
        response = self.client.get("/decrypt") # Sees if it can get the decrypt page.
        self.assertIn(b'Decryption-page', response.data) # Asserts whether the page it is on is the decryption page.

    def testEncryptionRoute(self):
        self.client.post("/login", data=dict(username="testUser", password="password")) # Logins.
        response = self.client.get("/encrypt") # Sees if it can get the decrypt page.
        self.assertIn(b'Encryption-page', response.data) # Asserts whether the page it is on is the encryption page.

class TestRegisterForm(BaseTestCase):
    # Boundary Value Test for Username (Amount of characters) {4, 5, 6, 7, 9, 10, 11}
    def testInvalidUsername(self):
        form1 = RegisterForm(username="boba", password="password", token="verygoodtokentohave")
        form2 = RegisterForm(username="12345678911", password="password", token="verygoodtokentohave")
        self.assertFalse(form1.validate())
        self.assertFalse(form2.validate())

    def testValidUsername(self):
        form1 = RegisterForm(username="12345", password="password", token="verygoodtokentohave")
        form2 = RegisterForm(username="123456", password="password", token="verygoodtokentohave")
        form3 = RegisterForm(username="1234567", password="password", token="verygoodtokentohave")
        form4 = RegisterForm(username="123456789", password="password", token="verygoodtokentohave")
        form5 = RegisterForm(username="1234567891", password="password", token="verygoodtokentohave")
        self.assertTrue(form1.validate())
        self.assertTrue(form2.validate())
        self.assertTrue(form3.validate())
        self.assertTrue(form4.validate())
        self.assertTrue(form5.validate())

    # Boundary Value Test for Password (Amount of characters) {7, 8, 9, 15, 19, 20, 21}
    def testInvalidPassword(self):
        form1 = RegisterForm(username="validuser", password="1234567", token="verygoodtokentohave") #7
        form2 = RegisterForm(username="validuser", password="123456789012345678901", token="verygoodtokentohave") #21
        self.assertFalse(form1.validate())
        self.assertFalse(form2.validate())

    def testValidPassword(self):
        form1 = RegisterForm(username="validuser", password="12345678", token="verygoodtokentohave") # 8
        form2 = RegisterForm(username="validuser", password="123456789", token="verygoodtokentohave") # 9
        form3 = RegisterForm(username="validuser", password="123456789012345", token="verygoodtokentohave") # 15
        form4 = RegisterForm(username="validuser", password="1234567890123456789", token="verygoodtokentohave") # 19
        form5 = RegisterForm(username="validuser", password="12345678901234567890", token="verygoodtokentohave") # 20
        self.assertTrue(form1.validate())
        self.assertTrue(form2.validate())
        self.assertTrue(form3.validate())
        self.assertTrue(form4.validate())
        self.assertTrue(form5.validate())


    # Boundary Value Test for Token (Amount of characters) {9, 10, 11, 20, 29, 30, 31}
    def testInvalidToken(self):
        form1 = RegisterForm(username="validuser", password="validpassword", token="123456789") # 9
        form2 = RegisterForm(username="validuser", password="validpassword", token="1234567890123456790123456789012") # 31
        self.assertFalse(form1.validate())
        self.assertFalse(form2.validate())

    def testValidToken(self):
        form1 = RegisterForm(username="validuser", password="validpassword", token="1234567891") # 10
        form2 = RegisterForm(username="validuser", password="validpassword", token="12345678911") # 11
        form3 = RegisterForm(username="validuser", password="validpassword", token="123456789012345312") # Midpoint somewhere
        form4 = RegisterForm(username="validuser", password="validpassword", token="12345678901234567890123456789") # 29
        form5 = RegisterForm(username="validuser", password="validpassword", token="123456789012345678901234567890") # 30
        self.assertTrue(form1.validate())
        self.assertTrue(form2.validate())
        self.assertTrue(form3.validate())
        self.assertTrue(form4.validate())
        self.assertTrue(form5.validate())


if __name__ == "__main__":
    unittest.main()