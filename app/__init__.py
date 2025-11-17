from flask import Flask
from .extensions import mongo, login_manager, mail, limiter, principals, bootstrap
from .config import Config
from .main.errors import register_error_handlers
from .profile.routes import profile
from app.admin import admin

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    mongo.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    principals.init_app(app)
    bootstrap.init_app(app)
    register_error_handlers(app)

    # Set USERS_COLLECTION if a default database is available. When using
    # a MongoDB URI without a default database (e.g. a MongoDB Atlas URI
    # that does not include '/mydb' at the end), `mongo.db` may be None
    # and accessing `mongo.db.users` raises AttributeError. Handle that
    # gracefully so the app can start and report the misconfiguration.
    try:
        default_db = getattr(mongo, 'db', None)
        # Database objects do not support truth-value testing; compare with None
        if default_db is not None:
            app.config["USERS_COLLECTION"] = default_db.users
        else:
            app.logger.warning("MongoDB default database not found - check MONGO_URI (missing '/<dbname>')")
            app.config["USERS_COLLECTION"] = None
    except Exception as exc:
        # Log the underlying exception but don't crash the app at startup
        app.logger.warning("Error accessing mongo.db at startup: %s", exc)
        app.config["USERS_COLLECTION"] = None
    

    from .main.routes import main
    from .auth.routes import auth
    from .recipes.routes import recipes

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(recipes)
    app.register_blueprint(profile)
    app.register_blueprint(admin)

    return app