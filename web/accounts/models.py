from flask_login import UserMixin
from web import db
from crypto.Cipher import Cipher

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=False)
    encryptedPass = db.Column(db.String, nullable=False)
    key = db.Column(db.String, nullable=False)
    encryPassWithKey = db.Column(db.String, nullable=False)

    def __init__(self, username, password, token):
        self.username = username 
        cipher = Cipher()
        enc_text = cipher.encrypt(password)
        key = cipher.encrypt(password)
        self.password = enc_text
        self.token = token
        self.encryptedPass = enc_text
        self.key = key
        self.encryPassWithKey = ''

    def __repr__(self):
        return f"<username {self.username}>" 

    def check_password(self, password):
        cipher = Cipher()
        return cipher.decrypt(self.encryptedPass) == password

    def set_password(self, new_password):
        cipher = Cipher()
        encrypted_password = cipher.encrypt(new_password)
        self.encryptedPass = encrypted_password
        self.password = encrypted_password
        db.session.commit()
        return self.password
    
    def encrypt_password(self, password, key):
        cipher = Cipher()
        encrypted = cipher.encrypt(password, key)
        self.encryptedPass = encrypted
        self.key = key
        return encrypted

    def decrypt_password(self, password):
        cipher = Cipher()
        decrypted = cipher.decrypt(password)
        return decrypted

class EncryptedPassword(db.Model):
    __tablename__ = "encrypted_passwords"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    key = db.Column(db.String, nullable=False)
    encrypted_text = db.Column(db.String, nullable=False)

    user = db.relationship("User", backref=db.backref("encrypted_passwords", lazy="dynamic"))

    def __repr__(self):
        return f"<EncryptedPassword {self.id}: {self.encrypted_text}>"