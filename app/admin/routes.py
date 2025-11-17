from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from bson import ObjectId

from app.extensions import mongo
from . import admin
from .decorators import admin_required


# --------------------------
# ADMIN DASHBOARD
# --------------------------
@admin.route("/")
@login_required
@admin_required
def dashboard():
    total_users = mongo.db.users.count_documents({})
    total_recipes = mongo.db.recipes.count_documents({})
    return render_template("admin/dashboard.html",
                           total_users=total_users,
                           total_recipes=total_recipes)


# --------------------------
# USER LIST
# --------------------------
@admin.route("/users")
@login_required
@admin_required
def users():
    # support searching by username or name (case-insensitive, partial)
    q = request.args.get('q', '').strip()
    query = {}
    if q:
        # search username or name fields
        query = {"$or": [
            {"username": {"$regex": q, "$options": "i"}},
            {"name": {"$regex": q, "$options": "i"}}
        ]}

    all_users = list(mongo.db.users.find(query))
    return render_template("admin/users.html", users=all_users, q=q)


# --------------------------
# TOGGLE ADMIN ROLE
# --------------------------
@admin.route("/users/<user_id>/toggle_admin", methods=["POST"])
@login_required
@admin_required
def toggle_admin(user_id):

    # Prevent removing your own admin role
    if str(current_user.id) == str(user_id):
        flash("You cannot remove admin permissions from yourself.", "danger")
        return redirect(url_for("admin.users"))

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("admin.users"))

    new_status = not user.get("is_admin", False)

    mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_admin": new_status}}
    )

    flash("Admin status updated!", "success")
    return redirect(url_for("admin.users"))


# --------------------------
# DELETE USER (except yourself)
# --------------------------
@admin.route("/users/<user_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):

    if str(current_user.id) == str(user_id):
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("admin.users"))

    mongo.db.users.delete_one({"_id": ObjectId(user_id)})

    flash("User deleted.", "success")
    return redirect(url_for("admin.users"))
