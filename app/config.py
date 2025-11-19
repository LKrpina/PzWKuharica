import os
from dotenv import load_dotenv


load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "supertajnikljuc")
    
    SESSION_COOKIE_NAME = "session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False 
    REMEMBER_COOKIE_DURATION = 86400
    SESSION_PERMANENT = False

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydatabase")

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() in ('true', '1', 'yes')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', None)
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', None)
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@unizd-oglasnik.hr')
    # Timeout postavke za Render (Render blokira odlazne konekcije na određene portove)
    MAIL_TIMEOUT = int(os.getenv('MAIL_TIMEOUT', 10))
    MAIL_SUPPRESS_SEND = os.getenv('MAIL_SUPPRESS_SEND', 'False').lower() in ('true', '1', 'yes')

    USERS_COLLECTION = None 
    

    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    RATELIMIT_STRATEGY = "fixed-window"


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
