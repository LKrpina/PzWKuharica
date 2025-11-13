from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_principal import Principal
from flask_bootstrap import Bootstrap5
from app.models.user_model import User
from bson import ObjectId

mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

mail = Mail()
limiter = Limiter(key_func=get_remote_address)
principals = Principal()
bootstrap = Bootstrap5()


@login_manager.user_loader
def load_user(user_id):
    from app.extensions import mongo
    try:
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User(user_data) if user_data else None
    except Exception:
        return None
