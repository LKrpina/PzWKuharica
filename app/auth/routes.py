from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.extensions import mongo
from app.models.user_model import User
from .forms import RegisterForm, LoginForm
from bson import ObjectId

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = mongo.db.users.find_one({"email": form.email.data.lower()})
        if existing_user:
            flash("Email is already registered.", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = User.hash_password(form.password.data)
        user_data = {
            "name": form.name.data,
            "email": form.email.data.lower(),
            "password_hash": hashed_password,
            "is_admin": False,
            "email_verified": False
        }
        mongo.db.users.insert_one(user_data)
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user_data = mongo.db.users.find_one({"email": form.email.data.lower()})
        if user_data and User(user_data).check_password(form.password.data):
            user = User(user_data)
            login_user(user)
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)

@auth.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))