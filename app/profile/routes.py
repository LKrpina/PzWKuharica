from flask import render_template, redirect, url_for,flash, request
from flask_login import login_required, current_user
from app.extensions import mongo
from . import profile


@profile.route("/profile")
@login_required
def view_profile():
    user = mongo.db.users.find_one({"_id":current_user.id})
    return render_template("profile.html",user=user)

@profile.route("/profile/edit", methods=["GET","POST"])
@login_required
def edit_profile():
    flash("Profile editing coming soon!", "info")
    return redirect(url_for("profile.view_profile"))