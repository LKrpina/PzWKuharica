from flask import Blueprint

recipes = Blueprint("recipes", __name__)

@recipes.route("/recipes")
def all_recipes():
    return "Recipe list (coming soon)"
