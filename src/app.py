# -*- coding: utf-8 -*-

import os
import traceback

import sentry_sdk
from sentry_sdk import capture_exception, capture_message
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, request, jsonify
from celery import Celery
from .config import DefaultConfig, CeleryConfig

# For import *
__all__ = ['create_app', 'create_celery_app']


def create_app(config=None, app_name=None):
    """Create a Flask app."""
    if app_name is None:
        app_name = DefaultConfig.PROJECT

    app = Flask(app_name, instance_relative_config=True)
    configure_app(app, config)
    configure_hook(app)
    configure_extensions(app)
    configure_blueprints(app)
    configure_template_filters(app)
    configure_error_handlers(app)
    configure_logging_level()

    return app


def configure_app(app, config=None):
    """Different ways of configurations."""

    # http://flask.pocoo.org/docs/api/#configuration
    app.config.from_object(DefaultConfig)

    # http://flask.pocoo.org/docs/config/#instance-folders
    app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)


def configure_extensions(app):

    # Sentry
    if DefaultConfig.SENTRY_DSN:
        sentry_sdk.init(
            dsn=DefaultConfig.SENTRY_DSN,
            integrations=[FlaskIntegration()],
        )

        capture_message('{} starts'.format(DefaultConfig.PROJECT))


def configure_blueprints(app):
    """Configure blueprints in views."""
    from src.api import DEFAULT_BLUEPRINTS as blueprints
    for blueprint in blueprints:
        app.register_blueprint(
            blueprint,
            url_prefix=f'{blueprint.url_prefix}'
        )


def configure_template_filters(app):
    @app.template_filter()
    def pretty_date(value):
        return pretty_date(value)

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)


def configure_logging_level():
    import logging
    logging.getLogger('suds').setLevel(logging.ERROR)


def configure_hook(app):
    @app.before_request
    def before_request():
        pass


def configure_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_page(error):
        return jsonify(msg="forbidden"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify(msg="notfound"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return jsonify(msg="server error"), 500

def create_celery_app(app=None, name='celery'):
    app = app or create_app()
    celery = Celery(name)
    celery.config_from_object(CeleryConfig)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery