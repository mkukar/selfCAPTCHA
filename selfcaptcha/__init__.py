# selfCAPTCHA
# Michael Kukar 2019
# MIT License

import os

from flask import Flask 
from werkzeug.utils import secure_filename


def create_app(test_config=None):
    # create and configure the app

    UPLOAD_FOLDER = '/path/to/the/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config.from_mapping(
        SECRET_KEY='dev', # change this to a random number/something unique
        DATABASE=os.path.join(app.instance_path, 'selfcaptcha.sqlite'),
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
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, world!'
    
    from . import iamnotarobot
    app.register_blueprint(iamnotarobot.bp)

    return app
    