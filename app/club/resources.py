from flask import request

from flask_restplus import Namespace, Resource, fields  

from app import db
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
        auth_header = request.headers.get('Authorization', 'Token Null')
        token = [item.encode('ascii') for item in auth_header.split(' ')]
        user = User.verify_auth_token(token[1])
        return user
    except:
        return None


class ClubList(Resource):
    parser = ns.parser()
    parser.add_argument('page', type=int)
    parser.add_argument('size', type=int)

    @ns.doc(parser=parser)
    def get(self):
        args = self.parser.parse_args()
        page = args.get("page") or 1
        size = args.get("size") or 3
        club_list = Club.query.filter_by(is_show=True).paginate(page=page, per_page=size).items
        if not club_list:
            ns.abort(404, message="Club doesn't exist")
        serialized_list = list(map(lambda x: x.serialize(), club_list))
        return serialized_list


class ClubBase(Resource):
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
            ns.abort(404, message="Club {} already exist".format(name))
        else:
            club = Club(name=args.get("name"),
                        introduce_one_line=args.get("introduce_one_line"),
                        introduce_all="",
                        manager=user)
            db.session.add(club)
            db.session.commit()
        return club


class ClubDetail(Resource):
    @ns.marshal_with(club_fields)
    def get(self, club_id):
        club = Club.query.filter_by(id=club_id).first()
        if not club:
            ns.abort(404, message="Post {} doesn't exist".format(club_id))
        return club


ns.add_resource(ClubList, '/list')
ns.add_resource(ClubBase, '')
ns.add_resource(ClubDetail, '/<club_id>')
