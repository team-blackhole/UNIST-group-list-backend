import unittest

from flask_testing import TestCase

from app import db, app
from test.ready_local_db import Ready


class NoticeIntegrationTest(TestCase):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()
        Ready().run()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_notice_with_anonymous_access(self):
        """only is_shown == True and is_public == True contents must be returned"""
        response = self.client.get('/api/v1/notice')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 5)
        print(response.json[0]['is_active'])
        self.assertEqual(len([i for i in response.json if not i['is_active'] or not i['is_public']]), 0)

    def test_get_notice_with_login_access(self):
        """only is_shown == True contents must be returned"""
        response = self.client.get('/api/v1/notice')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 6)
        self.assertEqual(len([i for i in response.json if not i['is_active']]), 0)

    def test_get_notice_with_admin_access(self):
        """all contents (including is_shown == False) must be returned"""
        response = self.client.get('/api/v1/notice')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 7)


if __name__ == '__main__':
    unittest.main()
