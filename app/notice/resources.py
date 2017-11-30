from app import db

from flask import Blueprint, g

from flask_restful import Api, Resource 
from flask.ext.restful import abort, fields, marshal_with, reqparse

from app.base.decorators import login_required, has_permissions
from app.notice.models import Notice

notice_bp = Blueprint('notice_api', __name__)
api = Api(notice_bp)


class NoticeDetail(Resource):

    def get(self, notice_id):
        notice = Notice.query.filter_by(id=notice_id)
        if not notice:
            abort(404, message="Notice {} doesn't exist".format(notice_id))
        serialized_list = list(map(lambda x: x.serialize(), notice))
        return serialized_list


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

