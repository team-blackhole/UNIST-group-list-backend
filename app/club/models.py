from app import db

manager = db.Table('manager',
                   db.Column('auth_user_id', db.Integer, db.ForeignKey('auth_user.id'), primary_key=True),
                   db.Column('club_club_id', db.Integer, db.ForeignKey('club_club.id'), primary_key=True)
                   )


class Club(db.Model):
    __tablename__ = 'club_club'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    introduce_one_line = db.Column(db.String(512), nullable=True)
    introduce_all = db.Column(db.Text(), nullable=True)
    is_show = db.Column(db.Boolean, default=False)
    manager = db.relationship('User', secondary=manager)

    # thumbnail_image = db.Column(db.Boolean, default=False)

    def __init__(self, name, introduce_one_line, introduce_all, manager, **_):
        self.name = name
        self.introduce_one_line = introduce_one_line
        self.introduce_all = introduce_all
        self.manager.append(manager)

    def __repr__(self):
        return '<Club %r>' % self.name

    def get_manager_list(self):
        manager_list = []
        for user in self.manager:
            manager_list.append(user.username)
        return manager_list

    def serialize(self):
        print(self.manager.__dict__)
        serialized_data = {
            "name": self.name,
            "introduce_one_line": self.introduce_one_line,
            "introduce_all": self.introduce_all,
            "manager": self.get_manager_list()
        }
        return serialized_data
