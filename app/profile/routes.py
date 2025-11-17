from flask import render_template, redirect, url_for,flash, request
from flask_login import login_required, current_user
from flask import send_file
from app.extensions import mongo
from bson import ObjectId
from gridfs import GridFS
from . import profile
from .forms import ProfileForm
import io


@profile.route("/profile")
@login_required
def view_profile():
    user = mongo.db.users.find_one({"_id":ObjectId(current_user.id)})
    return render_template("profile.html",user=user)

@profile.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = ProfileForm()
    fs = GridFS(mongo.db)

    user = mongo.db.users.find_one({"_id": ObjectId(current_user.id)})

    if form.validate_on_submit():
        update_data = {
            "name": form.name.data,
            "description": form.description.data,
            "date_of_birth": form.date_of_birth.data.strftime("%Y-%m-%d") if form.date_of_birth.data else None
        }

        if form.profile_image.data:
            image_file = form.profile_image.data
            image_id = fs.put(image_file, filename=image_file.filename, content_type=image_file.content_type)
            update_data["profile_image_id"] = image_id

        mongo.db.users.update_one({"_id": ObjectId(current_user.id)}, {"$set": update_data})

        current_user.name = form.name.data
        current_user.description = form.description.data
        current_user.date_of_birth = form.date_of_birth.data.strftime("%Y-%m-%d") if form.date_of_birth.data else None
        if form.profile_image.data:
            current_user.profile_image_id = image_id

            
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile.view_profile"))

    if request.method == "GET" and user:
        
        form.name.data = user.get("name")
        form.description.data = user.get("description")
        if user.get("date_of_birth"):
            from datetime import datetime
            form.date_of_birth.data = datetime.strptime(user["date_of_birth"], "%Y-%m-%d")
        print("DEBUG: Form name after setting:", form.name.data)
    return render_template("edit_profile.html", form=form, user=user)

@profile.route("/profile/image/<image_id>")
def get_profile_image(image_id):
    fs = GridFS(mongo.db)
    image = fs.get(ObjectId(image_id))
    return send_file(io.BytesIO(image.read()),mimetype=image.content_type)