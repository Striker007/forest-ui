# -*- coding: utf-8 -*-
""" docker module controller
    ~~~~~~~~~~~~~~~~
"""
from __future__ import print_function
import logging
from flask import Response,\
                  Blueprint, \
                  jsonify,\
                  request,\
                  render_template

from .forms import LaunchForm
from .models import SandboxesManager, \
                    RedisQueue, \
                    RedisDataSet, \
                    RedisConnection


connect = RedisConnection()
queue = RedisQueue(connect)
data_set = RedisDataSet(connect)
manager = SandboxesManager(queue, data_set)

mod_docker = Blueprint('containers', __name__, url_prefix='/containers')
logging.basicConfig(level=logging.DEBUG, filename='./controllers.log')


""" Controller routes
    ~~~~~~~~~~~~~~~~
"""
@mod_docker.route('/launch', methods=['GET'])
def launch():
    branch = request.args.get('branch')
    sandbox = request.args.get('sandbox')
    if ("" != branch) and \
            ("" != sandbox) and \
            manager.launch(sandbox, branch):
        result = "success"
    else:
        result = {"errors": {"branch": "(or sandbox) not selected"}}
    # manager.add("sandbox_10")
    return jsonify(result)\


@mod_docker.route('/list2', methods=['GET'])
def list2():
    list = manager.list()
    return jsonify(list)


@mod_docker.route('/', methods=['GET'])
def list():
    form = LaunchForm(request.form)
    list = manager.list()
    logging.debug(list)
    return render_template(
        "container_list/list.html",
        list={"containers_exist":  bool(list),
              "containers":        list,
              "code_version":      "u",  #manager.code_branch,
              "websokets_version": "u",  #manager.websockets_branch,
              "ip":                "u",  #manager.bind_ip
              },
        form=form)



