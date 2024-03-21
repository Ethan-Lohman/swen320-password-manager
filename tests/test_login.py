import unittest
from base_test import BaseTestCase
from flask import url_for
from web.accounts.forms import LoginForm, RegisterForm, ChangePasswordForm

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