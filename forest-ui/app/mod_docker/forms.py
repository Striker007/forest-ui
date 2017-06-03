# -*- coding: utf-8 -*-
"""
    docker module
    ~~~~~~~~~~~~~~~~
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class LaunchForm(FlaskForm):
    branch = StringField('branch', validators=[DataRequired(message="branch name required")])
    sandbox = StringField('sandbox', validators=[DataRequired(message="sandbox name required")])
