from flask_login import UserMixin
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app

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

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def _get_serializer():
        """Dohvaća URLSafeTimedSerializer za generiranje i verifikaciju tokena"""
        secret_key = current_app.config['SECRET_KEY']
        return URLSafeTimedSerializer(secret_key)
    
    @staticmethod
    def _get_collection():
        return current_app.config['USERS_COLLECTION']
    
    @staticmethod
    def verify_email(token):
        serializer = User._get_serializer()
        users_collection = User._get_collection()

        try:
            user_id = serializer.loads(token,max_age=3600)
        except SignatureExpired:
            return None, 'Verifikacijski token je istekao. Molimo zatražite novi verifikacijski email.'
        except BadSignature:
            return None, 'Nevažeći verifikacijski token'
        # Dohvati korisnika
        try:
            user_data = users_collection.find_one({'_id': ObjectId(user_id)})
        except:
            return None, 'Nevažeći verifikacijski token'
        
        if not user_data:
            return None, 'Nevažeći verifikacijski token'
        
        if user_data.get('email_verified', False):
            return None, 'Email adresa je već verificirana'
        
        # Ažuriraj korisnika kao verificiranog
        users_collection.update_one(
            {'_id': user_data['_id']},
            {'$set': {'email_verified': True}}
        )


    def generate_verification_token(self):
        serializer = User._get_serializer()
        return serializer.dumps(self.id)

