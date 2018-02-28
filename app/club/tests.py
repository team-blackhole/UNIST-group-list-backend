import unittest

from flask import g
from flask_testing import TestCase

from app import db, app
from app.auth.models import User, Permission
from test.ready_local_db import Ready


def login_not_manager():
    g.user = User.query.filter_by(username='other manager').first()
    if not g.user:
        print('login failed.')
        assert False


def login_manager():
    g.user = User.query.filter_by(username='manager').first()
    if not g.user:
        print('login failed.')
        assert False


def login_admin():
    admin = User(username='admin', password='pw')
    admin.permissions.append(Permission.query.filter_by(code='admin').first())
    db.session.add(admin)
    db.session.commit()
    g.user = admin


class ClubIntegrationTest(TestCase):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()
        Ready.generate_permission()
        Ready.generate_club()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_clubs(self):
        """only is_shown == True when anonymous access"""
        response = self.client.get('/api/v1/club/list')
        self.assertEqual(response.status_code, 200, msg=response.json)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(len([i for i in response.json if 'manager' in i['name']]), 0)

    def test_get_clubs_when_manager(self):
        """is_shown == True & one's own club"""
        login_manager()
        response = self.client.get('/api/v1/club/list')
        self.assertEqual(response.status_code, 200, msg=response.json)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(len([i for i in response.json if 'manager' in i['name']]), 1)
        self.assertEqual(len([i for i in response.json if 'other manager' in i['name']]), 0)

    def test_get_clubs_when_not_manager(self):
        """same with anonymous access"""
        login_not_manager()
        response = self.client.get('/api/v1/club/list')
        self.assertEqual(response.status_code, 200, msg=response.json)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(len([i for i in response.json if 'manager' in i['name']]), 1)
        self.assertEqual(len([i for i in response.json if 'other manager' in i['name']]), 1)

    def test_get_clubs_when_admin(self):
        """get all"""
        login_admin()
        response = self.client.get('/api/v1/club/list')
        self.assertEqual(response.status_code, 200, msg=response.json)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(len([i for i in response.json if 'manager' in i['name']]), 2)
        self.assertEqual(len([i for i in response.json if 'other manager' in i['name']]), 1)


if __name__ == '__main__':
    unittest.main()
