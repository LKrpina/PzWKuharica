from flask_login import UserMixin
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin):
    def __init__(self, data):
        self.id = str(data.get("_id"))
        self.name = data.get("name")
        self.email = data.get("email")
        self.password_hash = data.get("password_hash")
        self.is_admin = data.get("is_admin", False)
        self.profile_image_id = data.get("profile_image_id")
        self.description = data.get("description")
        self.date_of_birth = data.get("date_of_birth")
        self.email_verified = data.get("email_verified", False)
        self.created_at = data.get("created_at", datetime.utcnow())

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
