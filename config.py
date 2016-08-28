import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BasicConfig():

    SECRET_KEY = 'HARD TO GUESS'
    FLASK_ADMIN = 'christianyang@wistronits.com'
    FLASKY_POSTS_PER_PAGE = 25

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BasicConfig):

    DEBUG = True
    MAIL_SERVER = 'tpma2001.wistronits.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +\
        os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(BasicConfig):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +\
        os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(BasicConfig):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +\
        os.path.join(basedir, 'data.sqlite')

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    'production': ProductionConfig,
    "default": DevelopmentConfig
}
