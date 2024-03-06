from flask import Blueprint, render_template
from flask_login import login_required

core_bp = Blueprint("core", __name__)

# Starts the Flask app
@core_bp.route("/")
@login_required
def home():
    return render_template("core/encrypt.html")
@core_bp.route("/list")
def list():
    return render_template("core/list.html")
@core_bp.route("/encrypt")
def encrypt():
    return render_template("core/encrypt.html")
@core_bp.route("/decrypt")
def decrypt():
    return render_template("core/decrypt.html")