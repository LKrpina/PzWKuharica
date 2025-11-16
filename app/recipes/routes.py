from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
import io
from bson import ObjectId
from gridfs import GridFS
from flask_login import login_required, current_user

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


@recipes.route("/recipes/<recipe_id>")
def recipe_detail(recipe_id):
    from app.models.recipe_model import Recipe

    recipe_data = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    if not recipe_data:
        flash("Recipe not found.", "danger")
        return redirect(url_for("recipes.all_recipes"))
    
    recipe = Recipe(recipe_data)
    return render_template("recipes/recipe_detail.html", recipe=recipe)

@recipes.route("/recipes/image/<image_id>")
def recipe_image(image_id):
    fs = GridFS(mongo.db)
    image = fs.get(ObjectId(image_id))
    return send_file(io.BytesIO(image.read()), mimetype=image.content_type)


@recipes.route("/recipes/<recipe_id>/delete", methods=["POST"])
@login_required
def delete_recipe(recipe_id):
    from app.models.recipe_model import Recipe
    fs = GridFS(mongo.db)

    recipe_data = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    if not recipe_data:
        flash("Recipe not found.", "danger")
        return redirect(url_for("recipes.all_recipes"))

    recipe = Recipe(recipe_data)

    # Permission check: only creator or admin
    if recipe.created_by != current_user.id and not current_user.is_admin:
        flash("You do not have permission to delete this recipe.", "danger")
        return redirect(url_for("recipes.recipe_detail", recipe_id=recipe_id))

    # Delete image from GridFS (if exists)
    if recipe.image_id:
        try:
            fs.delete(ObjectId(recipe.image_id))
        except Exception:
            pass  # ignore if already deleted

    # Delete recipe
    mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})

    flash("Recipe deleted successfully!", "success")
    return redirect(url_for("recipes.all_recipes"))
