from flask_restplus import Namespace, Resource, fields

from app import db
from app.base.decorators import login_required
from app.pages.models import Page

ns = Namespace('Pages', description='Pages Board - incomplete')

page_fields = ns.model('page_fields', {
    'id': fields.Integer,
    'created': fields.DateTime,
    'modified': fields.DateTime,
    'title': fields.String,
    'content': fields.String,
    'slug': fields.String,
})

list_fields = ns.model('list_fields', {
    'id': fields.Integer,
    'title': fields.String,
    'slug': fields.String,
})

parser = ns.parser()
parser.add_argument('title', type=str)
parser.add_argument('content', type=str)


class PageDetail(Resource):
    @ns.marshal_with(page_fields)
    def get(self, slug):
        page = Page.query.filter_by(slug=slug).first()
        if not page:
            ns.abort(404, message="Page {} doesn't exist".format(slug))
        return page

    @login_required
    def delete(self, slug):
        page = Page.query.filter_by(slug=slug).first()
        if not page:
            ns.abort(404, message="Page {} doesn't exist".format(slug))
        db.session.delete(page)
        db.session.commit()
        return {}, 204

    @ns.marshal_with(page_fields)
    @login_required
    def put(self, slug):
        parsed_args = parser.parse_args()
        page = Page.query.filter_by(slug=slug).first()
        if not page:
            ns.abort(404, message="Page {} doesn't exist".format(slug))
        page.title = parsed_args['title']
        page.content = parsed_args['content']
        db.session.add(page)
        db.session.commit()
        return page, 200


class PageList(Resource):
    @ns.marshal_with(list_fields)
    def get(self):
        pages = Page.query.all()
        return pages

    @ns.marshal_with(page_fields)
    @login_required
    def post(self):
        parsed_args = parser.parse_args()
        title = parsed_args['title']
        content = parsed_args['content']
        if title == '' or content == '':
            ns.abort(400, message="title, content cannot be empty");
        page = Page(title=parsed_args['title'], content=parsed_args['content'])
        db.session.add(page)
        db.session.commit()
        return page, 201


ns.add_resource(PageDetail, '/<string:slug>')
ns.add_resource(PageList, '/')
