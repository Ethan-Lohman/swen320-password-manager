from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from web.accounts.models import User
from web.accounts.forms import LoginForm, RegisterForm

core_bp = Blueprint("core", __name__)

@core_bp.route("/encrypt", methods=["GET", "POST"])
@login_required
def encrypt():
    if request.method == "POST":
        password_text = request.form.get('passwordTextE')
        key_text = request.form.get('key')
        user = User.query.filter_by(email=current_user.email).first()
        if user: 
            encrypted_text = user.encrypt_password(password_text, key_text)
            return render_template("core/encrypt.html", encrypted_text=encrypted_text)
        else: 
            flash("User not found or not logged in.", "error")
            return redirect(url_for("auth.login"))
    return render_template("core/encrypt.html")


@core_bp.route("/decrypt", methods=["GET", "POST"])
@login_required
def decrypt():
    if request.method == "POST":
        encrypt_text = request.form.get('encryptedTextD') 
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            decrypted_text = user.decrypt_password(encrypt_text)
            return render_template("core/decrypt.html", decrypted_text=decrypted_text)
        else:
            flash("User not found or not logged in.", "error")
            return redirect(url_for("auth.login"))
    return render_template("core/decrypt.html")



# Starts the Flask app
@core_bp.route("/")
@login_required
def home():
    return render_template("core/encrypt.html")
    
@core_bp.route("/list")
def list():
    return render_template("core/list.html")