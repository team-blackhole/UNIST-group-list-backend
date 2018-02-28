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
    def real_club():
        clubs = [
            ["UNICC", "유니스트 싸이클(자전거) 소모임 입니다", "010-5019-8678", ""],
            ["반반 (VAHN-VAHN)",
             "우주 최강 보컬 동아리 입니다. 다양한 장르의 음악을 즐기고 교류하며 버스킹, 공연을 합니다. 아름답고 편안한 가창을 위한 발성 세미나는 우리 동아리의 특색 중 하나입니다",
             "010-4094-1203", "면접없음. 간단한 지원서만 받아요. 여성보컬 급구!"],
            ["I'm SO", "암벽등반 소모임 입니다. ", "010-4002-9448", "근력이 없으셔도 쉽게 시작 하실수 있습니다."],
            ["화이트초콜릿 (White Chocolate)",
             "감성 밴드 동아리 화이트초콜릿입니다! 락, 인디, 팝, 힙합, 발라드, 누구든 원하는 장르를 할 수 있는 자유로운 동아리입니다. 주로 버스킹, 자체 공연 준비 위주의 활동을 하며 모든 점에서 자유를 최우선으로 추구하고 있습니다. 빡빡한 연습, 엄격한 질서, 그런 것 없이 음악을 하고자 하는 분들 모두 환영입니다!",
             "010-9235-5669", ""],
            ["바구니", "유서깊은 농구 소모임입니다.", "", ""],
            ["에이씨발로마(AC Valloma)", "즐거운 축구 동아리(실력 안 봄), 자유로운 분위기! 행복축구!!", "010-4195-8334",
             "실력 필요 없음, 지원하면 다 합격, 부상자 및 공 못 차는 사람 우대"],
            ["PING", "유니스트 e-sports 소모임입니다.", "010-5150-7345", "게임 하는 것을 좋아하시는 분, 보시는 것을 좋아하시는 분 모두 환영합니다!"],
            ["ESF", "학원복음화협의회에서 추천하는 건전한 캠퍼스 기독교 동아리입니다. 성경읽기, 기도회, 또 다양한 주제로 책모임도 진행하고 있습니다. 따뜻한 모임을 바라는 사람들 강추!",
             "010-5173-7532", ""],
            ["IVFC", "건전한 축구 소모임입니다. 실력 상관없이 누구나 즐기면서 축구를 할 수 있는 곳 입니다. 매주 1회 정도 축구를 하며, 실력 및 나이 제한 일절 없습니다.",
             "010-2459-0200", "면접 없음. 나이 및 실력 제한X, 복학생분들도 대환영입니다."],
            ["페더링(Feathering)", "유니스트 양궁 국궁 동아리입니다. ", "010-8684-6506",
             "유니스트 내 양궁장 이용가능. 초보자&리더쉽수강자 모두 환영합니다. 꾸준히 열심히 하실 분 환영합니다!"],
            ["Vectormen", "유니스트 축구 소모임입니다. 자유롭게 나오고 싶을때 나와서 함께 즐겁게 축구할 수 있는 동아리입니다.", "010-5116-9384",
             "항상 상시 모집중입니다. 면접 없고 서로 즐겁게 축구할 수 있는 분이면 좋겠습니다!"],
            ["±0", "유니스트 마작 소모임입니다. 사람을 모아서 마작을 칠 수 있습니다.", "010-5060-3923", "마작 패가 뭔지 모르셔도 괜찮습니다. 초보자 매우 환영"],
        ]

        for club in clubs:
            user = User(username=club[0], password='')
            db.session.add(user)

            club = Club(name=club[0],
                        introduce_one_line=club[1],
                        contact=club[2],
                        introduce_all=club[3],
                        manager=user)
            club.is_shown = True
            db.session.add(club)
        db.session.commit()

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
