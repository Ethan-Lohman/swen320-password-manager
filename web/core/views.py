from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from web.accounts.models import User, EncryptedPassword
from web import db
from web.accounts.forms import LoginForm, RegisterForm
from web.core.forms import EncryptedPasswordForm

core_bp = Blueprint("core", __name__)

@core_bp.route("/encrypt", methods=["GET", "POST"])
@login_required
def encrypt():
    form = EncryptedPasswordForm()
    if request.method == "POST":
        password_text = request.form.get('passwordTextE')
        key_text = request.form.get('key')
        user = User.query.filter_by(username=current_user.username).first()
        if user: 
            encrypted_text = user.encrypt_password(password_text, key_text)
            return render_template("core/encrypt.html", encrypted_text=encrypted_text, form=form)
        else: 
            flash("User not found or not logged in.", "error")
            return redirect(url_for("auth.login"))
    return render_template("core/encrypt.html", form=form)

@core_bp.route("/decrypt", methods=["GET", "POST"])
@login_required
def decrypt():
    if request.method == "POST":
        encrypt_text = request.form.get('encryptedTextD') 
        user = User.query.filter_by(username=current_user.username).first()
        if user:
            decrypted_text = user.decrypt_password(encrypt_text)
            return render_template("core/decrypt.html", decrypted_text=decrypted_text)
        else:
            flash("User not found or not logged in.", "error")
            return redirect(url_for("auth.login"))
    return render_template("core/decrypt.html")

@core_bp.route("/save_password", methods=["GET", "POST"])
@login_required
def save_password():
    form = EncryptedPasswordForm()

    if form.validate_on_submit():
        key = form.key.data
        encrypted_text = form.encrypted_text.data

        existing_password = EncryptedPassword.query.filter_by(user_id=current_user.id, key=key).first()

        if existing_password:
            existing_password.encrypted_text = encrypted_text
            db.session.commit()
            flash("Encrypted password updated successfully.", "success")
        else:
            encrypted_password = EncryptedPassword(
                user_id=current_user.id,
                key=key,
                encrypted_text=encrypted_text
            )

            db.session.add(encrypted_password)
            db.session.commit()
            flash("Encrypted password saved successfully.", "success")

        return redirect(url_for("core.list"))

    return render_template("core/encrypt.html", form=form)

@core_bp.route("/remove_password/<int:password_id>", methods=["POST"])
@login_required
def remove_password(password_id):
    encrypted_password = EncryptedPassword.query.get(password_id)

    if encrypted_password and encrypted_password.user_id == current_user.id:
        db.session.delete(encrypted_password)
        db.session.commit()
        flash("Encrypted password removed successfully.", "success")
    else:
        flash("Error: Unable to remove the encrypted password.", "error")

    return redirect(url_for("core.list"))

@core_bp.route("/list")
@login_required
def list():
    encrypted_passwords = EncryptedPassword.query.filter_by(user_id=current_user.id).all()
    return render_template("core/list.html", encrypted_passwords=encrypted_passwords)

@core_bp.route("/")
@login_required
def home():
    form = EncryptedPasswordForm()
    return render_template("core/encrypt.html", form=form)
