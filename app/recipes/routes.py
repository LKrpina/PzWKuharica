from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from bson import ObjectId
from gridfs import GridFS

from app.extensions import mongo
from app.markdown_utils import markdown_to_html
from .forms import RecipeForm

recipes = Blueprint("recipes", __name__)

@recipes.route("/recipes")
def all_recipes():
    recipes_list = list(mongo.db.recipes.find().sort("created_at", -1))
    return render_template("recipes/all_recipes.html", recipes = recipes_list)

@recipes.route("/recipes/new", methods=["GET", "POST"])
@login_required
def new_recipe():
    form = RecipeForm()
    fs = GridFS(mongo.db)

    if form.validate_on_submit():

        markdown_text = form.description.deta
        html_text = markdown_to_html(markdown_text)

        image_id = None
        if form.image.data:
            image_file = form.image.data
            image_id = fs.put(
                image_file,
                filename = image_file.filename,
                content_type=image_file.content_type
            )

        mongo.db.recipes.insert_one({
            "title": form.title.data,
            "description": markdown_text,
            "description_html": html_text,
            "category": form.category.data,
            "image_id": image_id,
            "created_by": current_user.id,
            "created_at": mongo.db.command("serverStatus")["localTime"],
        })

        flash("Your recipe was published!", "success")
        return redirect(url_for("recipes.all_recipes"))
    
    return render_template("recipes/new_recipe.html", form=form)