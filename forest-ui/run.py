# -*- coding: utf-8 -*-
"""
    run WEB UI server
    ~~~~~~~~~~~~~~~~
    You can change IP to appropriate
    (routes in ./app/__init__.py)
"""
from app import app


app.run(host='0.0.0.0', port=8081, debug=True, threaded=True)
