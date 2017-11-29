import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask.ext.restful import abort
from flask.ext.migrate import Migrate
from flask.ext.cors import CORS


app = flask.Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app, resources=r'/*', allow_headers='*')

@app.errorhandler(404)
def not_found(error):
    err = {'message': "Resource doesn't exist.(404)"}
    return flask.jsonify(**err)


# Admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.auth.models import User
from app.club.models import Club
admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Club, db.session))


#from app.blog.resources import blog_bp
from app.club.resources import club_bp
from app.auth.resources import auth_bp
from app.pages.resources import page_bp

#app.register_blueprint(
    #blog_bp,
    #url_prefix='/blog'
#)

app.register_blueprint(
    club_bp,
    url_prefix='/club'
)

app.register_blueprint(
    auth_bp,
    url_prefix='/auth'
)

app.register_blueprint(
    page_bp,
    url_prefix='/page'
)

