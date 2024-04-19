from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user, login_required, logout_user
from web import db
from web.accounts.models import User
from .forms import LoginForm, RegisterForm, ChangePasswordForm
from crypto.Cipher import Cipher 

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Your account has been registered.", "info")
        return redirect(url_for("core.home"))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, token=form.token.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Welcome!", "success")
        return redirect(url_for("core.home"))
    
    return render_template("accounts/register.html", form=form)

@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    success = False
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):  # Add password check
            login_user(user)
            success = True
            return redirect(url_for("core.home"))
        else:
            flash("Invalid username and/or password.", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template("accounts/login.html", form=form, success=success)

@accounts_bp.route("/logout")
@login_required
def logout():
    db.session.commit()
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))

@accounts_bp.route("/updatepass", methods=["GET", "POST"])
@login_required
def updatepass():
    form = ChangePasswordForm()
    success = False
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        if user:
            user.set_password(form.newPassword.data)  # Update the password
            db.session.commit()
            flash("Password updated successfully!", "success")
            success = True
        else:
            flash("User not found.", "danger")
    return render_template("accounts/updatepass.html", form=form, success=success)