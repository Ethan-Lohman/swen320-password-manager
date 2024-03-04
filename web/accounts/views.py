from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user, login_required, logout_user
from web import db
from web.accounts.models import User
from .forms import LoginForm, RegisterForm
from crypto.Cipher import Cipher 

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You're account has been registered.", "info")
        return redirect(url_for("core.home"))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data, token=form.token.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Welcome!", "success")
        return redirect(url_for("core.home"))
    
    return render_template("accounts/register.html", form=form)

@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data): # Add password check
            login_user(user)
            return redirect(url_for("core.home"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template("accounts/login.html", form=form)


@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))


@accounts_bp.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    return render_template("accounts/encrypt.html")



@accounts_bp.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    return render_template("accounts/decrypt.html")
