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
    @staticmethod
    def generate_permission():
        Permission.query.delete()
        permission = Permission(name='admin', code='admin')
        db.session.add(permission)
        db.session.commit()

    @staticmethod
    def generate_club():
        Club.query.delete()
        User.query.delete()

        for _ in range(20):
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
            club.is_shown = True
            db.session.add(club)
        db.session.commit()

        # to pull below clubs up in the list
        import time
        time.sleep(1.1)

        user = User(username='manager',
                    password='pw')
        db.session.add(user)
        club = Club(name='manager`s club',
                    introduce_one_line=fake.bs(),
                    introduce_all='',
                    manager=user)
        db.session.add(club)
        db.session.commit()

        user = User(username='other manager',
                    password='pw')
        db.session.add(user)
        club = Club(name='other manager`s club',
                    introduce_one_line=fake.bs(),
                    introduce_all='',
                    manager=user)
        db.session.add(club)
        db.session.commit()

    @staticmethod
    def generate_notice():
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

    def run(self):
        self.generate_permission()
        self.generate_club()
        self.generate_notice()
        return
