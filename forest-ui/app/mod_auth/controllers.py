# -*- coding: utf-8 -*-
"""
    auth module
    ~~~~~~~~~~~~~~~~
"""
import logging
from werkzeug import check_password_hash, generate_password_hash
from flask import Flask, Response, Blueprint
from flask import request, render_template, redirect, url_for, flash, session

from app.mod_auth.forms import LoginForm
from app.mod_auth.models import User


mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
logging.basicConfig(level=logging.DEBUG, filename='./controllers.log')


@mod_auth.route('/')
def index():
    return redirect(url_for('auth.signin'))

@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    # If sign in form is submitted
    form = LoginForm(request.form)
    # Verify the sign in form
    if form.validate_on_submit():

        # user = User.query.filter_by(email=form.email.data).first()
        user = User('test', 'test@test.net', '123')

        if user and check_auth(user.password, form.password.data):
            session['user_id'] = user.id

            flash('Welcome %s' % user.name)

            return redirect(url_for('container_list.list'))

        flash('Wrong email or password', 'error-message')

    return render_template("auth/signin.html", form=form)


def check_auth(validPassword, receivedPassword):
    return check_password_hash(
        generate_password_hash(validPassword),
        receivedPassword
    )

#
# @mod_auth.route('/list', methods=['GET'])
# def list():
#     return hello_world()
#
# def hello_world():
#     return "authorized"
#
# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(auth.username, auth.password):
#             return signin()
#         return f(*args, **kwargs)
#
#     return decorated
