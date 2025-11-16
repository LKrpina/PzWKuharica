from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask import send_file
from app.extensions import mongo
from bson import ObjectId
from gridfs import GridFS
from . import profile
from .forms import ProfileForm
from app.models.user_model import User
import io


@profile.route("/profile")
@login_required
def view_profile():
    user = mongo.db.users.find_one({"_id": ObjectId(current_user.id)})
    return render_template("profile.html", user=user)


@profile.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = ProfileForm()

    user_data = mongo.db.users.find_one({"_id": ObjectId(current_user.id)})
    user = User(user_data)
    fs = GridFS(mongo.db)

    if request.method == "GET":
        form.name.data = user.name
        form.description.data = user.description
        form.date_of_birth.data = user.date_of_birth

    if form.validate_on_submit():

        # optional new profile image
        image_id = user.profile_image_id
        if form.image.data:
            if image_id:
                try:
                    fs.delete(ObjectId(image_id))
                except:
                    pass
            img = form.image.data
            image_id = fs.put(img, filename=img.filename, content_type=img.content_type)

        mongo.db.users.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": {
                "name": form.name.data,
                "description": form.description.data,
                "date_of_birth": form.date_of_birth.data,
                "profile_image_id": image_id
            }}
        )

        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile.view_profile"))

    return render_template("profile/edit_profile.html", form=form)

@profile.route("/profile/image/<image_id>")
def profile_image(image_id):
    fs = GridFS(mongo.db)
    image = fs.get(ObjectId(image_id))
    return send_file(io.BytesIO(image.read()), mimetype=image.content_type)


@profile.route("/user/<user_id>")
def public_profile(user_id):
    # You'll need to import User class if you use it here
    from app.models.user_model import User  # Add this import
    
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user_data:
        flash("User not found.", "danger")
        return redirect(url_for("main.home"))

    user = User(user_data)

    # Fetch all recipes by this user
    recipes = list(mongo.db.recipes.find({"created_by": user_id}).sort("created_at", -1))

    return render_template("profile/public_profile.html", user=user, recipes=recipes)