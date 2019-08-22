import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

bp = Blueprint('iamnotarobot', __name__, url_prefix="/iamnotarobot")

# initial splash screen (I am not a robot checkbox)
@bp.route('/splash', methods=('GET', 'POST'))
def slash():
    return render_template('iamnotarobot/splash.html')

# captcha screen (shows photo and upload windows)
@bp.route('/captcha', methods=('GET', 'POST'))
def captcha():
    return render_template('iamnotarobot/captcha.html')