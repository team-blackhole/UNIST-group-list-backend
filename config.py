import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite')
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

# noinspection SpellCheckingInspection
SECRET_KEY = "9oup6z5mjbw)8(f5$9ob1m&jha*(5ulqot&x*y1n$1^^9qo#d-"

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False
