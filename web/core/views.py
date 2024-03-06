from flask import Blueprint, render_template, request
from flask_login import login_required
from web.accounts.models import User

core_bp = Blueprint("core", __name__)



@core_bp.route("/encrypt", methods=["GET", "POST"])
@login_required
def encrypt():
    if request.method == "POST":
        password_text = request.form['passwordTextE']
        key_text = request.form['key']
        encrypted_text = User.encrypt_password(password_text, key_text)
        return render_template("core/encrypt.html", encrypted_text=encrypted_text)
    return render_template("core/encrypt.html")


@core_bp.route("/decrypt", methods=["GET", "POST"])
@login_required
def decrypt():
    if request.method == "POST":
        encrypt_text = request.form['encryptedTextD']
        decrypted_text = User.decrypt_password(encrypt_text)
        return render_template("core/decrypt.html", decrypted_text=decrypted_text)
    return render_template("core/decrypt.html")


# Starts the Flask app
@core_bp.route("/")
@login_required
def home():
    return render_template("core/index.html")