from datetime import datetime
from bson import ObjectId
from app.extensions import mongo

class Recipe:
    def __init__(self,data):
        self.id = str(data.get("_id"))
        self.title = data.get("title")
        self.description = data.get("description")
        self.description_html = data.get("description_html")
        self.category = data.get("category")
        self.image_id = data.get("image_id")
        self.created_by = data.get("created_by")
        self.created_at = data.get("created_at", datetime.now)

        user = mongo.db.users.find_one({"_id": ObjectId(self.created_by)})
        self.creator_name = user.get("name") if user else "Unknown"
    
    @staticmethod
    def from_id(collection,recipe_id):
        data = collection.find_one({"_id": ObjectId(recipe_id)})
        return Recipe(data) if data else None
    
        
