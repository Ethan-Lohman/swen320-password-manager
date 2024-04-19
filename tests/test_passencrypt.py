import os
import unittest

from flask_testing import TestCase
from flask import url_for, session

from web import app, db
from web.accounts.models import User, EncryptedPassword
from web.accounts.forms import LoginForm, RegisterForm, ChangePasswordForm
from web.core.forms import EncryptedPasswordForm

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

class TestEncrypt(BaseTestCase):
    def test_encryption(self):
        encryptedText = "WCFmZjVnT2pqZSFtTEdFR0ZNWmw0"
        unencryptedText = "Hello"
        form1 = LoginForm(username="testUser", password="password")
        form1.validate()
        response = self.client.get("/login")
        response = self.client.post("/login", data=dict(
            username=form1.username.data,
            password=form1.password.data
        ), follow_redirects=True)
        self.client.get("/encrypt")
        response2 = self.client.post("/encrypt", data=dict(passwordTextE=unencryptedText), follow_redirects=True)
        self.assertIn("encryptedText", response2.data.decode("utf-8"))
        
if __name__ == "__main__":
    unittest.main()