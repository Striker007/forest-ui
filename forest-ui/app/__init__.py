# -*- coding: utf-8 -*-
"""
    app initialization
    ~~~~~~~~~~~~~~~~
    Configure app and Routes
"""
from flask import Flask, render_template, redirect, url_for

from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_docker.controllers import mod_docker as container_module


app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(auth_module)
app.register_blueprint(container_module)


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


@app.route('/')
def index():
    return redirect(url_for('containers.list'))
