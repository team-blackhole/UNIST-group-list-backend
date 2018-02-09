from flask import Blueprint
from flask.ext.restful import abort, fields, marshal_with, reqparse
from flask_restful import Api, Resource
from sqlalchemy import desc

from app import db
from app.base.decorators import login_required
from app.notice.models import Notice

notice_bp = Blueprint('notice_api', __name__)
api = Api(notice_bp)

notice_fields = {
    'id': fields.Integer,
    'created': fields.DateTime,
    'modified': fields.DateTime,
    'title': fields.String,
    'is_shown': fields.Boolean,
    'is_public': fields.Boolean
}


class NoticeDetail(Resource):
    def get(self, notice_id):
        notice = Notice.query.filter_by(id=notice_id)
        if not notice or notice.count() == 0:
            abort(404, message="Notice {} doesn't exist".format(notice_id))
        serialized_list = list(map(lambda x: x.serialize(), notice))
        return serialized_list


class NoticeBase(Resource):
    def get(self):
        notices = Notice.query.order_by(desc(Notice.modified)).limit(10).all()
        print(type(notices))
        if not notices or len(notices) == 0:
            abort(404, message="No notice exists.")
        serialized_list = list(map(lambda x: x.serialize(), notices))
        return serialized_list

    @marshal_with(notice_fields)
    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str)
        parser.add_argument("contents")
        parser.add_argument("is_shown", type=bool)
        parser.add_argument("is_public", type=bool)
        args = parser.parse_args()

        title = args.get('title')
        contents = args.get('contents')
        is_shown = args.get('is_shown')
        is_public = args.get('is_public')

        if title and contents and is_shown and is_public:
            notice = Notice(title=title,
                            contents=contents,
                            is_shown=is_shown,
                            is_public=is_public)
            db.session.add(notice)
            db.session.commit()
            return notice
        else:
            abort(400, message='Not enough fields for register.')


class NoticeList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int)
        parser.add_argument('size', type=int)
        args = parser.parse_args()
        page = args.get("page") or 1
        size = args.get("size") or 3

        notice_list = Notice.query.filter_by(is_shown=True).paginate(page=page, per_page=size).items
        if not notice_list:
            abort(404, message="Notice {} page doesn't exist".format(page))
        serialized_list = list(map(lambda x: x.serialize(), notice_list))
        return serialized_list


api.add_resource(NoticeDetail, '/<notice_id>')
api.add_resource(NoticeList, '/list')
api.add_resource(NoticeBase, '')
