import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'testkey'
DATABASE = os.path.join(_basedir, 'test.db')
DATABASE_CONNECT_OPTIONS = {}
ADMINS = frozenset(['Greg Ziegan'])

del os
