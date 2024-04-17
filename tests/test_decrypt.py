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

if __name__ == "__main__":
    unittest.main()