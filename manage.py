#!/usr/bin/env python
from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager, Server

from app import app
from test.ready_local_db import Ready

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('db', MigrateCommand)
manager.add_command('ready-local-db', Ready())

if __name__ == '__main__':
    manager.run()
