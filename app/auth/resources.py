from flask_restplus import Resource, Namespace, fields

from app import db
from app.auth.models import User
from app.base.decorators import login_required, has_permissions

ns = Namespace('Auth', description='User authentication')

auth_fields = ns.model('auth_fields', {
    'username': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
})

perm_fields = ns.model('perm_fields', {
    'name': fields.String,
    'code': fields.String,
})

user_fields = ns.model('user_fields', {
    'id': fields.Integer(),
    'created': fields.DateTime(),
    'modified': fields.DateTime(),
    'username': fields.String(),
    'permissions': fields.Nested(perm_fields),
    'managing_clubs': fields.Raw()
})


class UserBase(Resource):
    def get_user(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            ns.abort(404, message="User {} doesn't exist".format(username))
        return user

    def add_permissions(self, user, perms):
        user.permissions = []
        if perms is None:
            perms = []
        for p in perms:
            user.add_permission(p)

    def add_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user:
            ns.abort(400, message="Username is already exist".format(username))
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user


class UserDetail(UserBase):
    put_parser = ns.parser()
    put_parser.add_argument('cur_password', type=str)
    put_parser.add_argument('new_password', type=str)
    put_parser.add_argument('permissions', type=str, action='append')

    @ns.marshal_with(user_fields)
    @login_required
    def get(self, username):
        user = self.get_user(username)
        return user

    @login_required
    def delete(self, username):
        db.session.delete(user)
        db.session.commit()
        return {}, 204

    @ns.marshal_with(user_fields)
    @login_required
    def put(self, username):
        args = self.put_parser.parse_args()
        user = self.get_user(username)
        # Update password if current one matches
        if None not in [args['cur_password'], args['new_password']]:
            if user.check_password(args['cur_password']):
                user.set_password(args['new_password'])
            else:
                ns.abort(400, message="Invalid password")
        # Update permissions
        self.add_permissions(user, args['permissions'])
        db.session.add(user)
        db.session.commit()
        return user, 200


class UserList(UserBase):
    user_list_parser = ns.parser()
    user_list_parser.add_argument('page', type=int)
    user_list_parser.add_argument('size', type=int)

    user_search_parser = ns.parser()
    user_search_parser.add_argument('username', type=str, help='User email')
    user_search_parser.add_argument('password', type=str, help='User password')
    user_search_parser.add_argument('permissions', type=str, action='append')

    @ns.doc(parser=user_list_parser)
    @ns.marshal_with(user_fields)
    @login_required
    def get(self):
        args = self.user_list_parser.parse_args()
        page = args.get("page") or 1
        size = args.get("size") or 3
        user_list = User.query.filter_by().paginate(page=page, per_page=size).items
        serialized_list = list(map(lambda x: x.serialize(), user_list))
        return serialized_list

    @ns.doc(parser=user_search_parser)
    @ns.marshal_with(user_fields)
    @has_permissions('admin')
    def post(self):
        parsed_args = self.user_searchparser.parse_args()
        user = User(
            username=parsed_args['username']
        )
        user.set_password(parsed_args['password'])
        self.add_permissions(user, parsed_args['permissions'])
        db.session.add(user)
        db.session.commit()
        return user, 201


class UserRegister(UserBase):
    parser = ns.parser()
    parser.add_argument('password', type=str, help='User password', location='form')
    parser.add_argument('username', type=str, help='User email', location='form')

    @ns.doc(parser=parser)
    def post(self):
        args = self.parser.parse_args()
        try:
            if UserBase.add_user(UserBase, args['username'], args['password']):
                # token = user.generate_auth_token()
                # return {'token': token.decode('ascii')}, 200
                return {'status': 'success'}
            else:
                ns.abort(401, message="Invalid register")
        except:
            ns.abort(400, message="error")


class AuthToken(UserBase):
    parser = ns.parser()
    parser.add_argument('password', type=str, help='User password', location='form')
    parser.add_argument('username', type=str, help='User email', location='form')

    @ns.doc(parser=parser)
    def post(self):
        args = self.parser.parse_args()
        user = self.get_user(args['username'])
        if user.check_password(args['password']):
            token = user.generate_auth_token()
            return {'token': token.decode('ascii')}, 200
        else:
            ns.abort(401, message="Invalid login info")


ns.add_resource(AuthToken, '/login')
ns.add_resource(UserRegister, '/user')
ns.add_resource(UserDetail, '/user/<string:username>')
ns.add_resource(UserList, '/users')
