import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restplus import Api
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
from app.notice.models import Notice
admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Club, db.session))
admin.add_view(ModelView(Notice, db.session))


# Add router
from app.auth.resources import ns as auth_ns
from app.club.resources import ns as club_ns
from app.notice.resources import ns as notice_ns
from app.pages.resources import ns as pages_ns

authorizations = {
    'Authorization': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    title='somoim.space',
    version='0.1',
    description='Backend server',
    prefix='/api/v1',
    authorizations=authorizations
)

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(club_ns, path='/club')
api.add_namespace(notice_ns, path='/notice')
api.add_namespace(pages_ns, path='/page')

api.init_app(app)
