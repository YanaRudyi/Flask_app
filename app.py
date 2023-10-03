#!/usr/bin/env python3
"""Task API Application

This script sets up and runs a Flask-based API for managing tasks.
"""
from os import environ

import connexion
from dotenv import load_dotenv

from login import login_blueprint
from task import task_blueprint, db


def create_app():
    app = connexion.FlaskApp(__name__)
    app.add_api('swagger.yaml')
    application = app.app
    load_dotenv()
    application.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(application)

    with application.app_context():
        db.create_all()

    application.register_blueprint(task_blueprint)
    application.register_blueprint(login_blueprint)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
