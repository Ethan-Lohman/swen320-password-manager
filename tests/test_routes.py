import os
import unittest

from flask_testing import TestCase
from flask import url_for

from web import app, db
from web.accounts.models import User
from base_test import BaseTestCase

class TestRoutes(BaseTestCase):
    def testDecryptionRoute(self):
        self.client.post("/login", data=dict(username="testUser", password="password")) # Logins.
        response = self.client.get("/decrypt") # Sees if it can get the decrypt page.
        self.assertIn(b'Decryption-page', response.data) # Asserts whether the page it is on is the decryption page.

    def testEncryptionRoute(self):
        self.client.post("/login", data=dict(username="testUser", password="password")) # Logins.
        response = self.client.get("/encrypt") # Sees if it can get the decrypt page.
        self.assertIn(b'Encryption-page', response.data) # Asserts whether the page it is on is the encryption page.

if __name__ == "__main__":
    unittest.main()