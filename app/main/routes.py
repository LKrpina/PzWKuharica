from flask import Blueprint, render_template

# Create the blueprint object
main = Blueprint("main", __name__)

@main.route("/")
def home():
    return "Hello, Cooking App!"
