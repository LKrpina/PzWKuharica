from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_principal import Principal
from flask_bootstrap import Bootstrap5

mongo = PyMongo()
login_manager = LoginManager()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)
principals = Principal()
bootstrap = Bootstrap5()

# Temporary fix for login_manager
@login_manager.user_loader
def load_user(user_id):
    return None  # We'll implement this properly later

