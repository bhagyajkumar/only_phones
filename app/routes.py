from flask import Blueprint, render_template, request, redirect, url_for
from .models import User
import hashlib
from .ext import db
from flask_login import login_user, logout_user, login_required

view = Blueprint("routes", __name__)

@view.route("/")
def home():
    return render_template("index.html")

@view.route("/call")
def call():
    username = request.args.get("username")
    user = User.query.filter_by(username=username).first()
    return render_template("dial.html", user=user)

@view.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["username"]
        phone = request.form["phone"]
        password = request.form["password"]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User(username=username, phone_number=phone, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("routes.login"))


@view.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user is not None:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if(hashed_password == user.password_hash):
                login_user(user)
                return redirect(url_for("routes.home"))

        return "unable to login"

@view.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("routes.home"))



@view.route("/edit-profile")
@login_required
def edit_profile():
    if request.method == "GET":
        return render_template("edit_profile.html")
