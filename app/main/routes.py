from flask import Blueprint, render_template
from app.extensions import mongo
from bson import ObjectId

# Create the blueprint object
main = Blueprint("main", __name__)


@main.route("/")
def home():
    # Fetch up to 6 random recipes for Today's suggestions using MongoDB $sample
    try:
        suggestions_cursor = mongo.db.recipes.aggregate([{"$sample": {"size": 6}}])
        suggestions = list(suggestions_cursor)
    except Exception:
        suggestions = []

    # Fetch author names for suggestions
    authors = {}
    user_ids = {r.get('created_by') for r in suggestions if r.get('created_by')}
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

    return render_template("home.html", suggestions=suggestions, authors=authors)
