from faker import Faker
from flask_script import Command

from app import db
from app.auth.models import Permission
from app.auth.models import User
from app.club.models import Club
from app.notice.models import Notice

fake = Faker('ko_KR')


class Ready(Command):
    """ready local db to front-end development"""

    def run(self):
        # permission
        Permission.query.delete()
        permission = Permission(name='admin', code='admin')
        db.session.add(permission)
        db.session.commit()

        # dummy clubs
        Club.query.delete()
        for _ in range(50):
            name = fake.name()
            while User.query.filter_by(username=name).all():
                name = fake.name()
            user = User(username=name,
                        password='pw')
            db.session.add(user)

            name = fake.company()
            while Club.query.filter_by(name=name).all():
                name = fake.company()
            club = Club(name=name,
                        introduce_one_line=fake.bs(),
                        introduce_all='',  # this column also empty in post of api
                        manager=user)
            db.session.add(club)
        db.session.commit()

        # dummy notices
        Notice.query.delete()
        for _ in range(5):
            notice = Notice(title=fake.catch_phrase(),
                            contents=(fake.paragraph(nb_sentences=5, variable_nb_sentences=True,
                                                     ext_word_list=None) + '\n\n') * 3,
                            is_shown=True,
                            is_public=True)
            db.session.add(notice)

        notice = Notice(title='이 공지사항은 비공개 상태입니다.',
                        contents=fake.job(),
                        is_shown=False,
                        is_public=True)
        db.session.add(notice)

        notice = Notice(title='이 공지사항은 권한이 있어야 볼 수 있습니다.',
                        contents=fake.job(),
                        is_shown=True,
                        is_public=False)
        db.session.add(notice)

        db.session.commit()
        return
