CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
DEBUG = True

import os
basedir = os.path.abspath(os.path.dirname(__file__))
sijax_path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SIJAX_STATIC_PATH = sijax_path
SIJAX_JSON_URI = '/static/js/sijax/json2.js'