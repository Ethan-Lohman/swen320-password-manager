import os
import unittest

from flask_testing import TestCase
from flask import url_for

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
        self.user = User(username="testUser", password="password", token="verygoodtokentohave")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        testdb_path = os.path.join("web", "testdb.sqlite")
        if os.path.exists(testdb_path):
            os.remove(testdb_path)

class TestEncryptedPasswords(BaseTestCase):
    def test_EncryptedPasswordsList(self):
        self.client.post("/login", data=dict(
        username="testUser",
        password="password"
        ), follow_redirects=True)
    
        encrypt_form = EncryptedPasswordForm()
        encrypt_form.key.data = "key1"
        encrypt_form.encrypted_text.data = "text1"
        self.client.post("/save_password", data=encrypt_form.data)

        encrypt_form.key.data = "key2"
        encrypt_form.encrypted_text.data = "text2"
        self.client.post("/save_password", data=encrypt_form.data)

        response = self.client.get("/list")
        self.assertIn(b"key1", response.data)
        self.assertIn(b"text1", response.data)
        self.assertIn(b"key2", response.data)
        self.assertIn(b"text2", response.data)

        self.client.post("/logout", data=dict(
        username="testUser",
        password="password"
        ))


    def test_RemoveEncryptedPassword(self):

        self.client.post("/login", data=dict(
            username="testUser",
            password="password"
        ), follow_redirects=True)



        encrypt_form = EncryptedPasswordForm()
        encrypt_form.key.data = "key1"
        encrypt_form.encrypted_text.data = "text1"
        self.client.post("/save_password", data=encrypt_form.data)


        encrypted_password = EncryptedPassword.query.filter_by(key="key1").first()

        self.client.post(f"/remove_password/{encrypted_password.id}")

        response = self.client.get("/list")
        self.assertNotIn(b"key1", response.data)
        self.assertNotIn(b"text1", response.data)

        self.client.post("/logout", data=dict(
        username="testUser",
        password="password"
        ))


if __name__ == "__main__":
    unittest.main()