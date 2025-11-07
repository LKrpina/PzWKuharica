from flask import Flask
from .extensions import mongo, login_manager, mail, limiter, principals, bootstrap
from .config import Config
from .main.errors import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    principals.init_app(app)
    bootstrap.init_app(app)
    register_error_handlers(app)
    

    from .main.routes import main
    from .auth.routes import auth
    from .recipes.routes import recipes

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(recipes)

    return app