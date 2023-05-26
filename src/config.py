# -*- coding: utf-8 -*-

import os
import os.path as op
import json
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    PROJECT = "flask-celery-api-template"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = os.getenv("SECRET_KEY")


class DefaultConfig(BaseConfig):
    DEBUG = True

    ACCEPT_LANGUAGES = ['vi']
    BABEL_DEFAULT_LOCALE = 'en'

    # The SQLAlchemy connection string.
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres_local')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PW = os.getenv('POSTGRES_PW', '123456')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'fenris')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

    REDIS_CACHED_URL = os.getenv('REDIS_CACHED_URL')

    SENTRY_DSN = os.getenv('SENTRY_DSN', 'https://54dff5fd6d1840c49cf4eeb73feffc25@o305892.ingest.sentry.io/5080701')



class CeleryConfig(BaseConfig):
    broker_url = os.getenv('REDIS_BROKER_URL', 'redis://localhost:6379/0')
    result_backend = os.getenv('REDIS_RESULT_BACKEND', 'redis://localhost:6379/1')
    result_expires = 86400
    task_default_queue = 'celery'
    task_track_started = 'True'
    enable_utc = True
    # timezone = 'Asia/Ho_Chi_Minh'

    # import tasks
    imports = [
        'src.tasks.task'
    ]
