# -*- coding: utf-8 -*-
"""
    docker module
    ~~~~~~~~~~~~~~~~
"""
# Define a User model
class User(object):

    id       = 777
    name     = 'test'
    email    = 'test@test.net',
    password = '123'
    role     = 1
    status   = 1

    # def __init__(self, name, email, password):
    def __init__(self, name, email, password):
        self.name     = name
        self.email    = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)

    def query(self):
        return self 
