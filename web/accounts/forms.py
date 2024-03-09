from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, Length
from web.accounts.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=10)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20)])
    token = StringField("Passkey (Token)", validators=[DataRequired(), Length(min=10, max=30)])


    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate(extra_validators=extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        return True
    
class passwordForm(FlaskForm):
    password = PasswordField("Password text", validators=[DataRequired()])

class ChangePasswordForm(FlaskForm):
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


