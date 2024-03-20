from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, ValidationError

class EncryptedPasswordForm(FlaskForm):
    key = StringField('Key', validators=[DataRequired(), Length(max=30)])
    encrypted_text = StringField('Encrypted Text', validators=[DataRequired("Encrypt a Password")])