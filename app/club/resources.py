from flask import request, g
from flask_restplus import Namespace, Resource, fields
from sqlalchemy import desc

from app import db
from app.auth.models import User
from app.base.decorators import login_required
from app.club.models import Club

ns = Namespace('Club', description='Club api')

club_fields = ns.model('club_fields', {
    'id': fields.Integer,
    'created': fields.DateTime,
    'modified': fields.DateTime,
    'name': fields.String,
    'introduce_one_line': fields.String,
    'introduce_all': fields.String,
    'manager': fields.Raw
})

list_fields = ns.model('list_fields', {
    'id': fields.Integer,
    'created': fields.DateTime,
    'modified': fields.DateTime,
    'name': fields.String,
    'slug': fields.String,
})


def get_user_from_token():
    try:
        token = request.headers.get('Authorization', 'Null')
        user = User.verify_auth_token(token)
        return user
    except:
        return None


class ClubBase(Resource):
    @staticmethod
    def get_clubs():
        clubs = Club.query.order_by(desc(Club.modified))

        # check if signed in
        if hasattr(g, 'user'):
            user = g.user
        else:
            user = get_user_from_token()
        if not user:
            return clubs.filter_by(is_shown=True)

        # check if the user is admin
        if user.has_permission('admin'):
            return clubs

        a = clubs.filter(Club.is_shown | (Club.manager.contains(user)))
        return a


class ClubPost(ClubBase):
    parser = ns.parser()
    parser.add_argument("name", type=str, location='form')
    parser.add_argument("introduce_one_line", type=str, location='form')

    @ns.marshal_with(club_fields)
    @login_required
    @ns.doc(parser=parser)
    def post(self):
        args = self.parser.parse_args()
        club = Club.query.filter_by(name=args.get("name")).first()
        user = get_user_from_token()

        if club:
            ns.abort(404, message="Club {} already exist".format(args.get("name")))
        else:
            club = Club(name=args.get("name"),
                        introduce_one_line=args.get("introduce_one_line"),
                        introduce_all="",
                        manager=user)
            db.session.add(club)
            db.session.commit()
        return club.serialize()


class ClubList(ClubBase):
    parser = ns.parser()
    parser.add_argument('page', type=int)
    parser.add_argument('size', type=int)

    @ns.doc(parser=parser)
    def get(self):
        args = self.parser.parse_args()
        page = args.get("page") or 1
        size = args.get("size") or 3
        club_list = self.get_clubs().paginate(page=page, per_page=size).items
        if not club_list:
            ns.abort(404, message="Club doesn't exist")
        serialized_list = list(map(lambda x: x.serialize(), club_list))
        return serialized_list


class ClubDetail(ClubBase):
    @ns.marshal_with(club_fields)
    def get(self, club_id):
        club = self.get_clubs().filter_by(id=club_id).first()
        if not club:
            ns.abort(404, message="Post {} doesn't exist".format(club_id))
        serialized_club = club.serialize()
        return serialized_club


ns.add_resource(ClubList, '/list')
ns.add_resource(ClubPost, '')
ns.add_resource(ClubDetail, '/<club_id>')
