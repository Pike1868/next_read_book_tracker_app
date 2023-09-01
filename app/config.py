import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    API_KEY = os.environ.get('API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class Testing:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')
    API_KEY = os.environ.get('API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG = True
