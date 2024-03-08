from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, Length
from web.accounts.models import User


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(message=None), Length(min=5, max=10)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20)])
    token = StringField("Passkey (Token)", validators=[DataRequired(), Length(min=10, max=30)])


    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate(extra_validators=extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True
    
class passwordForm(FlaskForm):
    password = PasswordField("Password text", validators=[DataRequired()])


