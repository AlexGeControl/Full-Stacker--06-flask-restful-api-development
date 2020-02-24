import os

# root dir of app:
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # security:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    # database:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # pagination:
    FLASK_QUESTIONS_PER_PAGE = 10
    # mail service:
    """
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    """

    @staticmethod
    def init_app(app):
        """ integrate with app factory
        """
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # connect to the database:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'todos-dev.sqlite')
    
    # TODO IMPLEMENT DEV DATABASE URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://udacity:udacity@db:5432/triviaapp'

class TestingConfig(Config):
    TESTING = True
    # database:
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    # database:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'todos.sqlite')
    
    # TODO IMPLEMENT DATABASE URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://udacity:udacity@db:5432/triviaapp'

# configs:
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}