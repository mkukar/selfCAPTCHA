# selfCAPTCHA Project
# CB: Michael Kukar 2019
# MIT License

import os

from flask import Flask, redirect, url_for
from werkzeug.utils import secure_filename


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True, static_url_path='/static')

    app.config.from_mapping(
        SECRET_KEY='dev', # change this to a random number/something unique if releasing outside dev environment
    )

    if test_config is None:
        # loads the instance config when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import iamnotarobot
    app.register_blueprint(iamnotarobot.bp)

    # redirect to selfcaptcha splash page (even for 404 error)
    @app.route('/')
    def selfcaptcha():
        return redirect(url_for('iamnotarobot.splash'))

    @app.errorhandler(404)
    def page_not_found(e):
        # your processing here
        return redirect(url_for('iamnotarobot.splash'))

    return app
    