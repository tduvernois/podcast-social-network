import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PHOTO_PATH = os.environ.get('PHOTO_PATH')
    PHOTO_PATH_STATIC = '/static/images/photos'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    USERS_PER_PAGE = int(os.environ.get('USERS_PER_PAGE'))
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

