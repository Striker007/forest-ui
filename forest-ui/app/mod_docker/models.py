# Define a User model
from __future__ import print_function # In python 2.7
import redis
import logging
import sys
import json
#import git, yaml, time
# from flask import Response, Blueprint
# from flask import jsonify, request, render_template
# from docker import Client


class RedisConnection(object):

    queue_name = "tasks"
    db_name = "sandboxes"
    instance = None

    def __init__(self):
        self.get()

    def get(self):
        if self.instance is None:
            try:
                self.instance = redis.StrictRedis(host='localhost', port=6379, db=0)
                self.instance.ping()  # detect if connect is established
            except:
                logging.warn("Redis connecting trouble")
                raise RuntimeError('Initialization trouble')
        else:
            logging.debug('ContainerManager from cache')
        return self.instance


class RedisQueue(object):

    redis = None

    def __init__(self, redis_connection):
        if redis_connection:
            self.redis = redis_connection
        else:
            raise ValueError

    def pop(self):
        return self.redis.instance.rpop(self.redis.queue_name)

    def push(self, value):
        return self.redis.instance.lpush(self.redis.queue_name, value)


class RedisDataSet(object):

    redis = None

    def __init__(self, redis_connection):
        if redis_connection:
            self.redis = redis_connection
        else:
            raise ValueError

    def push(self, key, maping):
        logging.warn(maping)
        # if self.redis.instance.hmset(self.redis.db_name, maping):
        if self.redis.instance.hset(self.redis.db_name, key, maping):
            return True

    def delete(self, value):
        # if self.redis.instance.sadd(self.redis.db_name, value):
        #     return True
        return False

    def list(self):
        result = []
        data = self.redis.instance.hgetall(self.redis.db_name)
        if data:
            for i in data:
                result.append(
                    json.loads(data[i]).values()
                )
        return result


class SandboxesManager(object):

    queue = None
    dataset = None

    def __init__(self, queue, data_set):
        self.queue = queue
        self.data_set = data_set
        pass

    """ add job to queue """
    def launch(self, sandbox, branch):
        result = self.queue.push(sandbox + ':' + branch)
        if result:
            self.add(
                sandbox,
                json.dumps({sandbox: {"name": sandbox, "branch": branch}})
            )
        return bool(result)

    def shutdown(self, branch):
        self.queue.push(branch)
        return True

    def add(self, sandbox, sandbox_mapping):
        self.data_set.push(sandbox, sandbox_mapping)

    def delete(self, sandbox_name):
        self.data_set.delete(sandbox_name)

    def list(self):
        # TODO get sandboxes from Redis
        list = self.data_set.list()
        # logging.warn(list.keys())
        #
        # result = []
        # for key, val in list.iteritems():
        #     result.append({key: json.load(val)})
        # if result:
        #     return result

        return list

        # from datetime import datetime
        # return [{"name": "sandbox_10", "ip": "192.168.0.1", "state": "up",
        #          "branch": "master", "updated": str(datetime.now())}]


# class ContainerManager(object):
#
#     containers = None
#     queue = None
#
#     def __init__(self):
#         # self.queue = queue
#         pass
#
#     def connect(self, base_url='unix://var/run/docker.sock'):
#         cli = Client(base_url)
#         self.containers = cli.containers(all=True)
#         return self.containers
#
#     def how_many(self):
#         return len(self.containers)
#
#     def get_containers(self):
#         return self.containers
#
#     def get_bind_ip(compose_file):
#         with open(compose_file, 'r') as f:
#             conf = yaml.load(f)
#         return conf['proxy-nginx']['ports'][0].split(':')[0]
#
#     def git_branch(source_path):
#         repo = git.Repo(source_path)
#         branch = repo.active_branch
#         return str(branch.name)
#
#     def list(self):
#         code_branch = 'unknown'
#         websockets_branch = 'unknown'
#         bind_ip = 'unknown'
#
#         for container in containers:
#             if 'phpfpm' in container['Image']:
#                 code_branch = docker.git_branch(container['Mounts'][0]['Source'])
#                 logging.debug(docker.git_branch)
#             if 'comet' in container['Image']:
#                 websockets_branch = docker.git_branch(container['Mounts'][0]['Source'])
#                 logging.debug(docker.git_branch)
#             if 'nginx' in container['Image']:
#                 bind_ip = docker.get_bind_ip("/data/docker_sandbox_1/docker-compose.yml")
#
#         action = False
#         if request.method == "POST":
#             action = request.form
#             # logging.debug(action)
#
#         if action:
#             # logging.debug(action)
#             # logging.debug(type(action))
#             # logging.debug(action.keys())
#
#             container_id = action.keys()[0]
#             container_act = action.values()[0]
#             logging.debug(container_act)
#             logging.debug(container_id)
#             if container_act == "restart":
#                 try:
#                     cli.restart(container_id)
#                     time.sleep(0)
#                     containers = cli.containers(all=True)
#                 except BaseException as e:
#                     logging.critical(e)
#                     return render_template('error.html', error=e)
#             if container_act == "stop":
#                 try:
#                     cli.stop(container_id)
#                     time.sleep(0)
#                     containers = cli.containers(all=True)
#                 except BaseException as e:
#                     logging.critical(e)
#                     return render_template('error.html', error=e)
#             if container_act == "start":
#                 try:
#                     cli.start(container_id)
#                     time.sleep(0)
#                     containers = cli.containers(all=True)
#                 except BaseException as e:
#                     logging.critical(e)
#                     return render_template('error.html', error=e)
#             if container_act == "delete":
#                 try:
#                     cli.remove_container(container_id)
#                     time.sleep(0)
#                     containers = cli.containers(all=True)
#                 except BaseException as e:
#                     logging.critical(e)
#                     return render_template('error.html', error=e)
