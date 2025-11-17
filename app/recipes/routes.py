from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, abort
import io
from bson import ObjectId
from bson.errors import InvalidId
from gridfs import GridFS
from flask_login import login_required, current_user

from app.extensions import mongo
from app.markdown_utils import markdown_to_html

from .forms import RecipeForm

recipes = Blueprint("recipes", __name__)

@recipes.route("/recipes")
def all_recipes():
    # Query params
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    PER_PAGE = 6

    # Build filter
    query = {}
    if q:
        # search in title or description (case-insensitive)
        query['$or'] = [
            {'title': {'$regex': q, '$options': 'i'}},
            {'description': {'$regex': q, '$options': 'i'}}
        ]
    if category:
        query['category'] = category

    total = mongo.db.recipes.count_documents(query)
    skip = (page - 1) * PER_PAGE

    recipes_list = list(mongo.db.recipes.find(query).sort('created_at', -1).skip(skip).limit(PER_PAGE))

    # Fetch author names for displayed recipes
    user_ids = {r.get('created_by') for r in recipes_list if r.get('created_by')}
    authors = {}
    if user_ids:
        object_ids = []
        for uid in user_ids:
            try:
                object_ids.append(ObjectId(uid))
            except Exception:
                pass
        if object_ids:
            users_cursor = mongo.db.users.find({'_id': {'$in': object_ids}})
            for u in users_cursor:
                authors[str(u.get('_id'))] = u.get('name') or u.get('email')

    # Distinct categories for filter dropdown
    categories = mongo.db.recipes.distinct('category')

    # Pagination meta
    total_pages = (total + PER_PAGE - 1) // PER_PAGE

    return render_template(
        "recipes/all_recipes.html",
        recipes=recipes_list,
        authors=authors,
        page=page,
        total_pages=total_pages,
        q=q,
        category=category,
        categories=sorted([c for c in categories if c]),
        total=total,
        per_page=PER_PAGE,
    )

@recipes.route("/recipes/new", methods=["GET", "POST"])
@login_required
def new_recipe():
    form = RecipeForm()
    fs = GridFS(mongo.db)

    if form.validate_on_submit():

        markdown_text = form.description.data
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
    # Validate recipe_id and return 404 if invalid or missing
    try:
        oid = ObjectId(recipe_id)
    except InvalidId:
        abort(404)

    recipe_data = mongo.db.recipes.find_one({"_id": oid})
    if not recipe_data:
        abort(404)

    recipe = Recipe(recipe_data)
    # Fetch author data
    author_name = None
    try:
        if recipe.created_by:
            author_doc = mongo.db.users.find_one({"_id": ObjectId(recipe.created_by)})
            if author_doc:
                author_name = author_doc.get('name') or author_doc.get('email')
    except Exception:
        author_name = None

    return render_template("recipes/recipe_detail.html", recipe=recipe, author_name=author_name)

@recipes.route("/recipes/image/<image_id>")
def recipe_image(image_id):
    fs = GridFS(mongo.db)
    # Validate image id and handle missing files with 404
    try:
        oid = ObjectId(image_id)
    except InvalidId:
        abort(404)

    try:
        image = fs.get(oid)
    except Exception:
        abort(404)

    return send_file(io.BytesIO(image.read()), mimetype=image.content_type)


@recipes.route("/recipes/<recipe_id>/delete", methods=["POST"])
@login_required
def delete_recipe(recipe_id):
    from app.models.recipe_model import Recipe
    fs = GridFS(mongo.db)
    # Validate recipe id
    try:
        oid = ObjectId(recipe_id)
    except InvalidId:
        abort(404)

    recipe_data = mongo.db.recipes.find_one({"_id": oid})
    if not recipe_data:
        abort(404)

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
    mongo.db.recipes.delete_one({"_id": oid})

    flash("Recipe deleted successfully!", "success")
    return redirect(url_for("recipes.all_recipes"))


@recipes.route("/recipes/<recipe_id>/edit", methods=["GET","POST"])
@login_required
def edit_recipe(recipe_id):
    from app.models.recipe_model import Recipe
    fs = GridFS(mongo.db)
    # Validate recipe id
    try:
        oid = ObjectId(recipe_id)
    except InvalidId:
        abort(404)

    recipe_data = mongo.db.recipes.find_one({"_id": oid})
    if not recipe_data:
        abort(404)
    
    recipe = Recipe(recipe_data)


    if recipe.created_by != current_user.id and not current_user.is_admin:
        flash("You do not have permission to edit this recipe.", "danger")
        return redirect(url_for("recipes.recipe_detail", recipe_id=recipe_id))
    
    form = RecipeForm(
        title = recipe.title,
        description = recipe.description,
        category = recipe.category
    )

    if form.validate_on_submit():

        markdown_text = form.description.data
        html_text = markdown_to_html(markdown_text)

        image_id = recipe.image_id
        if form.image.data:
            if image_id:
                try:
                    fs.delete(ObjectId(image_id))
                except:
                    pass

            image_file = form.image.data
            image_id = fs.put(
                image_file,
                filename=image_file.filename,
                content_type=image_file.content_type
            )
        
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)},
            {"$set": {
                "title": form.title.data,
                "description": markdown_text,
                "description_html": html_text,
                "category": form.category.data,
                "image_id": image_id
            }}
        )

        flash("Your recipe has been updated!", "success")
        return redirect(url_for("recipes.recipe_detail", recipe_id=recipe_id))
    
    return render_template("recipes/edit_recipe.html", form=form, recipe=recipe)